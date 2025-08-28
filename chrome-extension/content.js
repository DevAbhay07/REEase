// Content script for handling text selection on web pages

// Listen for messages from popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'getSelectedText') {
        const selectedText = window.getSelection().toString().trim();
        sendResponse({text: selectedText});
    }
});

// Create context menu for right-click summarization
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'summarizeSelection') {
        const selectedText = window.getSelection().toString().trim();
        if (selectedText) {
            // Send selected text to background script for summarization
            chrome.runtime.sendMessage({
                action: 'summarizeFromContext',
                text: selectedText
            });
        }
    }
});

// Highlight selected text temporarily (visual feedback)
function highlightSelection() {
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const span = document.createElement('span');
        span.style.backgroundColor = '#ffeb3b';
        span.style.transition = 'background-color 0.3s';
        
        try {
            range.surroundContents(span);
            setTimeout(() => {
                span.outerHTML = span.innerHTML;
            }, 1000);
        } catch (e) {
            // If surrounding fails, just continue
        }
    }
}

// Listen for double-click to show summarization option
document.addEventListener('dblclick', function(e) {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText && selectedText.length > 50) {
        // Create a floating button for quick summarization
        createFloatingButton(e.pageX, e.pageY, selectedText);
    }
});

function createFloatingButton(x, y, text) {
    // Remove existing button if any
    const existingButton = document.getElementById('ai-summarizer-button');
    if (existingButton) {
        existingButton.remove();
    }
    
    const button = document.createElement('button');
    button.id = 'ai-summarizer-button';
    button.innerHTML = '🤖 Summarize';
    button.style.cssText = `
        position: absolute;
        top: ${y + 10}px;
        left: ${x}px;
        z-index: 10000;
        background: #007bff;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        transition: all 0.2s;
    `;
    
    button.addEventListener('click', function() {
        chrome.runtime.sendMessage({
            action: 'openPopupWithText',
            text: text
        });
        button.remove();
    });
    
    button.addEventListener('mouseover', function() {
        button.style.background = '#0056b3';
    });
    
    button.addEventListener('mouseout', function() {
        button.style.background = '#007bff';
    });
    
    document.body.appendChild(button);
    
    // Remove button after 5 seconds or when clicking elsewhere
    setTimeout(() => {
        if (button.parentNode) {
            button.remove();
        }
    }, 5000);
    
    document.addEventListener('click', function removeButton(e) {
        if (e.target !== button) {
            button.remove();
            document.removeEventListener('click', removeButton);
        }
    });
}

// Handle messages for inserting text into popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'insertTextIntoPopup') {
        // This will be handled by the popup script
        sendResponse({success: true});
    }
});