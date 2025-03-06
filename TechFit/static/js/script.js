var themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon");
var themeToggleLightIcon = document.getElementById("theme-toggle-light-icon");

if (
  localStorage.getItem("color-theme") === "dark" ||
  (!("color-theme" in localStorage) &&
    window.matchMedia("(prefers-color-scheme: dark)").matches)
) {
  themeToggleLightIcon.classList.remove("hidden");
} else {
  themeToggleDarkIcon.classList.remove("hidden");
}

var themeToggleBtn = document.getElementById("theme-toggle");

themeToggleBtn.addEventListener("click", function () {
  themeToggleDarkIcon.classList.toggle("hidden");
  themeToggleLightIcon.classList.toggle("hidden");

  if (localStorage.getItem("color-theme")) {
    if (localStorage.getItem("color-theme") === "light") {
      document.documentElement.classList.add("dark");
      localStorage.setItem("color-theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("color-theme", "light");
    }
  } else {
    if (document.documentElement.classList.contains("dark")) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("color-theme", "light");
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("color-theme", "dark");
    }
  }
});

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
