# Emotion Analysis Application

## Descrição
Este é um sistema de análise de emoções que permite aos usuários tirar fotos com a webcam ou fazer upload de imagens para detectar emoções. As emoções detectadas são traduzidas para o português e exibidas na interface.


## Pré-requisitos

- Python 3.9 ou superior
- pip (Python package installer)

## Instruções para Rodar a Aplicação

### Configuração

1. **Clone o repositório**

2. **Crie e ative um ambiente virtual**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o servidor Flask**
    ```bash
    python3 app.py
    ```

Rodando em [http://127.0.0.1:5000](http://127.0.0.1:5000).

4. **Ngrok é uma ferramenta que cria um túnel seguro de HTTP a partir de uma URL pública HTTPS para um servidor web rodando localmente.**
    ```bash
    ngrok http 5000
    ```

## Funcionalidades

1. **Capturar Foto pela Webcam**
    - Clique em "Capture Photo" para tirar uma foto usando a webcam.
    - Após capturar a foto, um botão "Analyze Photo" aparecerá. Clique nele para enviar a foto para análise.

2. **Fazer Upload de Imagem**
    - Clique em "Choose File" para selecionar uma imagem do seu computador.
    - Após selecionar a imagem, um botão "Analyze Photo" aparecerá. Clique nele para enviar a imagem para análise.

3. **Ver Resultado da Análise**
    - O resultado da análise será exibido em uma caixa de diálogo indicando a emoção detectada em português.

## Dependências

- Flask
- Werkzeug
- DeepFace
- TensorFlow
- OpenCV

## Observações

- Certifique-se de que o diretório `uploads/` existe no diretório `emotion-analysis-backend`. Se não existir, crie-o manualmente.
- Se houver problemas com permissões ou outras questões ao rodar o servidor, tente executar o terminal com permissões de administrador.

## Autor

- Desenvolvido por Itamar Ribeiro



