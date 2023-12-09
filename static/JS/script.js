function togglePasswordVisibility(passwordInputId) {
    const passwordInput = document.getElementById(passwordInputId);
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Change eye icon based on password visibility
    const eyeIcon = document.querySelector('.toggle-password img');
    eyeIcon.src = type === 'password' ?
        '/static/images/Eye.svg' :
        '/static/images/Eye-off.svg';
}

document.addEventListener('DOMContentLoaded', function () {
    // Your other DOMContentLoaded code here, if any
});
