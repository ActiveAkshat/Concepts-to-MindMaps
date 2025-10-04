import json
import streamlit as st
from openai import OpenAI, OpenAIError

MODEL = "gemini-2.5-flash"
def generate_mindmap_code(client, text: str):
    messages = [
        {
            "role": "system",
            "content": "You are an expert educational content designer and a precise JSON-generating machine. Your sole purpose is to create a valid, parsable JSON object based on the user's request."
        },
        {
            "role": "user",
            "content": f"""
    Create a beautiful, student-friendly mind map from the text provided below.

    **Task:**
    1.  Analyze the text and deconstruct it into a clear hierarchy: one main topic (root), subtopics, and details.
    2.  Follow all guidelines to populate the nodes and links.

    **Source Text:**
    ---
    {text}
    ---

    **Guidelines:**
    1.  **Hierarchy:** The structure must be logical and intuitive for a learner.
    2.  **Concise Text:** Keep node text short (3-5 words) and student-friendly.
    3.  **Visuals:** Use the provided color palette and add a relevant emoji to every node. (Palette: #FF6B6B, #4ECDC4, #45B7D1, #FFA07A, #98D8C8, #FFD93D, #A8E6CF).
    4.  **Descriptions:** Include a short, helpful description (10-15 words) for each node.
    5.  **Connections:** Ensure all links logically connect related concepts.

    Additional layout control instructions:
    1. Ensure nodes and edges never overlap — they should have enough spacing between them.
    2. If a node text appears multiple times, create a separate node instance with a unique key.
    3. Maintain clear visual separability: no node should touch another node or edge.
    4. Distribute branches evenly around the root for a balanced look.
    5. Keep horizontal and vertical distances consistent between levels.

    **Structural & Layout Guidelines (NEW - Crucial for avoiding visual errors):**
    1.  **Prioritize a Balanced Hierarchy:** The structure should be wider rather than deeper. Avoid creating long, "stringy" chains of nodes (e.g., A -> B -> C -> D). A flatter structure with more branches from the main topics is visually cleaner and prevents awkward line paths.
    2.  **Focus on Key Concepts:** Be selective. Do not map every single detail from the text. A less cluttered map with fewer, more important nodes gives the rendering algorithm more space to draw connections properly and avoids visual overlap.

    **Strict Output Rules (Most Important):**
    1.  **JSON Only:** Your entire response MUST be a single, valid JSON object and nothing else.
    2.  **No Extra Text:** Do NOT include any introductory text, explanations, apologies, or markdown formatting like ```json before or after the JSON object.
    3.  **No Trailing Commas:** Ensure there are no trailing commas after the last element in any array or object.
    4.  **Correct Quoting:** All keys and string values must be enclosed in double quotes ("). Escape any double quotes that appear inside a string value with a backslash (e.g., "His name was \\"John\\"").

    **JSON Format:**
    {{
      "nodes": [
        {{"key": "string", "text": "string", "color": "string", "emoji": "string", "description": "string"}}
      ],
      "links": [
        {{"from": "string", "to": "string"}}
      ]
    }}
    """
        }
    ]

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"}
        )
    except OpenAIError as e:
        st.error(f"❌ Error from API: {e}")
        return None

    msg = resp.choices[0].message.content

    try:
        code = json.loads(msg)
    except json.JSONDecodeError:
        st.error("❌ Could not parse JSON output. Raw response:")
        st.code(msg, language="text")
        return None

    return code
