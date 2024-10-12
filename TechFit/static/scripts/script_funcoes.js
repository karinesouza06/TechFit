// Abrir modal
const modal = document.getElementById("modal");
const openModal = document.getElementById("openModal");
const closeModal = document.querySelector(".close");

openModal.onclick = function() {
    modal.style.display = "block";
}

// Fechar modal
closeModal.onclick = function() {
    modal.style.display = "none";
}

// Fechar modal ao clicar fora dele
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

const form = document.getElementById('form');
form.addEventListener('submit', function(event) {
    /* Previne o comportamento padrão do evento submit do JS, ou seja,
    impede o recarregamento da página */
    event.preventDefault();

    /* Pegando as informações informadas no forms no arquivo index.html */
    const peso = document.getElementById('peso').value;
    const altura = document.getElementById('altura').value;
    

    /* Calculo do IMC */
    const bmi = (peso / (altura * altura)).toFixed(2);

    if (!isNaN(bmi)) {
        const value = document.getElementById('value');
        let description = '';

        value.classList.add('attention');
        
        document.getElementById('infos').classList.remove('hidden');
        
        /* Analisando o valor do IMC e retornando uma mensagem expecífica de acordo com tal valor (Essa parte de exibir mensagem pode ser retirada) */
        if (bmi < 18.5){
            description = 'Cuidado! Você está abaixo do peso!';
        } 

        else if (bmi >= 18.5 && bmi <= 25) {
            description = "Você está no peso ideal!";
            value.classList.remove('attention');
            value.classList.add('normal');
        }

        else if (bmi > 25 && bmi <= 30) {
            description = "Cuidado! Você está com sobrepeso!";
        }

        else if (bmi > 30 && bmi <= 35) {
            description = "Cuidado! Você está com obesidade moderada!";
        }

        else if (bmi > 35 && bmi <= 40) {
            description = "Cuidado! Você está com obesidade severa!";
        }

        else {
            description = "Cuidado! Você está com obesidade morbida!";
        }

        value.textContent = bmi.replace('.', ',');
        document.getElementById('description').textContent = description;
    }
});


form.addEventListener('keypress', function(event) {
    if (event.key === 'press') {
        document.getElementById('#calculate').click();
    }
});

let totalLitros = 0; // Variável para armazenar o total de litros

function somar_agua() {

    document.getElementById('infos2').classList.remove('hidden')
    const input = document.getElementById('qtd_agua'); // Captura o valor do input
    const valor = parseFloat(input.value); // Converte o valor do input para float

    if (!isNaN(valor) && valor > 0) { // Verifica se o valor é um número válido e maior que 0
        totalLitros += valor; // Adiciona o valor ao total de litros
        input.value = ''; // Limpa o input após adicionar o valor
    } else {
        alert("Por favor, insira um valor válido de litros.");
    }

    // Exibe o total de litros
    document.getElementById('value').textContent = totalLitros.toFixed(2);
};
