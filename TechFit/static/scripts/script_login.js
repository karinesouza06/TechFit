
document.addEventListener('DOMContentLoaded', () => {
    const validarButton = document.getElementById('validar_button');

    validarButton.addEventListener('click', () => {
        const nomeInput = document.getElementById('inputNome');
        const senhaInput = document.getElementById('inputPassword5');

        const nome = nomeInput.value.trim();
        const senha = senhaInput.value.trim();

        const nomeError = validateName(nome, nomeInput);
        const senhaError = validatePassword(senha, senhaInput);

        if (nomeError) {
            nomeInput.style.border = '2px solid red';
        } else {
            nomeInput.style.border = '2px solid green';
        }

        if (senhaError) {
            senhaInput.style.border = '2px solid red';
        } else {
            senhaInput.style.border = '2px solid green';
        }

        if (!nomeError && !senhaError) {
           // document.location.href = "{{url_for('static', filename='scripts/inicial.html')}}";
           document.location.href = "http://127.0.0.1:5000/ "
            
        }
    });

    function validateName(name) {
        if (!name) {
            return 'Nome é obrigatório.';
        }

        if (name.length < 3) {
            return 'O nome deve ser maior que 3 caracteres.';
        }

        const invalidChars = /[^a-zA-Z\s]/;
        if (invalidChars.test(name)) {
            return 'Nome não pode conter números, caracteres especiais ou emojis.';
        }
        return '';
    }

    function validatePassword(password) {
        if (!password) {
            return 'Senha é obrigatória.';
        }
        if (password.length < 8 || password.length > 20) {
            return 'Senha deve ter de 8 a 20 caracteres.';
        }

        return '';
    }
});