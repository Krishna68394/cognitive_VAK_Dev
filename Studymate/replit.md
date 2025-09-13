# PDF Study Assistant

## Overview

The PDF Study Assistant is an AI-powered educational tool that helps students interact with PDF documents through intelligent question-answering capabilities. The application extracts text from uploaded PDF files and uses AI models to provide contextual responses in multiple study modes, including general questions, exam preparation, and age-appropriate explanations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application providing an interactive user interface
- **Layout**: Wide layout with sidebar for file upload and settings, main area for chat interface
- **State Management**: Streamlit session state to maintain PDF content, chat history, and component instances across user interactions

### Backend Architecture
- **Modular Design**: Separated into distinct components for PDF processing, AI assistance, and visualization
- **AI Integration**: Dual implementation approach with local model fallback and remote API integration
- **Text Processing**: Multi-stage PDF text extraction with cleaning and formatting capabilities

### Core Components

#### PDF Processing (`PDFProcessor`)
- **Primary Library**: pdfplumber for accurate text extraction with formatting preservation
- **Fallback Support**: pypdf as alternative extraction method
- **Content Structure**: Page-by-page text extraction with metadata capture
- **Text Cleaning**: Regex-based cleaning to remove artifacts and improve readability

#### AI Assistant (`AIStudyAssistant`)
- **Dual Implementation**: 
  - Local model using TinyLlama via Hugging Face transformers
  - Remote inference using Hugging Face API for scalability
- **Context Awareness**: Incorporates PDF content into AI prompts for relevant responses
- **Multiple Study Modes**: Supports different interaction patterns (general, exam prep, age-appropriate)
- **Error Handling**: Graceful degradation when models are unavailable

#### Visualization (`PDFVisualizer`)
- **Analytics**: Word frequency analysis and content visualization
- **Charts**: Interactive Plotly visualizations for document insights
- **Text Analysis**: Stop word filtering and statistical content breakdown

### Data Flow
1. User uploads PDF file through Streamlit interface
2. PDFProcessor extracts and cleans text content
3. AIStudyAssistant receives user questions with PDF context
4. AI model generates contextual responses based on study mode
5. Results displayed in chat interface with visualization options

### Error Handling Strategy
- **Graceful Degradation**: Application remains functional even when AI components fail
- **User Feedback**: Clear error messages and status indicators
- **Fallback Options**: Multiple PDF extraction methods and AI implementation approaches

## External Dependencies

### AI/ML Services
- **Hugging Face Transformers**: Local AI model inference with TinyLlama model
- **Hugging Face Inference API**: Remote AI processing for enhanced capabilities
- **PyTorch**: Machine learning framework for local model execution

### PDF Processing
- **pdfplumber**: Primary PDF text extraction with layout preservation
- **pypdf**: Secondary PDF processing library for fallback support

### Data Visualization
- **Plotly**: Interactive charting and visualization components
- **Matplotlib/Seaborn**: Statistical plotting capabilities
- **Pandas**: Data manipulation for analytics features

### Web Framework
- **Streamlit**: Complete web application framework with built-in state management

### Text Processing
- **Regular Expressions (re)**: Text cleaning and pattern matching
- **Collections**: Data structure utilities for frequency analysis

### Environment Configuration
- **Environment Variables**: HUGGINGFACE_API_TOKEN for API authentication
- **OS Module**: System environment access for configuration management