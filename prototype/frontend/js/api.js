const API_URL = 'http://localhost:8000';

async function apiCall(endpoint, method = 'GET', body = null, requireAuth = true) {
    const headers = {
        'Content-Type': 'application/json'
    };

    if (requireAuth) {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
    };

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        if (response.status === 401 && requireAuth) {
            localStorage.removeItem('token');
            window.location.href = 'login.html';
            return;
        }
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Something went wrong');
        }
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
