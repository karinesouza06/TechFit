// Seleciona todos os botões que abrem e fecham o modal
const openButtons = document.querySelectorAll('.open-modal');
const closeButtons = document.querySelectorAll('.close-modal');

// Percorre cada botão de abrir e adiciona o evento de click
openButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Pega o id do modal que o botão abre
        const modalId = button.getAttribute('data-modal');

        // Pega o modal pelo id
        const modal = document.getElementById(modalId);

        // Abre o modal
        modal.showModal();
    });
});

// Percorre cada botão de fechar e adiciona o evento de click
closeButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Pega o id do modal que o botão fecha
        const modalId = button.getAttribute('data-modal');

        // Pega o modal pelo id
        const modal = document.getElementById(modalId);

        // Fecha o modal
        modal.close();
    });
});



// Modifique o script_modal_login.js para incluir a validação
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#modal-1 form');
    const emailInput = document.getElementById('email_login'); // estava 'email'
    const passwordInput = document.getElementById('password');
    
    // Função de validação
    const validateForm = () => {
        let isValid = true;
        
        // Validação de email
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
            showError(emailInput, 'Por favor insira um email válido');
            isValid = false;
        }
        
        // Validação de senha
        if (passwordInput.value.length < 6) {
            showError(passwordInput, 'A senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }
        
        return isValid;
    };

    // Mostrar erros
    const showError = (input, message) => {
        const formGroup = input.closest('.input-group');
        const errorMessage = formGroup.querySelector('.error-message');
        formGroup.classList.add('invalid');
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    };

    // Resetar erros
    const resetErrors = () => {
        document.querySelectorAll('.input-group').forEach(group => {
            group.classList.remove('invalid');
            group.querySelector('.error-message').style.display = 'none';
        });
    };

});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#modal-1 form');
    const emailInput = document.getElementById('email_login');
    const passwordInput = document.getElementById('password');

    // Check if there's a flash message to open the modal
    const flashMessage = "{{ get_flashed_messages()|join('') }}"; // Make sure to use Jinja2 to get the flash messages
    if (flashMessage.includes("Cadastro realizado com sucesso")) {
        document.getElementById('modal-1').showModal();
    }

    // Rest of your existing JavaScript...
});

// Fechar modal ao clicar em Cadastre-se
document.querySelector('#modal-1 .register a').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('modal-1').close();
    
    // Opcional: Rolagem suave para a seção de cadastro
    document.querySelector('#cadastro').scrollIntoView({
        behavior: 'smooth'
    });
});