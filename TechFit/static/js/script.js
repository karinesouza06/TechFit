/* Script do carrossel */
let currentSlide = 0;
const slides = document.querySelector(".carousel-images");
const totalSlides = document.querySelectorAll(".carousel-image").length;

function moveSlide(direction) {
  currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
  slides.style.transform = `translateX(-${currentSlide * 100}%)`;
}

function goToSlide(index) {
  currentSlide = index;
  slides.style.transform = `translateX(-${currentSlide * 100}%)`;
}

// Touch events para mobile
let touchStartX = 0;
let touchEndX = 0;

slides.addEventListener("touchstart", (e) => {
  touchStartX = e.changedTouches[0].screenX;
});

slides.addEventListener("touchend", (e) => {
  touchEndX = e.changedTouches[0].screenX;
  if (touchStartX - touchEndX > 50) moveSlide(1);
  if (touchEndX - touchStartX > 50) moveSlide(-1);
});

// Auto-rotate opcional
let autoRotate = setInterval(() => moveSlide(1), 5000);

// Pausa auto-rotate ao interagir
document.querySelectorAll(".carousel-button").forEach((element) => {
  element.addEventListener("click", () => {
    clearInterval(autoRotate);
    autoRotate = setInterval(() => moveSlide(1), 5000);
  });
});

// CADASTRO
document.addEventListener("DOMContentLoaded", () => {
  const tipoUsuario = document.getElementById("tipoUsuario");
  const alunoFields = document.querySelector(".aluno-fields");
  const personalFields = document.querySelector(".personal-fields");

  tipoUsuario.addEventListener("change", () => {
    const value = tipoUsuario.value;
    alunoFields.classList.add("hidden");
    personalFields.classList.add("hidden");

    if (value === "aluno") {
      alunoFields.classList.remove("hidden");
      alunoFields
        .querySelectorAll("select, input")
        .forEach((el) => (el.required = true));
    } else if (value === "personal") {
      personalFields.classList.remove("hidden");
      personalFields
        .querySelectorAll("select, input")
        .forEach((el) => (el.required = true));
    }
  });

    document.getElementById('cadastroForm').addEventListener('submit', function(e) {
      e.preventDefault();
      let isValid = true;
      
      // Resetar erros
      document.querySelectorAll('.text-red-500').forEach(el => {
          el.classList.add('hidden');
      });
  
      // Validação básica
      const camposObrigatorios = [
          'nome', 'email', 'telefone', 'nascimento', 
          'senha', 'confirmarSenha', 'genero', 'tipoUsuario'
      ];
  
      camposObrigatorios.forEach(id => {
          const input = document.getElementById(id);
          if(!input.value.trim()) {
              showError(id, 'Campo obrigatório');
              isValid = false;
          }
      });
  
      // Validação específica
      if(!/^\d{11}$/.test(document.getElementById('telefone').value)) {
          showError('telefone', 'Telefone inválido (11 dígitos)');
          isValid = false;
      }
  
      if(document.getElementById('senha').value !== document.getElementById('confirmarSenha').value) {
          showError('confirmarSenha', 'Senhas não coincidem');
          isValid = false;
      }
  
      // Validação campos condicionais
      const tipo = document.getElementById('tipoUsuario').value;
      if(tipo === 'aluno') {
          ['dias_treino', 'horario_treino'].forEach(id => {
              if(!document.getElementById(id).value) {
                  showError(id, 'Campo obrigatório');
                  isValid = false;
              }
          });
      }
      else if(tipo === 'personal') {
          ['dias_trabalho', 'horario_trabalho'].forEach(id => {
              if(!document.getElementById(id).value) {
                  showError(id, 'Campo obrigatório');
                  isValid = false;
              }
          });
      }
  
      if(isValid) {
          // SUBMETER VIA AJAX (exemplo com Fetch API)
          const formData = new FormData(this);
          
          fetch(this.action, {
              method: 'POST',
              body: formData
          })
          .then(response => {
              if(response.ok) {
                  // Mostrar modal de login após cadastro
                  document.getElementById('modal-1').showModal();
                  this.reset();
                  document.querySelector('.aluno-fields').classList.add('hidden');
                  document.querySelector('.personal-fields').classList.add('hidden');
              }
          })
          .catch(error => {
              console.error('Erro:', error);
          });
      }
  });

  function showError(fieldId, message) {
    const errorElement = document.getElementById(`${fieldId}Error`);
    errorElement.textContent = message;
    errorElement.classList.remove("hidden");
  }
});

document.getElementById("tipoUsuario").addEventListener("change", function () {
  const tipo = this.value;
  document
    .querySelectorAll(".aluno-fields, .personal-fields")
    .forEach((div) => {
      div.classList.add("hidden");
      div
        .querySelectorAll("[required]")
        .forEach((input) => input.removeAttribute("required"));
    });

  if (tipo === "aluno") {
    document.querySelector(".aluno-fields").classList.remove("hidden");
    document
      .querySelectorAll(".aluno-fields [required]")
      .forEach((input) => input.setAttribute("required", true));
  } else if (tipo === "personal") {
    document.querySelector(".personal-fields").classList.remove("hidden");
    document
      .querySelectorAll(".personal-fields [required]")
      .forEach((input) => input.setAttribute("required", true));
  }
});

// Função para alternar a visibilidade da senha
function togglePasswordVisibility(inputId, buttonId, iconId) {
  const passwordInput = document.getElementById(inputId);
  const toggleButton = document.getElementById(buttonId);
  const toggleIcon = document.getElementById(iconId);

  toggleButton.addEventListener('click', function () {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      
      // Altera o ícone com base no tipo de input
      if (type === 'password') {
          toggleIcon.src = 'static/images/icons/olho_aberto_preto.png'; // Ícone de olho aberto
      } else {
          toggleIcon.src = 'static/images/icons/olho_fechado_preto.png'; // Ícone de olho fechado
      }
  });
}

// Aplicar a função para o campo de senha do login
togglePasswordVisibility('password', 'togglePasswordLogin', 'togglePasswordIconLogin');

// Aplicar a função para o campo de senha do cadastro
togglePasswordVisibility('senha', 'togglePasswordCadastro', 'togglePasswordIconCadastro');

// Aplicar a função para o campo de confirmação de senha do cadastro
togglePasswordVisibility('confirmarSenha', 'toggleConfirmarSenhaCadastro', 'toggleConfirmarSenhaIconCadastro');

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('#modal-1 form');
    const loginError = document.getElementById('loginError');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Limpa mensagens de erro anteriores
            loginError.textContent = '';
            loginError.classList.remove('show');
            
            // Mostra loading no botão
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            
            try {
                const formData = new FormData(loginForm);
                const response = await fetch(loginForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Login bem-sucedido - redirecionar
                    window.location.href = data.redirect || '/';
                } else {
                    // Mostrar erro
                    loginError.textContent = data.error || 'Email ou senha incorretos';
                    loginError.classList.add('show');
                    
                    // Adiciona shake animation para indicar erro
                    loginForm.classList.add('shake');
                    setTimeout(() => {
                        loginForm.classList.remove('shake');
                    }, 500);
                }
            } catch (error) {
                console.error('Erro:', error);
                loginError.textContent = 'Ocorreu um erro ao tentar fazer login';
                loginError.classList.add('show');
            } finally {
                // Restaura o botão
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        });
    }
});
