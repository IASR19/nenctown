const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');
const submitButton = document.getElementById('submitButton');
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const resultDiv = document.getElementById('result');
const interface1 = document.getElementById('interface1');
const interface2 = document.getElementById('interface2');
const emotionResult = document.getElementById('emotionResult');
const backButton = document.getElementById('backButton');
const captureIndicator = document.getElementById('captureIndicator');
const progressIndicator = document.getElementById('progressIndicator');
let capturedImageBlob = null;

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Erro ao acessar a câmera: ", err);
    });

captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        capturedImageBlob = blob;
        captureIndicator.style.display = 'block';
        submitButton.style.display = 'inline-block';
    }, 'image/jpeg');
});

submitButton.addEventListener('click', () => {
    const formData = new FormData();
    formData.append('file', capturedImageBlob, 'photo.jpg');

    progressIndicator.style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            progressIndicator.style.display = 'none';
            resultDiv.textContent = `Erro: ${result.error}`;
        } else {
            analyzeImage(result.filename);
        }
    })
    .catch(error => {
        progressIndicator.style.display = 'none';
        console.error('Erro:', error);
        resultDiv.textContent = `Erro: ${error}`;
    });
});

uploadForm.addEventListener('submit', event => {
    event.preventDefault();
    const formData = new FormData(uploadForm);

    progressIndicator.style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            progressIndicator.style.display = 'none';
            resultDiv.textContent = `Erro: ${result.error}`;
        } else {
            analyzeImage(result.filename);
        }
    })
    .catch(error => {
        progressIndicator.style.display = 'none';
        console.error('Erro:', error);
        resultDiv.textContent = `Erro: ${error}`;
    });
});

function analyzeImage(filename) {
    fetch(`/analyze/${filename}`)
    .then(response => response.json())
    .then(result => {
        progressIndicator.style.display = 'none';
        if (result.error) {
            resultDiv.textContent = `Erro: ${result.error}`;
        } else {
            emotionResult.textContent = `Emoção Detectada: ${result.emotion}`;
            interface1.style.display = 'none';
            interface2.style.display = 'block';
        }
    })
    .catch(error => {
        progressIndicator.style.display = 'none';
        console.error('Erro:', error);
        resultDiv.textContent = `Erro: ${error}`;
    });
}

backButton.addEventListener('click', () => {
    interface1.style.display = 'block';
    interface2.style.display = 'none';
    resultDiv.textContent = '';
    emotionResult.textContent = '';
    captureIndicator.style.display = 'none';
    submitButton.style.display = 'none';
});
