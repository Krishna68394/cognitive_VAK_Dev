import streamlit as st
from pdf_processor import PDFProcessor
from ai_assistant_remote import AIStudyAssistant
from visualizer import PDFVisualizer
import time

# Page configuration
st.set_page_config(page_title="📚 PDF Study Assistant",
                   page_icon="📚",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Custom CSS for educational theme
st.markdown("""
<style>
    /* Main theme colors - More visible and clean */
    .stApp {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
        color: #333333;
    }
    
    /* Sidebar styling - Clean and professional */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 3px solid #4ECDC4;
    }
    
    /* Custom styling for main content */
    .main-header {
        background: linear-gradient(90deg, #2E86C1, #28B463, #E74C3C, #AF7AC5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Study mode cards */
    .study-mode-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 5px solid #4ECDC4;
    }
    
    /* Search box styling */
    .search-container {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Progress indicators */
    .progress-indicator {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        height: 4px;
        border-radius: 2px;
        margin: 10px 0;
    }
    
    /* Interactive buttons - More visible */
    .stButton > button {
        background: linear-gradient(45deg, #2E86C1, #28B463);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Chat message styling */
    .chat-message {
        background: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    
    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
    
    /* Educational icons and emojis enhancement */
    .feature-icon {
        font-size: 2rem;
        margin-right: 10px;
    }
</style>
""",
            unsafe_allow_html=True)

# Initialize session state
if 'pdf_processor' not in st.session_state:
    st.session_state.pdf_processor = PDFProcessor()

if 'ai_assistant' not in st.session_state:
    st.session_state.ai_assistant = AIStudyAssistant()

if 'pdf_uploaded' not in st.session_state:
    st.session_state.pdf_uploaded = False

if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = ""

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if 'study_mode' not in st.session_state:
    st.session_state.study_mode = "general"


def main():
    # Enhanced colorful header
    st.markdown(
        '<h1 class="main-header">🎓 STUDY MATE: Smart PDF Study Assistant 📚</h1>',
        unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align: center; font-size: 1.2rem; color: #2C3E50; margin-bottom: 30px; font-weight: 500;">'
        '✨ Upload, Learn, Excel! Your AI-powered study companion ✨'
        '</div>',
        unsafe_allow_html=True)

    # Enhanced colorful sidebar
    with st.sidebar:
        st.markdown("""
            <div style="text-align: left; font-family: 'Trebuchet MS', sans-serif; color: #2E86C1; font-size: 2rem; font-weight: bold; margin-bottom: 10px;">
                 VAK_Dev
            </div>
            <div style="text-align: left;">
                <h2 style="color: #117A65; font-family: 'Segoe UI', sans-serif;">🎒 Study Dashboard</h2>
            </div>
            """,
                    unsafe_allow_html=True)

        # PDF Upload with enhanced styling
        st.markdown("### 📤 Upload Your Study Material")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload your textbook, notes, or study material")

        if uploaded_file is not None:
            if st.button("🔄 Process PDF"):
                with st.spinner("Processing PDF..."):
                    result = st.session_state.pdf_processor.extract_text_from_pdf(
                        uploaded_file)

                    if result['success']:
                        st.session_state.pdf_content = result['text']
                        st.session_state.pdf_uploaded = True
                        st.session_state.ai_assistant.set_pdf_content(
                            result['text'])
                        st.success("✅ PDF processed successfully!")

                        # Display PDF info
                        st.info(
                            st.session_state.pdf_processor.get_pdf_summary())
                    else:
                        st.error(f"❌ Error processing PDF: {result['error']}")

        st.markdown("---")

        # Enhanced Study Mode Selection
        st.markdown("### 🎯 Choose Your Learning Style")
        study_mode = st.selectbox(
            "Study mode:",
            ["general", "examination", "age_appropriate", "visual"],
            index=["general", "examination", "age_appropriate",
                   "visual"].index(st.session_state.study_mode),
            format_func=lambda x: {
                "general": "🔍 General Learning - Comprehensive explanations",
                "examination": "📝 Exam Prep - Structured answers",
                "age_appropriate": "👶 Age-Tailored - Custom difficulty",
                "visual": "📊 Visual Analysis - Charts & graphs"
            }[x])

        # Update session state when mode changes
        if study_mode != st.session_state.study_mode:
            st.session_state.study_mode = study_mode

        # Mode-specific settings
        marks = None
        age = None
        difficulty = "medium"

        if study_mode == "examination":
            st.markdown("**📝 Exam Configuration**")
            marks = st.number_input(
                "🎯 Question marks:",
                min_value=1,
                max_value=100,
                value=10,
                help="How many marks is this question worth?")

        elif study_mode == "age_appropriate":
            st.markdown("**👥 Learning Customization**")
            age = st.number_input("🎂 Student age:",
                                  min_value=5,
                                  max_value=25,
                                  value=16)
            difficulty = st.selectbox(
                "🎚️ Difficulty level:", ["easy", "medium", "hard"],
                format_func=lambda x:
                f"{'🟢' if x=='easy' else '🟡' if x=='medium' else '🔴'} {x.title()}"
            )

        # Enhanced AI Model status with better styling
        st.markdown("---")
        st.markdown("### 🤖 AI Assistant Status")
        if st.session_state.ai_assistant.model_loaded:
            st.markdown(
                '<div class="status-success">🚀 <strong>AI Ready!</strong><br>Your smart assistant is active and ready to help</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="status-info">⚠️ <strong>AI Offline</strong><br>Connect your API token to unlock AI features</div>',
                unsafe_allow_html=True)

        # Add new features section
        if st.session_state.pdf_uploaded:
            st.markdown("---")
            st.markdown("### 🎯 Advanced Features")

            # Quiz Generator
            if st.button("🧠 Generate Quiz",
                         help="Create a quiz based on your PDF content"):
                with st.spinner("🧠 Creating quiz questions..."):
                    quiz_content = st.session_state.ai_assistant.generate_quiz(
                    )
                    st.session_state.chat_history.append({
                        "role":
                        "assistant",
                        "content":
                        quiz_content
                    })
                st.rerun()

            # Concept Linking
            if st.button(
                    "🔗 Link Concepts",
                    help=
                    "Find connections between different concepts in your PDF"):
                with st.spinner("🔗 Analyzing concept relationships..."):
                    concept_links = st.session_state.ai_assistant.generate_concept_links(
                    )
                    st.session_state.chat_history.append({
                        "role":
                        "assistant",
                        "content":
                        concept_links
                    })
                st.rerun()

            # Study Plan Generator
            if st.button("📅 Create Study Plan",
                         help="Generate a personalized study plan"):
                with st.spinner("📅 Creating your study plan..."):
                    study_plan = st.session_state.ai_assistant.generate_study_plan(
                    )
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": study_plan
                    })
                st.rerun()

            # Key Terms Extractor
            if st.button("🔑 Extract Key Terms",
                         help="Identify important terms and definitions"):
                with st.spinner("🔑 Extracting key terms..."):
                    key_terms = st.session_state.ai_assistant.extract_key_terms(
                    )
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": key_terms
                    })
                st.rerun()

    # Enhanced Main content area
    if not st.session_state.pdf_uploaded:
        # Colorful welcome screen with cards
        st.markdown("## 🌟 Study Modes Available")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                '<div class="study-mode-card">'
                '<div class="feature-icon">📚</div>'
                '<h3>General Learning</h3>'
                '<p>Get comprehensive explanations with examples, key concepts, and detailed analysis of any topic from your PDF.</p>'
                '</div>',
                unsafe_allow_html=True)

        with col2:
            st.markdown(
                '<div class="study-mode-card">'
                '<div class="feature-icon">📝</div>'
                '<h3>Exam Preparation</h3>'
                '<p>Receive structured, exam-style answers formatted based on the marks allocated to your questions.</p>'
                '</div>',
                unsafe_allow_html=True)

        with col3:
            st.markdown(
                '<div class="study-mode-card">'
                '<div class="feature-icon">🎯</div>'
                '<h3>Age-Tailored</h3>'
                '<p>Get explanations customized for specific age groups and difficulty levels - perfect for any learner!</p>'
                '</div>',
                unsafe_allow_html=True)

        # Visual mode card
        st.markdown(
            '<div class="study-mode-card" style="max-width: 500px; margin: 20px auto;">'
            '<div class="feature-icon">📊</div>'
            '<h3>Visual Analysis</h3>'
            '<p>Explore your PDF with interactive charts, word frequency analysis, and visual insights.</p>'
            '</div>',
            unsafe_allow_html=True)

        # Add background + box style
        st.markdown("""
            <style>
            /* Full page gradient background */
            body {
                background: linear-gradient(135deg, #f0f9ff, #e0f7fa, #f9f9f9);
                background-attachment: fixed;
            }
            </style>
            """,
                    unsafe_allow_html=True)

        # Gradient heading box
        st.markdown(
            '<div style="text-align: center; font-size: 1.3rem; color: white; '
            'background: linear-gradient(45deg, #2E86C1, #28B463); '
            'padding: 15px; border-radius: 10px; margin: 20px auto; '
            'max-width: 600px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">'
            '🚀 Upload a PDF in the sidebar to start your learning journey!'
            '</div>',
            unsafe_allow_html=True)

    else:
        # PDF is uploaded - show main interface
        if st.session_state.study_mode == "visual":
            # Visual mode
            st.header("📊 PDF Visual Analysis")

            visualizer = PDFVisualizer(st.session_state.pdf_content)
            visualizer.display_visual_dashboard(
                st.session_state.pdf_processor.pages_content)

        else:
            # Enhanced Chat interface with search
            st.markdown("## 💬 Interactive Learning Center")

            # Display mode information with enhanced styling
            mode_info = {
                "general":
                "🔍 **General Learning Mode**: Comprehensive explanations with examples and detailed analysis",
                "examination":
                f"📝 **Exam Preparation Mode**: Structured answers for {marks}-mark questions",
                "age_appropriate":
                f"👥 **Age-Tailored Mode**: Explanations for age {age} with {difficulty} difficulty"
            }

            # Safe mode info display
            st.info(mode_info.get(st.session_state.study_mode, ""))

            # ADD SEARCH FUNCTIONALITY
            st.markdown("### 🔍 Search in PDF")

            search_col1, search_col2 = st.columns([3, 1])
            with search_col1:
                search_query = st.text_input(
                    "🔎 Search for specific content:",
                    placeholder="Enter keywords to search in your PDF...")
            with search_col2:
                if st.button("🔍 Search", type="primary"):
                    if search_query:
                        with st.spinner("🔍 Searching through your PDF..."):
                            search_results = st.session_state.pdf_processor.search_in_pdf(
                                search_query)
                            st.session_state.search_results = search_results

            # Display search results with safe highlighting
            if st.session_state.search_results:
                st.markdown("#### 📋 Search Results")
                for i, result in enumerate(st.session_state.search_results[:5],
                                           1):  # Show top 5 results
                    with st.expander(
                            f"📄 Result {i} - Page {result['page_number']}",
                            expanded=i == 1):
                        # Safe highlighting with proper case-insensitive matching
                        st.info(f"**Page {result['page_number']}:**")
                        # Highlight search terms safely with case-insensitive regex
                        highlighted_text = result['context']
                        if search_query:
                            import re
                            # Escape special regex characters and use case-insensitive replacement
                            escaped_query = re.escape(search_query.strip())
                            highlighted_text = re.sub(f"({escaped_query})",
                                                      r"**\1**",
                                                      highlighted_text,
                                                      flags=re.IGNORECASE)
                        st.markdown(f'"{highlighted_text}"')
                        if st.button(f"📖 More about the content",
                                     key=f"more_{i}"):
                            # Extract content BELOW the search result with proper length based on study mode
                            expanded_content = st.session_state.pdf_processor.get_expanded_content(
                                result['page_number'], result['context'],
                                st.session_state.study_mode, marks, age)
                            auto_question = f"More about: {search_query}"
                            st.session_state.chat_history.append({
                                "role":
                                "user",
                                "content":
                                auto_question
                            })

                            # Create detailed response with the expanded content following study mode rules
                            if st.session_state.study_mode == "examination":
                                mode_text = f"📝 **Examination Answer ({marks} marks):**"
                            elif st.session_state.study_mode == "age_appropriate":
                                mode_text = f"🎓 **Age-Appropriate Explanation (Age {age}):**"
                            else:
                                mode_text = "📚 **Study Response:**"

                            detailed_response = f"""{mode_text}

## 📄 From PDF Content:
{expanded_content}

## 🌐 General Knowledge:
This content appears below your searched topic "{search_query}" in the PDF and provides detailed information about the subject.

## 💡 Key Takeaways:
• The content above is directly related to your search topic
• This information follows immediately after your search result in the document
• Use this expanded context to understand the topic more thoroughly"""

                            st.session_state.chat_history.append({
                                "role":
                                "assistant",
                                "content":
                                detailed_response
                            })
                            st.rerun()

                st.markdown("---")

            # Enhanced Chat history with safe styling
            st.markdown("### 💭 Chat History")
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    with st.chat_message("user", avatar="🧑‍🎓"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(message["content"])

            # Enhanced Chat input
            st.markdown("### ✨ Ask Your Question")
            prompt = st.text_area(
                "💭 What would you like to learn about?",
                placeholder=
                "Ask anything about your PDF content... Try: 'Explain the main concepts', 'Summarize chapter 2', or 'What are the key points?'",
                height=100)

            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("🚀 Ask Question", type="primary") and prompt:
                    # Add user message to chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": prompt
                    })

                    # Generate AI response
                    with st.spinner("🤔 AI is thinking..."):
                        response = st.session_state.ai_assistant.generate_response(
                            prompt, st.session_state.study_mode, marks, age,
                            difficulty)
                        st.session_state.chat_history.append({
                            "role":
                            "assistant",
                            "content":
                            response
                        })
                    st.rerun()

            # Enhanced Quick actions
            st.markdown("---")
            st.markdown("### 🛠️ Quick Actions")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button(
                        "📋 Topic Overview",
                        help=
                        "Get a comprehensive overview of all topics in your PDF"
                ):
                    with st.spinner("🔍 Analyzing document..."):
                        overview = st.session_state.ai_assistant.generate_topic_overview(
                        )
                        st.session_state.chat_history.append({
                            "role":
                            "assistant",
                            "content":
                            f"📋 **Document Overview**\n\n{overview}"
                        })
                    st.rerun()

            with col2:
                if st.button("🧹 Clear Chat", help="Clear all chat history"):
                    st.session_state.chat_history = []
                    st.session_state.search_results = []
                    st.rerun()

            with col3:
                if st.button("📊 Visual Mode",
                             help="Switch to interactive charts and analysis"):
                    # Fix navigation by setting the study mode
                    st.session_state.study_mode = "visual"
                    st.rerun()

            with col4:
                if st.button("📥 Export Chat", help="Export your chat history"):
                    chat_export = "\n\n".join([
                        f"{msg['role'].upper()}: {msg['content']}"
                        for msg in st.session_state.chat_history
                    ])
                    st.download_button(label="💾 Download Chat",
                                       data=chat_export,
                                       file_name="study_session.txt",
                                       mime="text/plain")

    # Enhanced Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; background: linear-gradient(45deg, #2E86C1, #28B463); color: white; '
        'padding: 20px; border-radius: 10px; margin-top: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">'
        '<h4>🎓 Learn smarter, not harder.</h4>'
        '<p>Powered by AI • Built with ❤️ for learners everywhere</p>'
        '<p><small>✨ Upload • 🔍 Search • 💬 Chat • 📊 Visualize • 🚀 Learn</small></p>'
        '</div>',
        unsafe_allow_html=True)


if __name__ == "__main__":
    main()
