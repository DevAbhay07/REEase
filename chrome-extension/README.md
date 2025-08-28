# AI Document Summarizer Chrome Extension

A powerful Chrome extension that uses Google Gemini AI to summarize documents, text, and email threads directly in your browser.

## Features

- **Text Summarization**: Enter or paste text for instant AI summarization
- **File Upload**: Support for TXT and JSON files (PDF/DOCX require the web app)
- **Webpage Text Selection**: Select text on any webpage and summarize it
- **Multiple Compression Levels**: Choose 25%, 50%, 75%, or regular summary length
- **Email Thread Processing**: Upload JSON files with email data for thread-by-thread summaries
- **Context Menu Integration**: Right-click selected text to summarize
- **Quick Access**: Floating summarize button appears when you double-click text

## Installation

1. **Download/Copy the Extension Files**: Ensure you have all files in a folder:
   - manifest.json
   - popup.html
   - popup.js
   - content.js
   - background.js
   - icon files (add 16x16, 48x48, and 128x128 PNG icons)

2. **Install in Chrome**:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the chrome-extension folder
   - The extension should now appear in your extensions list

3. **Set Up API Key**:
   - Click the extension icon in your toolbar
   - Enter your Gemini API key (get one from https://aistudio.google.com/)
   - Click "Save API Key"

## Usage

### Text Summarization
1. Click the extension icon
2. Select the "Text" tab
3. Paste your text in the textarea
4. Choose summary length
5. Click "Summarize"

### File Upload
1. Click the extension icon
2. Select the "File" tab
3. Choose a TXT or JSON file
4. Select compression level
5. Click "Summarize File"

### Selected Text (from any webpage)
1. Select text on any webpage
2. Click the extension icon
3. Go to "Selected" tab
4. Click "Get Selected Text"
5. Click "Summarize"

### Right-Click Context Menu
1. Select text on any webpage
2. Right-click and choose "Summarize selected text"

### Double-Click Quick Access
1. Double-click on text (50+ characters)
2. A floating "🤖 Summarize" button will appear
3. Click it to open the extension with the text

## Icon Setup

Replace the placeholder icon files with proper PNG images:
- icon16.png (16x16 pixels)
- icon48.png (48x48 pixels)  
- icon128.png (128x128 pixels)

You can create simple icons with a text editor symbol or AI/document icon.

## Supported File Types

- **Text files** (.txt): Direct text extraction and summarization
- **JSON files** (.json): Email thread processing and summarization
- **Note**: PDF, DOCX, and PPTX files are supported in the web application but not in the extension due to browser limitations

## API Usage

This extension uses the Google Gemini API. You'll need:
1. A Google account
2. Access to Google AI Studio (https://aistudio.google.com/)
3. An API key (free tier available)

## Privacy

- Your API key is stored locally in Chrome's sync storage
- No data is sent to external servers except Google's Gemini API
- Text processing happens directly through Google's API

## Troubleshooting

- **"Please set your Gemini API key"**: Enter a valid API key in the extension popup
- **"No text selected"**: Make sure you've selected text on the webpage before clicking "Get Selected Text"
- **API errors**: Check that your API key is valid and you haven't exceeded rate limits
- **Extension not working**: Try refreshing the page or reloading the extension in chrome://extensions/

## Development

This extension is built with:
- Manifest V3 (latest Chrome extension format)
- Vanilla JavaScript (no external dependencies)
- Google Gemini API for AI summarization
- Chrome Extension APIs for tab and storage management