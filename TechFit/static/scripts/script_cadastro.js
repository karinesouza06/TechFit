document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    const form = event.target;
    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;

    // Validação da senha
    if (password !== confirmPassword) {
        alert('As senhas não coincidem.');
        return;
    }

    // Validação do telefone com expressão regular
    const phone = form.phone.value;
    const phonePattern = /^\(\d{2}\) \d{4}-\d{4}$/;
    if (!phonePattern.test(phone)) {
        alert('Número de telefone inválido. Use o formato (xx) xxxx-xxxx.');
        return;
    }

    // Submete o formulário se todas as validações estiverem corretas
    form.submit();
});

