import streamlit as st
import PyPDF2
import json
import os
import io
from summarizer import TextSummarizer
import docx
import pptx
import textract

def extract_text_from_file(uploaded_file) -> str:
    """Extract text from various file formats"""
    text = ''
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == "pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                if page_text:
                    text += page_text + "\n"
                    
        elif file_extension == "docx":
            doc = docx.Document(uploaded_file)
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
                    
        elif file_extension == "txt":
            text = uploaded_file.read().decode("utf-8")
            
        elif file_extension == "pptx":
            ppt = pptx.Presentation(uploaded_file)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        text += shape.text + "\n"
        else:
            # Fallback to textract for other formats
            try:
                text = textract.process(uploaded_file).decode("utf-8")
            except Exception:
                st.error(f"Unsupported file format: {file_extension.upper()}")
                return ""
            
    except Exception as e:
        st.error(f"Error extracting text from {uploaded_file.name}: {str(e)}")
        return ""
    
    return text.strip()

def process_json_file(uploaded_file) -> list:
    """Process uploaded JSON file and extract thread data"""
    try:
        # Read the JSON file content
        content = uploaded_file.read().decode("utf-8")
        data = json.loads(content)
        
        if not isinstance(data, list):
            st.error("JSON file should contain a list of email messages")
            return []
        
        return data
        
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON file: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Error processing JSON file: {str(e)}")
        return []

def create_download_file(content: str, file_format: str) -> bytes:
    """Create downloadable file content"""
    try:
        if file_format.lower() == "docx":
            doc = docx.Document()
            doc.add_paragraph(content)
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            return buffer.getvalue()
        else:
            # Default to text format
            return content.encode('utf-8')
    except Exception as e:
        st.error(f"Error creating download file: {str(e)}")
        return content.encode('utf-8')

def main():
    st.title("Document Text Summarizer")
    st.markdown("Upload documents or enter text to generate AI-powered summaries using Google Gemini.")
    
    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("⚠️ GEMINI_API_KEY environment variable is not set. Please configure your API key to use this application.")
        st.stop()
    
    try:
        summarizer = TextSummarizer()
    except Exception as e:
        st.error(f"Failed to initialize summarizer: {str(e)}")
        st.stop()
    
    # Main interface
    input_method = st.radio(
        "Select Input Method", 
        ("Upload File", "Enter Text", "Upload JSON (Email Threads)"),
        help="Choose how you want to provide content for summarization"
    )
    
    if input_method == "Upload File":
        st.subheader("📁 File Upload")
        
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=["pdf", "docx", "txt", "pptx"],
            help="Supported formats: PDF, Word, Text, PowerPoint"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            
            # Summarization options
            col1, col2 = st.columns(2)
            with col1:
                compression = st.selectbox(
                    "Summary Length", 
                    ["Regular", "25%", "50%", "75%"],
                    help="Choose the compression level for your summary"
                )
            
            with col2:
                download_format = st.selectbox(
                    "Download Format", 
                    ["TXT", "DOCX"],
                    help="Choose the format for the downloaded summary"
                )
            
            if st.button("🚀 Generate Summary", type="primary"):
                with st.spinner("Extracting text from file..."):
                    extracted_text = extract_text_from_file(uploaded_file)
                
                if extracted_text:
                    st.success("✅ Text extracted successfully!")
                    
                    with st.spinner("Generating AI summary..."):
                        compression_ratio = None if compression == "Regular" else compression
                        summary = summarizer.generate_summary(extracted_text, compression_ratio)
                    
                    if summary:
                        st.subheader("📝 Generated Summary")
                        st.text_area("Summary", summary, height=300, disabled=True)
                        
                        # Download functionality
                        file_content = create_download_file(summary, download_format)
                        file_name = f"summary.{download_format.lower()}"
                        
                        st.download_button(
                            label=f"⬇️ Download {download_format}",
                            data=file_content,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                    else:
                        st.error("Failed to generate summary. Please try again.")
                else:
                    st.error("No text could be extracted from the file. Please check the file format and content.")
    
    elif input_method == "Enter Text":
        st.subheader("✏️ Text Input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Input Text**")
            input_text = st.text_area(
                "Enter your text here", 
                placeholder="Paste or type the text you want to summarize...",
                height=400,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Summary**")
            summary_placeholder = st.empty()
            
            if input_text.strip():
                with st.spinner("Generating summary..."):
                    summary = summarizer.generate_summary(input_text)
                summary_placeholder.text_area(
                    "Generated summary",
                    summary,
                    height=400,
                    disabled=True,
                    label_visibility="collapsed"
                )
            else:
                summary_placeholder.text_area(
                    "Generated summary",
                    "Enter text in the left box to see the summary here...",
                    height=400,
                    disabled=True,
                    label_visibility="collapsed"
                )
    
    elif input_method == "Upload JSON (Email Threads)":
        st.subheader("📧 Email Thread Summarization")
        st.info("Upload a JSON file containing email thread data to generate summaries for each thread.")
        
        uploaded_json = st.file_uploader(
            "Choose a JSON file", 
            type=["json"],
            help="JSON file should contain email thread data with thread_id and body fields"
        )
        
        if uploaded_json is not None:
            st.success(f"✅ JSON file '{uploaded_json.name}' uploaded successfully!")
            
            if st.button("🚀 Generate Thread Summaries", type="primary"):
                with st.spinner("Processing JSON file..."):
                    json_data = process_json_file(uploaded_json)
                
                if json_data:
                    with st.spinner("Generating summaries for email threads..."):
                        summaries = summarizer.summarize_json_threads(json_data)
                    
                    if summaries:
                        st.subheader("📝 Thread Summaries")
                        
                        # Display summaries
                        for i, summary in enumerate(summaries):
                            with st.expander(f"Thread {summary.get('thread_id', 'Unknown')}"):
                                st.write(summary.get('body', 'No summary available'))
                        
                        # Download functionality
                        json_content = json.dumps(summaries, indent=2)
                        
                        st.download_button(
                            label="⬇️ Download JSON Summary",
                            data=json_content.encode('utf-8'),
                            file_name="thread_summaries.json",
                            mime="application/json"
                        )
                    else:
                        st.error("Failed to generate summaries. Please check your JSON file format.")
                else:
                    st.error("Failed to process JSON file. Please check the file format.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "Powered by Google Gemini AI • Built with Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
