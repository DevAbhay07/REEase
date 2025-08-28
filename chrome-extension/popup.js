document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab + '-content').classList.add('active');
        });
    });
    
    // Load saved API key
    chrome.storage.sync.get(['geminiApiKey'], function(result) {
        if (result.geminiApiKey) {
            document.getElementById('api-key').value = result.geminiApiKey;
            document.getElementById('api-key-section').style.display = 'none';
        }
    });
    
    // Save API key
    document.getElementById('save-key').addEventListener('click', function() {
        const apiKey = document.getElementById('api-key').value.trim();
        if (apiKey) {
            chrome.storage.sync.set({'geminiApiKey': apiKey}, function() {
                document.getElementById('api-key-section').style.display = 'none';
                showMessage('API key saved successfully!', 'success');
            });
        } else {
            showMessage('Please enter a valid API key', 'error');
        }
    });
    
    // Text summarization
    document.getElementById('summarize-text').addEventListener('click', function() {
        const text = document.getElementById('input-text').value.trim();
        const compression = document.getElementById('compression-text').value;
        
        if (!text) {
            showMessage('Please enter some text to summarize', 'error');
            return;
        }
        
        summarizeText(text, compression);
    });
    
    // File summarization
    document.getElementById('summarize-file').addEventListener('click', function() {
        const fileInput = document.getElementById('file-input');
        const compression = document.getElementById('compression-file').value;
        
        if (!fileInput.files[0]) {
            showMessage('Please select a file to summarize', 'error');
            return;
        }
        
        const file = fileInput.files[0];
        extractTextFromFile(file, compression);
    });
    
    // Get selected text
    document.getElementById('get-selected').addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: 'getSelectedText'}, function(response) {
                if (response && response.text) {
                    document.getElementById('selected-text').value = response.text;
                } else {
                    showMessage('No text selected. Please select text on the webpage first.', 'error');
                }
            });
        });
    });
    
    // Summarize selected text
    document.getElementById('summarize-selected').addEventListener('click', function() {
        const text = document.getElementById('selected-text').value.trim();
        const compression = document.getElementById('compression-selected').value;
        
        if (!text) {
            showMessage('No text to summarize. Please get selected text first.', 'error');
            return;
        }
        
        summarizeText(text, compression);
    });
    
    // Core summarization function
    function summarizeText(text, compression) {
        chrome.storage.sync.get(['geminiApiKey'], function(result) {
            if (!result.geminiApiKey) {
                showMessage('Please set your Gemini API key first', 'error');
                document.getElementById('api-key-section').style.display = 'block';
                return;
            }
            
            showLoading();
            
            chrome.runtime.sendMessage({
                action: 'summarize',
                text: text,
                compression: compression,
                apiKey: result.geminiApiKey
            }, function(response) {
                if (response.success) {
                    showResult(response.summary);
                } else {
                    showMessage('Error: ' + response.error, 'error');
                }
            });
        });
    }
    
    // File text extraction
    function extractTextFromFile(file, compression) {
        const reader = new FileReader();
        const fileType = file.name.split('.').pop().toLowerCase();
        
        if (fileType === 'json') {
            reader.onload = function(e) {
                try {
                    const jsonData = JSON.parse(e.target.result);
                    summarizeJsonData(jsonData, compression);
                } catch (error) {
                    showMessage('Invalid JSON file: ' + error.message, 'error');
                }
            };
            reader.readAsText(file);
        } else if (fileType === 'txt') {
            reader.onload = function(e) {
                summarizeText(e.target.result, compression);
            };
            reader.readAsText(file);
        } else {
            showMessage('File type not supported in extension. Please use the web app for PDF, DOCX, and PPTX files.', 'error');
        }
    }
    
    // JSON data summarization
    function summarizeJsonData(jsonData, compression) {
        chrome.storage.sync.get(['geminiApiKey'], function(result) {
            if (!result.geminiApiKey) {
                showMessage('Please set your Gemini API key first', 'error');
                return;
            }
            
            showLoading();
            
            chrome.runtime.sendMessage({
                action: 'summarizeJson',
                jsonData: jsonData,
                compression: compression,
                apiKey: result.geminiApiKey
            }, function(response) {
                if (response.success) {
                    displayJsonSummaries(response.summaries);
                } else {
                    showMessage('Error: ' + response.error, 'error');
                }
            });
        });
    }
    
    // Display JSON summaries
    function displayJsonSummaries(summaries) {
        const resultDiv = document.getElementById('result');
        let html = '<h3>Thread Summaries:</h3>';
        
        summaries.forEach(summary => {
            html += `
                <div style="margin-bottom: 15px; padding: 10px; background: #f8f9fa; border-left: 3px solid #007bff; border-radius: 4px;">
                    <strong>Thread ${summary.thread_id}:</strong>
                    <p style="margin: 5px 0 0 0;">${summary.body}</p>
                </div>
            `;
        });
        
        resultDiv.innerHTML = html;
        resultDiv.style.display = 'block';
    }
    
    // UI helper functions
    function showLoading() {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '<div class="loading">Generating summary...</div>';
        resultDiv.style.display = 'block';
        resultDiv.className = 'result';
    }
    
    function showResult(summary) {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '<h3>Summary:</h3><p>' + summary.replace(/\n/g, '<br>') + '</p>';
        resultDiv.style.display = 'block';
        resultDiv.className = 'result success';
    }
    
    function showMessage(message, type) {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = message;
        resultDiv.style.display = 'block';
        resultDiv.className = 'result ' + type;
        
        // Hide after 3 seconds for error messages
        if (type === 'error') {
            setTimeout(() => {
                resultDiv.style.display = 'none';
            }, 3000);
        }
    }
});