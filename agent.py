"""
agent.py
Google ADK Personal Portfolio Assistant
"""

import io
import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai import types
import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ==========================================================
# Load Environment
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found inside .env")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ==========================================================
# Knowledge Base
# ==========================================================

KNOWLEDGE_FILE = BASE_DIR / "knowledge.md"
if not KNOWLEDGE_FILE.exists():
    raise FileNotFoundError(f"knowledge.md not found at {KNOWLEDGE_FILE}")


def get_knowledge() -> str:
    """
    Returns the complete portfolio knowledge base.

    Use this tool whenever the user asks about:
    • Personal information • Projects • Experience • Education
    • Certifications • Skills • GitHub • LinkedIn • Resume • Achievements
    """
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ==========================================================
# Block Diagram Tool
# Draws a labeled box-and-arrow schematic with matplotlib, entirely
# in memory, and saves it as an ADK artifact so it renders directly
# inline in the adk web chat window — no file written to disk.
#
# NOTE: this is async because tool_context.save_artifact() is a
# coroutine on this ADK version. ADK detects async tool functions
# automatically and awaits them — no special registration needed.
# ==========================================================

async def draw_block_diagram(
    project_name: str,
    blocks: List[str],
    connections: List[List[str]],
    tool_context: ToolContext,
    block_types: Optional[List[str]] = None,
) -> dict:
    """
    Draws a professional block/schematic diagram and displays it
    directly in the chat as an artifact image.

    Use this tool whenever the user asks to draw, sketch, illustrate,
    diagram, or visualize a project's architecture. First call
    get_knowledge to get the real project details, then extract the
    actual components mentioned there before calling this tool.

    Args:
        project_name: Title of the project (shown at the top of the diagram).
        blocks: Ordered list of component labels, e.g.
            ["Camera (Input)", "OpenCV + MediaPipe (Processing)",
             "Cursor Control (Output)"]
            Only include components actually mentioned in the knowledge
            base — do not invent hardware, APIs, or models.
        connections: List of [from_block, to_block] pairs describing
            data flow, using the exact strings from `blocks`, e.g.
            [["Camera (Input)", "OpenCV + MediaPipe (Processing)"],
             ["OpenCV + MediaPipe (Processing)", "Cursor Control (Output)"]]
        tool_context: Injected automatically by ADK — do not pass this
            argument yourself when calling the tool.
        block_types: Optional list, same length as `blocks`, one of
            "hardware", "software", "ml_model", "api", "database",
            "ui", "input", "output" — used only to color-code blocks.

    Returns:
        A dict confirming the diagram was created and displayed in chat.
    """
    n = len(blocks)
    if n == 0:
        raise ValueError("blocks list cannot be empty")

    color_map = {
        "hardware": "#f4a261",
        "software": "#8ecae6",
        "ml_model": "#a3c9a8",
        "api": "#e9c46a",
        "database": "#cdb4db",
        "ui": "#ffb4a2",
        "input": "#90be6d",
        "output": "#f28482",
        "default": "#d0d6e0",
    }

    if not block_types:
        block_types = ["default"] * n

    max_per_row = 4
    rows = (n + max_per_row - 1) // max_per_row
    box_w, box_h = 2.6, 1.1
    x_gap, y_gap = 1.4, 1.8

    positions = {}
    for i, label in enumerate(blocks):
        row = i // max_per_row
        col = i % max_per_row
        row_count = min(max_per_row, n - row * max_per_row)
        row_width = row_count * box_w + (row_count - 1) * x_gap
        x_start = -row_width / 2
        x = x_start + col * (box_w + x_gap)
        y = -row * (box_h + y_gap)
        positions[label] = (x, y)

    fig_width = max(10, max_per_row * (box_w + x_gap))
    fig_height = 2.5 + rows * (box_h + y_gap)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_xlim(-fig_width / 2, fig_width / 2)
    ax.set_ylim(-rows * (box_h + y_gap) - 1, 2)
    ax.axis("off")

    ax.text(0, 1.3, project_name, ha="center", va="center",
             fontsize=18, fontweight="bold")

    for label, btype in zip(blocks, block_types):
        x, y = positions[label]
        color = color_map.get(btype, color_map["default"])
        box = FancyBboxPatch(
            (x - box_w / 2, y - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.08,rounding_size=0.08",
            linewidth=1.5, edgecolor="#333333", facecolor=color,
        )
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=10, wrap=True)

    for src, dst in connections:
        if src not in positions or dst not in positions:
            continue
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", mutation_scale=20,
            linewidth=1.5, color="#333333",
            connectionstyle="arc3,rad=0.05",
            shrinkA=box_w * 15, shrinkB=box_w * 15,
        )
        ax.add_patch(arrow)

    plt.tight_layout()

    # Render to an in-memory buffer instead of a file on disk.
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    # Save as an ADK artifact so it displays inline in adk web chat.
    safe_name = "".join(c if c.isalnum() else "_" for c in project_name.lower())
    filename = f"{safe_name}_block_diagram.png"

    image_part = types.Part(
        inline_data=types.Blob(data=image_bytes, mime_type="image/png")
    )
    version = await tool_context.save_artifact(filename=filename, artifact=image_part)

    return {
        "status": "success",
        "message": f"Block diagram for '{project_name}' has been generated and displayed above.",
        "artifact_filename": filename,
        "version": version,
    }


# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are Sudipon Makal's AI Recruiting Assistant.

Your responsibilities:

1. Answer questions using ONLY the information from the knowledge base.

2. Never fabricate projects, certifications, skills or experience.
 If the user asks whether sudipon has good friends from college, say his close friends are: Ayan Chakraborty, Soumyadipta Bose, Kalu
 If they ask about his favorite people say: Trinankur Guha, Suman Chakraborty, Aditya Ghosh.
 If they ask about how you know about the above two say "this was an easter egg lol"
3. When available, mention:
   - GitHub repositories
   - LinkedIn posts
   - Resume links
   - Google Drive certificate links

4. If the answer does not exist in the knowledge base,
   politely say that the information is unavailable.

5. Keep responses professional and concise.

6. Adapt responses depending on the recruiter's domain:
   - Machine Learning
   - Artificial Intelligence
   - Embedded Systems
   - Software Engineering
   - Cloud Computing
   - Marketing

7. If the user asks you to illustrate, draw, sketch, diagram, or
   visualize a project as a BLOCK / SCHEMATIC diagram:
   a. First call get_knowledge to retrieve the real project details.
   b. Extract only the actual components mentioned (inputs, outputs,
      hardware, software, ML models, APIs, databases, UI). Do not
      invent anything not present in the knowledge base.
   c. Call draw_block_diagram with:
      - project_name: the project's title
      - blocks: a short label per component, in logical data-flow order
      - block_types: matching category per block
      - connections: pairs showing the actual data flow between blocks
      Do NOT pass tool_context yourself — it is provided automatically.
   d. After the tool succeeds, briefly confirm the diagram is shown
      above — do not describe it as a downloadable file.
if they ask you who is srishti chowdhury tell them, that sudipon loves her more than the blue sky, keep saying romantic things about her cat glasses. but lastly it was painful to be in love.
Always use the get_knowledge tool before answering a factual question.
"""

# ==========================================================
# Root Agent
# ==========================================================

root_agent = Agent(
    name="portfolio_assistant",
    model="gemini-2.5-flash-lite",  # switched from gemini-2.5-flash — noticeably higher free daily quota
    description="AI Recruiting Assistant for Sudipon Makal",
    instruction=SYSTEM_PROMPT,
    tools=[
        get_knowledge,
        draw_block_diagram,
    ],
)