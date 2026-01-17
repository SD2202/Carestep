async function loadBookingHistory() {
    const historyList = document.getElementById('history-list');
    if (!historyList) return;

    try {
        const bookings = await apiCall('/bookings/history');
        if (bookings.length === 0) {
            historyList.innerHTML = '<p class="text-gray-500 italic">No bookings found.</p>';
            return;
        }

        historyList.innerHTML = bookings.map(booking => `
            <div onclick="window.location.href='booking-details.html?id=${booking.id}'" 
                class="bg-white p-4 rounded-lg border border-gray-100 shadow-sm flex justify-between items-center cursor-pointer hover:border-blue-300 hover:shadow-md transition">
                <div>
                    <h4 class="font-semibold text-healthcare-dark">${booking.service ? booking.service.name : 'Unknown Service'}</h4>
                    <p class="text-sm text-gray-600">Date: ${new Date(booking.scheduled_date).toLocaleDateString()}</p>
                    <p class="text-xs text-gray-500">${booking.address}</p>
                </div>
                <div>
                    <span class="px-3 py-1 rounded-full text-xs font-medium 
                        ${getStatusClass(booking.status)}">
                        ${booking.status}
                    </span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        historyList.innerHTML = '<p class="text-red-500">Failed to load booking history.</p>';
    }
}

async function updateProfile(event) {
    if (event) event.preventDefault();
    const fullName = document.getElementById('edit-name').value;
    const phone = document.getElementById('edit-phone').value;
    const address = document.getElementById('edit-address').value;
    const statusMsg = document.getElementById('settings-status');

    try {
        await apiCall('/users/me', 'PUT', {
            full_name: fullName,
            phone: phone,
            address: address
        });
        statusMsg.textContent = 'Profile updated successfully!';
        statusMsg.className = 'text-green-600 text-sm mt-2';
        setTimeout(() => statusMsg.textContent = '', 3000);
        // Refresh profile data in UI
        if (typeof loadProfile === 'function') loadProfile();
    } catch (err) {
        statusMsg.textContent = err.message || 'Update failed';
        statusMsg.className = 'text-red-600 text-sm mt-2';
    }
}

// Function to populate settings form
async function populateSettingsForm() {
    try {
        const user = await apiCall('/users/me');
        const nameInput = document.getElementById('edit-name');
        const phoneInput = document.getElementById('edit-phone');
        const addressInput = document.getElementById('edit-address');

        if (nameInput) nameInput.value = user.full_name || '';
        if (phoneInput) phoneInput.value = user.phone || '';
        if (addressInput) addressInput.value = user.address || '';
    } catch (err) {
        console.error("Failed to fetch profile for settings", err);
    }
}

function getStatusClass(status) {
    if (!status) return 'bg-gray-100 text-gray-800';
    switch (status.toLowerCase()) {
        case 'pending': return 'bg-yellow-100 text-yellow-800';
        case 'confirmed': return 'bg-blue-100 text-blue-800';
        case 'arrived': return 'bg-purple-100 text-purple-800';
        case 'completed': return 'bg-green-100 text-green-800';
        case 'cancelled': return 'bg-red-100 text-red-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}
