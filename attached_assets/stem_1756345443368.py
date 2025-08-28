import streamlit as st
import PyPDF2

import app

def extract_text_from_pdf(uploaded_file):
    text = ''
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    except Exception as e:
        st.error(f"Error extracting PDF: {e}")
    return text


def write_text_to_file(text):
    try:
        with open("summary.txt", 'wb', encoding='utf-8') as file:
            file.write(text)
        print(f"Data written to file successfully: ")
    except Exception as e:
        print(f"Error writing to file: {e}")


def main():
    st.title("PDF Text Extractor")

    # File upload button
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    # Initialize extracted_text as None
    extracted_text = None

    if uploaded_file is not None:
        # Display file upload confirmation
        st.write("File Uploaded Successfully!")

        # Submit button
        if st.button("Summarize Text"):
            # Perform text extraction on file submission
            extracted_text = extract_text_from_pdf(uploaded_file)
            if extracted_text:
                st.success("Text Extracted Successfully!")
                summarytext = app.generateSummary(extracted_text)
                st.write(summarytext)
                write_text_to_file(summarytext)

            else:
              st.warning("No text extracted from the PDF.")

    # Download button
    if extracted_text:
        download_button = st.download_button(label="Download Text", data=summarytext.encode('utf-8'),file_name="summary.txt")
        if download_button:
            st.info("Text File Downloaded Successfully!")


if __name__ == "__main__":
    main()
