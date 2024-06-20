# Usa una imagen base que soporte Python y puedas personalizar
FROM python:3.11

# Instala las dependencias del sistema necesarias (ejemplo para Ubuntu)
RUN apt-get update \
    && apt-get install -y \
        unixodbc \
        unixodbc-dev \
        odbcinst \
        freetds-bin \
        tdsodbc

# Configura el directorio de trabajo de la aplicación
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . .

# Instala las dependencias de Python (requerimientos de tu aplicación)
RUN pip install -r requirements.txt

# Comando para iniciar tu aplicación (ajústalo según cómo inicies tu aplicación)
CMD ["gunicorn", "main:crear_app()"]