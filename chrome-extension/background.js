// Background service worker for Chrome extension

// Create context menu when extension is installed
chrome.runtime.onInstalled.addListener(function() {
    chrome.contextMenus.create({
        id: "summarizeSelection",
        title: "Summarize selected text",
        contexts: ["selection"]
    });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(function(info, tab) {
    if (info.menuItemId === "summarizeSelection") {
        // Get selected text and open popup
        chrome.tabs.sendMessage(tab.id, {action: 'summarizeSelection'});
    }
});

// Handle messages from popup and content scripts
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'summarize') {
        handleSummarization(request, sendResponse);
        return true; // Will respond asynchronously
    } else if (request.action === 'summarizeJson') {
        handleJsonSummarization(request, sendResponse);
        return true; // Will respond asynchronously
    } else if (request.action === 'openPopupWithText') {
        // Store text for popup to access
        chrome.storage.local.set({'selectedTextForPopup': request.text});
    }
});

// Handle text summarization
async function handleSummarization(request, sendResponse) {
    try {
        const { text, compression, apiKey } = request;
        
        // Build prompt based on compression ratio
        let prompt;
        if (compression === '25%') {
            prompt = `Summarize the following text to 25% of its original length. Keep only the most essential information:\n\n${text}`;
        } else if (compression === '50%') {
            prompt = `Summarize the following text to 50% of its original length. Maintain key points and important details:\n\n${text}`;
        } else if (compression === '75%') {
            prompt = `Summarize the following text to 75% of its original length. Preserve most details while making it more concise:\n\n${text}`;
        } else {
            prompt = `Create a clear and concise summary of the following text, maintaining all important information:\n\n${text}`;
        }
        
        const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=' + apiKey, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }]
            })
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.candidates && data.candidates[0] && data.candidates[0].content) {
            let summary = data.candidates[0].content.parts[0].text;
            // Clean up formatting
            summary = summary.replace(/\*/g, '').replace(/#/g, '');
            sendResponse({ success: true, summary: summary });
        } else {
            throw new Error('No summary generated');
        }
        
    } catch (error) {
        console.error('Summarization error:', error);
        sendResponse({ success: false, error: error.message });
    }
}

// Handle JSON summarization
async function handleJsonSummarization(request, sendResponse) {
    try {
        const { jsonData, apiKey } = request;
        
        // Group messages by thread_id
        const threadGroups = {};
        jsonData.forEach(item => {
            const threadId = item.thread_id;
            const body = item.body || '';
            
            if (threadId !== undefined) {
                if (!threadGroups[threadId]) {
                    threadGroups[threadId] = [];
                }
                threadGroups[threadId].push(body);
            }
        });
        
        const summaries = [];
        
        // Process each thread
        for (const [threadId, bodies] of Object.entries(threadGroups)) {
            const combinedText = bodies.join(' ').trim();
            
            if (combinedText) {
                const prompt = `Summarize this email thread in 60 words or less. Focus on key decisions, actions, and important details. Remove formatting characters and line breaks:\n\n${combinedText}`;
                
                const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=' + apiKey, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: prompt
                            }]
                        }]
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                        let summary = data.candidates[0].content.parts[0].text;
                        summary = summary.replace(/\*/g, '').replace(/#/g, '').replace(/\n/g, ' ');
                        summaries.push({
                            thread_id: threadId,
                            body: summary
                        });
                    }
                }
            }
        }
        
        sendResponse({ success: true, summaries: summaries });
        
    } catch (error) {
        console.error('JSON summarization error:', error);
        sendResponse({ success: false, error: error.message });
    }
}