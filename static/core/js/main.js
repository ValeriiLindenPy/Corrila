// scroll-bar

window.addEventListener('scroll', (e) => {
  const nav = document.querySelector('.navbar');
  if (window.pageYOffset > 0) {
    nav.classList.add("add-shadow");
  } else {
    nav.classList.remove("add-shadow");
  }
});

// upload-logic

function uploadFile() {
  var form = document.getElementById("upload-form");
  var formData = new FormData(form);
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload/', true);
  xhr.onload = function () {
    if (xhr.status === 200) {
      alert('File uploaded successfully.');
    } else {
      alert('Error uploading file.');
    }
  };
  xhr.send(formData);
}

var dropZone = document.getElementById('drop-zone');
dropZone.addEventListener('dragover', function (e) {
  e.preventDefault();
  this.classList.add('dragover');
  dropZone.style.border = '4px solid #009578';
});
dropZone.addEventListener('dragleave', function () {
  this.classList.remove('dragover');
  dropZone.style.border = '4px dashed #009578';
});
dropZone.addEventListener('drop', function (e) {
  e.preventDefault();
  this.classList.remove('dragover');
  var files = e.dataTransfer.files;
  var inputField = document.getElementById('real-file');
  var customText = document.getElementById('custom-text');
  inputField.files = files;

  customText.innerHTML = inputField.files[0].name;
});

const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");

customBtn.addEventListener("click", function () {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", function () {
  if (realFileBtn.value) {
    customTxt.innerHTML = realFileBtn.value.match(
      /[\/\\]([\w\d\s\.\-\(\)]+)$/
    )[1];
  } else {
    customTxt.innerHTML = "No file chosen, yet.";
  }
});