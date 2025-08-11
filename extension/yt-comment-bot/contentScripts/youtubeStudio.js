// Refactored waitForElement to return a Promise
function waitForElement(selector) {
    return new Promise(resolve => {
        const element = document.querySelector(selector);
        if (element) {
            resolve(element);
        } else {
            const observer = new MutationObserver(() => {
                const element = document.querySelector(selector);
                if (element) {
                    resolve(element);
                    observer.disconnect();
                }
            });
            observer.observe(document.documentElement, {
                childList: true,
                subtree: true
            });
        }
    });
}

// New helper function: wait for an element within a given container
function waitForElementWithin(container, selector) {
    return new Promise(resolve => {
        const element = container.querySelector(selector);
        if (element) {
            resolve(element);
        } else {
            const observer = new MutationObserver(() => {
                const el = container.querySelector(selector);
                if (el) {
                    resolve(el);
                    observer.disconnect();
                }
            });
            observer.observe(container, {
                childList: true,
                subtree: true
            });
        }
    });
}

// Updated addCustomButton function to handle dropdown and delete in one click
function addCustomButton(commentElement) {
    const actionsContainer = commentElement.querySelector('#comment-actions');
    if (actionsContainer && !actionsContainer.querySelector('.custom-footer-button')) {
        actionsContainer.insertAdjacentHTML('beforeend', `
            <button class="custom-footer-button ytcp-button-shape-impl ytcp-button-shape-impl--tonal">Delete This Comment</button>
        `);
        const customBtn = actionsContainer.querySelector('.custom-footer-button');
        customBtn.addEventListener('click', async () => {
            // Log the index of the comment among all comment elements.
            const allComments = Array.from(document.querySelectorAll('ytcp-comment'));
            const commentIndex = allComments.indexOf(commentElement);

            try {
                // Click the action menu button
                const actionMenuButton = commentElement.querySelector('#action-menu-button');
                if (actionMenuButton) {
                    actionMenuButton.click();
                    const deleteMenuItem = await waitForElementWithin(
                        document.body,
                        'tp-yt-paper-item.style-scope.ytcp-menu-service-item-renderer[role="option"]'
                    );
                    if (deleteMenuItem) {
                        deleteMenuItem.click();
                    }
                }
            } catch (error) {
                // Error handling
            }
        });
    }
}

// Function to extract text content from comment
function getCommentText(element) {
    return Array.from(element.childNodes).map(node => {
        if (node.nodeType === Node.TEXT_NODE) { return node.textContent; }
        if (node.tagName === 'SPAN') { return node.textContent; }
        if (node.tagName === 'IMG') { return node.getAttribute('alt') || ''; }
        return '';
    }).join('').trim();
}

// New helper function to request reply from server using comment text
function getServerReply(commentText) {
    return fetch('http://127.0.0.1:65432', {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: commentText
    }).then(response => response.text());
}

function processItems(itemsDiv) {
    Array.from(itemsDiv.children).forEach((child, index) => {
        // Get and print comment text
        const commentElement = child.querySelector('yt-formatted-string#content-text');
        let commentText = "";
        if (commentElement) {
            commentText = getCommentText(commentElement);
        }

        // Auto-click reply button with stagger delay
        const nativeReply = child.querySelector("button[aria-label='Reply']");
        if (nativeReply) {
            setTimeout(() => {
                nativeReply.click();
                getServerReply(commentText).then(serverReply => {
                    waitForElementWithin(child, "textarea#textarea.style-scope.tp-yt-iron-autogrow-textarea")
                        .then(textarea => {
                            chrome.storage.local.get(["contactInfo"], function (data) {
                                const contact = data.contactInfo || '';
                                textarea.value = serverReply + ' ' + contact;
                                textarea.dispatchEvent(new Event('input', { bubbles: true }));
                                console.log(`Reply updated for comment index ${index}`);
                            });
                        });
                });
            }, index * 10);
        }
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    // Create observer for reply dialogs
    const replyDialogObserver = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1 && node.tagName === 'YTCP-COMMENT') {
                    addCustomButton(node);
                }
            });
        });
    });

    // Watch for comment elements
    replyDialogObserver.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Await items container and process items after delay
    const itemsDiv = await waitForElement('#items.style-scope.tp-yt-iron-list');
    setTimeout(() => {
        processItems(itemsDiv);
    }, 5000);
    console.log("Extension initialized");
});
