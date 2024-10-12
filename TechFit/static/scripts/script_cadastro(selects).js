const studentInputs = document.getElementById('student-inputs');
    const personalInputs = document.getElementById('personal-inputs');
    const userTypeRadios = document.querySelectorAll('input[name="user-type"]');

    userTypeRadios.forEach(radio => {
      radio.addEventListener('change', () => {
        // Oculta ambos os inputs ao mudar o tipo
        studentInputs.style.display = 'none';
        personalInputs.style.display = 'none';

        if (document.getElementById('user-student').checked) {
          studentInputs.style.display = 'flex'; // Exibe os inputs de aluno
        } else if (document.getElementById('user-personal').checked) {
          personalInputs.style.display = 'flex'; // Exibe os inputs de personal
        }
      });
    });
