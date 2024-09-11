# Security Force

Security Force es una aplicación web que gestiona vulnerabilidades de seguridad basadas en los CVEs (Common Vulnerabilities and Exposures) del NIST (National Institute of Standards and Technology). La aplicación utiliza una API REST construida con Django y Django REST Framework para listar, actualizar y visualizar vulnerabilidades, permitiendo también marcar como resueltas las que ya se han gestionado. La base de datos utilizada es PostgreSQL, y la aplicación se puede ejecutar en contenedores Docker para facilitar el despliegue.

## Características

- **Listar Vulnerabilidades**: Obtén una lista paginada de todas las vulnerabilidades.
- **Marcar como Solucionado**: Actualiza vulnerabilidades como solucionadas mediante una solicitud POST.
- **Vulnerabilidades Activas**: Obtén una lista de vulnerabilidades que aún no han sido solucionadas.
- **Resumen de Vulnerabilidades**: Obtén un resumen de vulnerabilidades agrupadas por severidad.

## Requisitos

- Docker
- Docker Compose
- Python 3.8 o superior

## Instalación

1. **Clona el repositorio:**
    git clone https://github.com/franklin2193/security_force.git

2. **Configuración de variables de entorno**
    DB_NAME=security_force_db
    DB_USER=security_force_user
    DB_PASSWORD=qwer12345
    DB_HOST=db
    DB_PORT=5432

    Estas variables ya están configuradas en el docker-compose.yml para poder ser usadas dentro de contenedores, tener presente que si se desea emplear otras variables, se deben realizar los cambios respectivos para el correcto funcionamiento

3. **Construir y levantar los contenedores de Docker**
    Usa Docker Compose para construir las imágenes de Docker y levantar los servicios:

    docker-compose up --build

    Esto levantará los siguientes servicios:

    db: Un contenedor que ejecuta PostgreSQL 13 para almacenar las vulnerabilidades.
    web: Un contenedor que ejecuta la aplicación de Django en el puerto 8000.

4. **Migrar la base de datos**
    Una vez que los contenedores estén levantados, ejecuta las migraciones:

    docker-compose exec web python3 manage.py migrate

5. **Acceder a la aplicación**
    Una vez que los contenedores estén ejecutándose correctamente y las migraciones estén aplicadas, puedes acceder a la aplicación visitando:

    http://localhost:8000

    Esto te llevara a la página principal de la aplicación, donde se puede acceder a las cuatro opciones.

6. **Uso**

    **Listar Vulnerabilidades:** Accede a http://localhost:8000/api/vulnerabilities/
    **Marcar Vulnerabilidades como Solucionadas:** Envía una solicitud POST a http://localhost:8000/api/vulnerabilities/fixed/ con un cuerpo JSON que contenga los IDs de las vulnerabilidades a actualizar.

    Ejemplo Cuerpo de la peticion (JSON):

    {
       "cve_ids": ["CVE-2023-12345", "CVE-2023-67890"]
    }

    **Vulnerabilidades Activas:** Accede a http://localhost:8000/api/vulnerabilities/active/
    **Resumen de Vulnerabilidades:** Accede a http://localhost:8000/api/vulnerabilities/summary/.
