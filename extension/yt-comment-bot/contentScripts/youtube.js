// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create a new div element
    const newDiv = document.createElement('div');
    newDiv.innerHTML = `
        <div style="position: fixed; top: 10px; right: 10px; background: white; border: 1px solid black; padding: 10px; z-index: 1000;">
            <h3>Injected Content</h3>
            <p>This content was injected by the extension.</p>
        </div>
    `;
    // Append the new div to the body
    document.body.appendChild(newDiv);
});
