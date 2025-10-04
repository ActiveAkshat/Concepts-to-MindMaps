import json
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from mindmap import generate_mindmap_code
from render_mindmap import render_enhanced_mindmap

load_dotenv()
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")
MODEL = "gemini-2.5-flash"

@st.cache_resource
def initialize_client():
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    return client

def main():
    st.set_page_config(
        page_title="Mind Map Generator",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better UI
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            font-weight: 800 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Mind Map Generator")
    st.markdown("### Transform your study notes into beautiful, memorable mind maps! 🎨")

    client = initialize_client()

    with st.sidebar:
        st.header("📖 How to Use")
        st.markdown("""
        **Steps:**
        1. 📝 Paste your study notes or textbook content
        2. 🚀 Click "Generate Mind Map"
        3. 🎨 Explore your interactive mind map
        4. 💾 Download as JSON
        """)

    text_input = st.text_area(
        "📚 Enter your study content:",
        height=250,
        placeholder="Example: Photosynthesis is the process by which plants convert light energy into chemical energy. It occurs in chloroplasts and involves light-dependent and light-independent reactions...",
        help="Paste any educational content you want to visualize as a mind map"
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        generate_button = st.button("🚀 Generate Mind Map", use_container_width=True)

    if generate_button:
        if not text_input.strip():
            st.warning("⚠️ Please enter some content first!")
        else:
            with st.spinner("🎨 Creating your mind map... This may take a moment!"):
                result = generate_mindmap_code(client, text_input)

            if result:
                st.success("✅ Mind map generated successfully! 🎉")

                st.markdown("---")

                tab1, tab2, tab3 = st.tabs(
                    ["🗺️ Interactive Mind Map", "📋 Concept Cards", "💾 Export Data"])

                with tab1:
                    st.markdown("#### 🌟 Your Interactive Mind Map")
                    st.info("💡 **Tip:** Hover over nodes to see detailed descriptions!")
                    render_enhanced_mindmap(result)

                with tab2:
                    st.markdown("#### 📚 Concept Cards for Review")

                    if "nodes" in result:
                        cols = st.columns(2)
                        for idx, node in enumerate(result["nodes"]):
                            with cols[idx % 2]:
                                color = node.get("color", "#cccccc")
                                emoji = node.get("emoji", "📌")
                                text = node.get("text", "N/A")
                                desc = node.get("description", "No description available")

                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, {color}ee, {color});
                                    padding: 20px;
                                    margin: 10px 0;
                                    border-radius: 15px;
                                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                    color: white;
                                    transition: transform 0.2s;
                                ">
                                    <div style="font-size: 32px; margin-bottom: 10px;">{emoji}</div>
                                    <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">{text}</div>
                                    <div style="font-size: 14px; opacity: 0.95;">{desc}</div>
                                </div>
                                """, unsafe_allow_html=True)

                with tab3:
                    st.markdown("#### 💾 Export Your Mind Map")

                    col1, col2 = st.columns(2)

                    with col1:
                        json_str = json.dumps(result, indent=2)
                        st.download_button(
                            label="⬇️ Download JSON File",
                            data=json_str,
                            file_name="mindmap_study_notes.json",
                            mime="application/json",
                            use_container_width=True
                        )

                    with col2:
                        st.markdown("**Use this to:**")
                        st.markdown("- 📱 Share with classmates")
                        st.markdown("- 💻 Import into other tools")
                        st.markdown("- 🔄 Edit and customize later")

                    st.markdown("**📄 JSON Preview:**")
                    st.json(result)


if __name__ == "__main__":
    main()