# Overview

This is a document summarization application built with Streamlit that leverages Google's Gemini AI to generate intelligent summaries of various document formats. The application supports multiple file types (PDF, DOCX, TXT, PPTX) and JSON data structures, offering users flexible compression ratios (25%, 50%, 75%) for customized summary lengths. The system is designed to extract text from uploaded documents and process them through Google's generative AI to produce concise, readable summaries while maintaining essential information.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web application framework for rapid UI development
- **File Upload System**: Multi-format file uploader supporting PDF, DOCX, TXT, PPTX, and JSON
- **Interactive Controls**: Compression ratio selection and real-time summary generation
- **Error Handling**: User-friendly error messages for unsupported formats and processing failures

## Backend Architecture
- **Text Extraction Layer**: Modular text extraction system with format-specific processors
  - PyPDF2 for PDF documents
  - python-docx for Word documents  
  - python-pptx for PowerPoint presentations
  - textract as fallback for additional formats
- **AI Processing Service**: Centralized TextSummarizer class managing Google Gemini API interactions
- **Prompt Engineering**: Dynamic prompt generation based on compression ratio requirements
- **JSON Processing**: Specialized handling for structured email/message data with thread organization

## Data Processing Pipeline
- **Input Validation**: File type verification and content validation
- **Text Normalization**: Cleaning and formatting of extracted text
- **Compression Logic**: Ratio-based summarization with different detail levels
- **Output Formatting**: Clean text output with asterisk and hash removal

## Error Management
- **Graceful Degradation**: Fallback mechanisms for unsupported file types
- **Exception Handling**: Comprehensive error catching with user feedback
- **Logging**: Error tracking for debugging and monitoring

# External Dependencies

## AI/ML Services
- **Google Gemini API**: Primary generative AI service for text summarization
  - Model: gemini-2.5-flash for fast processing
  - API Key authentication via environment variables
  - Content generation with custom prompts

## Document Processing Libraries
- **PyPDF2**: PDF text extraction and page-by-page processing
- **python-docx**: Microsoft Word document parsing
- **python-pptx**: PowerPoint presentation text extraction
- **textract**: Universal document processing fallback

## Web Framework
- **Streamlit**: Complete web application framework with file upload, UI components, and session management

## Development Tools
- **Python Standard Library**: JSON processing, file I/O, and environment variable management
- **Logging**: Built-in Python logging for error tracking

## Environment Configuration
- **GEMINI_API_KEY**: Required environment variable for Google AI authentication
- **File System**: Local storage for temporary file processing and output generation