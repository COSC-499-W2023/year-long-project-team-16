// Utility function to handle HTTP requests
async function fetchData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    return await response.json();
}

// Register function
async function handleRegister(event) {
    event.preventDefault();

    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match. Please try again.');
        return;
    }

    try {
        const data = await fetchData('//http://localhost:3001/register.html', { fullName, email, password });
        if (data.message) {
            alert('Registration successful');
            window.location.href = 'login.html';
        } else {
            alert('Registration failed. Please try again.');
        }
    } catch (error) {
        alert('An error occurred. Please try again later.');
    }
}

// Login function
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const data = await fetchData('http://localhost:3001/login', { email, password });
        if (data.token) {
            localStorage.setItem('token', data.token);
            alert('Login successful');
            window.location.href = 'index.html';
        } else {
            alert('Login failed. Please check your credentials.');
        }
    } catch (error) {
        alert('An error occurred. Please try again later.');
    }
}

// Event listeners
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', handleRegister);
}

const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}
