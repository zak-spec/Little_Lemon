FROM python:3.11-slim

# Evita que Python cree archivos pyc y habilita el buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las dependencias del sistema necesarias (incluyendo para mysqlclient)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y luego instala las dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo el código del proyecto
COPY . /app/

# Expone el puerto 8000 (puerto por defecto de Django)
EXPOSE 8000

# Comando para correr el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
