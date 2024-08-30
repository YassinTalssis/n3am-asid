document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // For demonstration purposes, let's log the values.
    // In a real application, you would send these values to the server for verification.
    console.log('Email:', email);
    console.log('Password:', password);

    // You can add your authentication logic here.

    // Example: Redirect to the dashboard after successful login
    // window.location.href = 'dashboard.html';
});
