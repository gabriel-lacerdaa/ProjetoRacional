const fileInput = document.getElementsByClassName('file-input')[0];
const imagem = document.getElementsByClassName('img-padrao')[0];

// Função para lidar com a alteração de imagem
//Essa função serve para quando alterar a imagem, alterar automaticamente no html
function handleImageChange(e) {
  const arquivo = e.target.files[0];

  if (!arquivo.type.match('image/jpeg')) {
    alert('Somente arquivos do tipo JPEG (.jpg) são aceitos!');
    return;
  }

  const reader = new FileReader();

  reader.onload = function(event) {
    imagem.src = event.target.result;
  }

  reader.readAsDataURL(arquivo);
}

// Remover o evento de escuta se já existir
if (fileInput) {
  fileInput.removeEventListener('change', handleImageChange);
  fileInput.addEventListener('change', handleImageChange);
}
