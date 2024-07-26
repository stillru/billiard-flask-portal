async function register(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });

        if (!response.ok) {
            throw new Error('Failed to connect to the backend.');
        }

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            window.location.href = '/login';
        } else {
            alert(result.error);
        }
    } catch (error) {
        window.location.href = `/error?message=${encodeURIComponent(error.message)}`;
    }
}
