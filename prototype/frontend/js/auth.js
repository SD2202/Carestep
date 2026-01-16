function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

function isLoggedIn() {
    return localStorage.getItem('token') !== null;
}

function updateAuthUI() {
    const authButtons = document.getElementById('auth-buttons');
    if (!authButtons) return;

    if (isLoggedIn()) {
        authButtons.innerHTML = `
            <a href="dashboard.html" class="nav-link">Dashboard</a>
            <button onclick="logout()" class="btn-secondary px-3 py-1">Logout</button>
        `;
    }
}

// Auto-run UI update on pages with auth-buttons
document.addEventListener('DOMContentLoaded', updateAuthUI);
