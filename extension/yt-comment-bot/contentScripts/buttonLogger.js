document.addEventListener('click', (event) => {
    if (event.target.classList.contains('reply-button')) {
        console.log('Reply button clicked');
    } else if (event.target.classList.contains('delete-button')) {
        console.log('Delete button clicked');
    }
});
