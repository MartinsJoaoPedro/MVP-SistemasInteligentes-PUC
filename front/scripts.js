/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/

const getList = async () => {
  let url = 'http://127.0.0.1:5000/pacientes';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);  // Imprime o JSON no console
      data.pacientes.forEach(item => insertList(item.id,
        item.idade,
        item.leucocitos,
        item.basofilos,
        item.creatinina,
        item.proteina_c,
        item.hemoglobina,
        item.rt_pcr
      ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputIdade, inputLeucocitos, inputBasofilos, inputCreatinina, inputProteinaC, inputHemoglobina) => {

  const formData = new FormData();
  formData.append('idade', inputIdade);
  formData.append('leucocitos', inputLeucocitos);
  formData.append('basofilos', inputBasofilos);
  formData.append('creatinina', inputCreatinina);
  formData.append('proteina_c', inputProteinaC);
  formData.append('hemoglobina', inputHemoglobina);

  let url = 'http://127.0.0.1:5000/paciente';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const idItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(idItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/paciente?id=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputIdade = document.getElementById("newIdade").value;
  let inputLeucocitos = document.getElementById("newLeucocitos").value;
  let inputBasofilos = document.getElementById("newBasofilos").value;
  let inputCreatinina = document.getElementById("newCreatinina").value;
  let inputProteinaC = document.getElementById("newProteina").value;
  let inputHemoglobina = document.getElementById("newHemoglobina").value;

  if (inputIdade === '' || inputLeucocitos === '' || inputBasofilos === '' || inputCreatinina === '' || inputProteinaC === '' || inputHemoglobina === '') {
    alert("Esse(s) campo(s) não podem ser vazio!");
  } else if (isNaN(inputIdade) || isNaN(inputLeucocitos) || isNaN(inputBasofilos) || isNaN(inputCreatinina) || isNaN(inputProteinaC) || isNaN(inputHemoglobina)) {
    alert("Esse(s) campo(s) precisam ser números!");
  } else {
    postItem(inputIdade, inputLeucocitos, inputBasofilos, inputCreatinina, inputProteinaC, inputHemoglobina);
    alert("Item adicionado!");
  }

}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (Id, Idade, Leucocitos, Basofilos, Creatinina, ProteinaC, Hemoglobina, Diagnostico) => {
  var item = [Id, Idade, Leucocitos, Basofilos, Creatinina, ProteinaC, Hemoglobina, Diagnostico];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);


  document.getElementById("newIdade").value = "";
  document.getElementById("newLeucocitos").value = "";
  document.getElementById("newBasofilos").value = "";
  document.getElementById("newCreatinina").value = "";
  document.getElementById("newProteina").value = "";
  document.getElementById("newHemoglobina").value = "";

  removeElement();
}