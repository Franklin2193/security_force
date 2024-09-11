# # Usar una imagen oficial de Ubuntu como imagen base
# FROM ubuntu:22.04

# # Establecer el directorio de trabajo dentro del contenedor
# WORKDIR /app

# # Instalar Python, herramientas de compilación y otras dependencias necesarias
# RUN apt-get update \
#     && apt-get install -y python3 python3-pip python3-venv \
#     && apt-get install -y build-essential libffi-dev libcairo2-dev libsystemd-dev libyaml-dev \
#     && apt-get update && apt-get install -y cmake ninja-build \
#     && apt-get install -y python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Crear un entorno virtual y activarlo
# RUN python3 -m venv venv
# ENV PATH="/app/venv/bin:$PATH"

# # Actualizar pip, setuptools y wheel para evitar problemas de compilación
# RUN pip install --upgrade pip setuptools wheel

# # Instalar Cython mediante pip antes de las demás dependencias
# RUN pip install cython

# # Copiar el archivo de requisitos
# COPY requirements.txt /app/

# # Instalar las dependencias
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el contenido del proyecto al contenedor
# COPY . /app/

# # Exponer el puerto 8000
# EXPOSE 8000

# # Definir el comando para iniciar el servidor
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# # Utilizar la imagen base de Ubuntu
# FROM ubuntu:22.04

# # Establecer el working directory en /app
# WORKDIR /app

# # Actualizar los paquetes de la imagen base
# RUN apt-get update \
#     && apt-get install -y python3 python3-pip python3-venv \
#     && apt-get install -y build-essential libffi-dev libcairo2-dev libsystemd-dev libyaml-dev

# # Crear un entorno virtual en /app/venv
# RUN python3 -m venv venv

# # Actualizar pip, setuptools y wheel
# RUN pip install --upgrade pip setuptools wheel

# # Instalar Cython y otras herramientas de construcción necesarias
# RUN pip install cython

# # Copiar el archivo de requisitos al contenedor
# COPY requirements.txt /app/

# # Instalar las dependencias
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el contenido del proyecto al contenedor
# COPY . /app/

# # Comando por defecto al ejecutar el contenedor
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.10

WORKDIR /app

# Instalar herramientas de construcción
RUN apt-get update \
    && apt-get install -y build-essential libffi-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel Cython==0.29.36

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
