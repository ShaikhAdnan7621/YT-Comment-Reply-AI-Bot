document.getElementById('clickMe').addEventListener('click', () => {
    alert('Button Clicked!');
});

document.getElementById('saveContact').addEventListener('click', () => {
    const contact = document.getElementById('contactInfo').value.trim();
    chrome.storage.local.set({ contactInfo: contact }, () => {
        console.log('Contact saved');
    });
});
