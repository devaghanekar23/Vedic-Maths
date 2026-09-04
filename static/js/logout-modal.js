function openLogoutModal(event) {
    event.preventDefault();
    const overlay = document.getElementById('logoutModalOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function closeLogoutModal() {
    const overlay = document.getElementById('logoutModalOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'logoutModalOverlay') {
        closeLogoutModal();
    }
});