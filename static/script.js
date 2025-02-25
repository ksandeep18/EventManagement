document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 3000);
    });
});
