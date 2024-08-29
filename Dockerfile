# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos a la carpeta de la aplicación
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto al contenedor
COPY . .

# Exponer el puerto en el que se ejecuta la aplicación FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
