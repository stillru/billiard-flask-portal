document.addEventListener('DOMContentLoaded', function() {
    // Функция для отображения тоста
    function showToast(message) {
        const toast = document.getElementById('newsToast');
        toast.querySelector('.toast-body').textContent = message;
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    // Сохранение состояния уведомления в localStorage
    function saveToastMessage(message) {
        localStorage.setItem('toastMessage', message);
    }

    const form = document.getElementById('news-form');
    const tagsSelect = document.getElementById('tags');

    // Получаем теги с бэкенда
    fetch('http://localhost:5000/api/tags')
        .then(response => response.json())
        .then(tags => {
            tags.data.forEach(tag => {
                const option = document.createElement('option');
                option.value = tag.id;
                option.textContent = tag.name;
                tagsSelect.appendChild(option);
            });
        });

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            title: formData.get('title'),
            body: formData.get('body'),
            source_type: formData.get('source_type'),
            source_id: formData.get('source_id'),
            tags: Array.from(formData.getAll('tags'))
        };

        fetch('http://localhost:5000/api/news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log(result.status);
            saveToastMessage('Новость успешно добавлена!');
            window.location.href = '/'; // Перенаправление на главную страницу
            })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
