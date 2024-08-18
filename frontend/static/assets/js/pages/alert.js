document.addEventListener('DOMContentLoaded', function() {
    function showToast(message) {
        const toast = document.getElementById('newsToast');
        toast.querySelector('.toast-body').textContent = message;
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    // Чтение сообщения из localStorage
    const toastMessage = localStorage.getItem('toastMessage');
    if (toastMessage) {
        showToast(toastMessage);
        localStorage.removeItem('toastMessage'); // Удаление сообщения после показа
    }
});
