function togglePassword(){
    password = document.getElementById('password');
    if (password.type === 'password'){
        password.type = 'text';
    } else {
        password.type = 'password';
    }
}

checkbox = document.getElementById("show");
checkbox.addEventListener('click', togglePassword);

