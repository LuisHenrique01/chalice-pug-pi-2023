FROM python:3.9-slim-buster

# Instalação de dependências
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    netcat

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código para o diretório de trabalho
COPY . /app

# Expõe a porta 8000
EXPOSE 8000

# Define o comando a ser executado quando o contêiner for iniciado
CMD ["chalice", "local", "--host", "0.0.0.0"]
