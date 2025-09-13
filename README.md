# cognitive_VAK_Dev
Studymate: Smart PDF Study Assistant

## 🌐 Live Demo  
Try it here: [PDF Study Assistant](https://a4baedc4-e7cf-4bd4-859b-fa532dfcb184-00-26rt7icissovg.pike.replit.dev/)

📘 PDF Study Assistant

PDF Study Assistant is an AI-powered educational tool that helps students interact with PDF documents through intelligent question-answering capabilities. The application extracts text from uploaded PDF files and uses AI models to provide contextual responses in multiple study modes, including:

🧾 General questions

📝 Exam preparation

👶 Age-appropriate explanations

🚀 Features

📂 Upload PDFs and extract clean, structured text

🤖 AI-powered Q&A with contextual responses

🧑‍🎓 Study Modes: General, exam prep, age-specific explanations

📊 Visual Insights: Word frequency analysis, charts, and content breakdown

⚡ Dual AI Integration: Local lightweight models + Hugging Face API fallback

🛠️ Graceful error handling with fallback PDF processors and AI models

🏗️ System Architecture
Frontend

Framework: Streamlit
 web app

Layout: Wide interface with sidebar (upload/settings) & main chat area

State Management: Streamlit session state for chat history & PDF content

Backend

Modular design: Separate components for PDF processing, AI assistant, and visualization

AI Integration: Local (TinyLlama) + Remote (Hugging Face API)

Text Processing: Multi-stage extraction + regex-based cleaning

🔑 Core Components
📄 PDFProcessor

Library: pdfplumber (primary), pypdf (fallback)

Extracts page-by-page text with metadata

Regex cleaning for better readability

🤖 AIStudyAssistant

Local model: TinyLlama
 via Hugging Face Transformers

Remote model: Hugging Face Inference API

Context awareness: Uses extracted PDF content in responses

Modes supported: General Q&A, Exam Prep, Age-specific explanations

Error handling: Graceful fallback when models are unavailable

📊 PDFVisualizer

Analytics: Word frequency + content statistics

Charts: Interactive Plotly
 graphs

Text analysis: Stop word filtering + breakdown

🔄 Data Flow

📤 User uploads a PDF via Streamlit

📄 PDFProcessor extracts and cleans text

🤖 AIStudyAssistant receives question + PDF context

🧠 AI generates contextual response based on chosen study mode

💬 Response + visual insights displayed in UI

⚠️ Error Handling

✅ Graceful degradation: App remains functional even if AI fails

🛠️ Fallbacks: Multiple extraction methods & AI implementations

🔔 Clear feedback: User-friendly error messages & status indicators

📦 External Dependencies
AI / ML Services

Hugging Face Transformers (local inference)

Hugging Face Inference API (remote processing)

PyTorch (for running local models)

PDF Processing

pdfplumber (primary)

pypdf (fallback)

Visualization & Data

plotly (interactive charts)

matplotlib, seaborn (statistical plots)

pandas (data manipulation)

Web Framework

Streamlit

Text Processing

re (regular expressions)

collections (frequency analysis utilities)
