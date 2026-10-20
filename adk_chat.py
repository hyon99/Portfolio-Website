import asyncio
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

from agent import root_agent

APP_NAME = "portfolio"
USER_ID = "streamlit"

session_service = InMemorySessionService()
# Required for tool_context.save_artifact() (used by draw_block_diagram) to
# work at all — without an artifact_service on the Runner, save_artifact()
# raises a ValueError, which is what was crashing requests like
# "describe a project with a diagram".
artifact_service = InMemoryArtifactService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    artifact_service=artifact_service,
)

SESSION_ID = str(uuid.uuid4())
_session_ready = False


async def _ensure_session():
    global _session_ready
    if _session_ready:
        return
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    except Exception:
        # Session already exists (or was created by a prior call) — fine.
        pass
    _session_ready = True


async def _ask(prompt: str) -> dict:
    """Runs one turn against the agent.

    Returns {"text": str, "images": [bytes, ...]} — images are PNG bytes for
    any diagrams generated during this turn via draw_block_diagram.
    """
    await _ensure_session()

    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    answer = ""
    artifact_filenames = set()

    try:
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=message,
        ):
            # Some events (tool-call-only, partial/thinking, control events)
            # carry no content at all — skip those instead of crashing.
            if not event.content or not event.content.parts:
                continue

            for part in event.content.parts:
                # Collect the final answer's text.
                if event.is_final_response() and getattr(part, "text", None):
                    answer += part.text

                # draw_block_diagram's tool result includes the filename it
                # saved the diagram under — collect it so we can fetch the
                # actual image bytes afterwards.
                fr = getattr(part, "function_response", None)
                if fr is not None and isinstance(fr.response, dict):
                    fname = fr.response.get("artifact_filename")
                    if fname:
                        artifact_filenames.add(fname)

    except Exception as e:
        return {
            "text": f"Sorry, something went wrong while generating a response: {e}",
            "images": [],
        }

    images = []
    for fname in artifact_filenames:
        try:
            artifact = await artifact_service.load_artifact(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID,
                filename=fname,
            )
            if artifact is not None and getattr(artifact, "inline_data", None):
                data = artifact.inline_data.data
                if data:
                    images.append(data)
        except Exception:
            # Don't let a failed image fetch take down the whole reply —
            # the text answer still gets through.
            continue

    if not answer.strip() and not images:
        answer = "Sorry, I couldn't generate a response — please try rephrasing your question."

    return {"text": answer, "images": images}


def ask_agent(prompt: str) -> dict:
    return asyncio.run(_ask(prompt))