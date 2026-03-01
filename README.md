# Banpay Challenge API

API REST robusta desarrollada con FastAPI para la gestión de usuarios, implementando autenticación JWT, control de acceso basado en roles (RBAC) e integración con la API externa de Studio Ghibli.

## Arquitectura y Decisiones Técnicas

* **Framework Web:** FastAPI, elegido por su alto rendimiento, validación automática de datos y generación nativa de documentación OpenAPI (Swagger).
* **Base de Datos:** PostgreSQL, garantizando integridad relacional, gestionada a través de SQLAlchemy (ORM) y Alembic para migraciones seguras.
* **Seguridad:** * Contraseñas protegidas mediante hashing con algoritmo `bcrypt`.
    * Autenticación de endpoints mediante JSON Web Tokens (JWT).
    * Validación estricta de variables de entorno (Fail-Fast).
    * Código auditado estáticamente con `Bandit` (0 vulnerabilidades reportadas).
* **Despliegue:** Contenerización completa con Docker y Docker Compose para garantizar replicabilidad exacta en cualquier entorno ("Build once, run anywhere").

## Requisitos Previos

* [Docker](https://www.docker.com/) y Docker Compose instalados.
* [Git](https://git-scm.com/)

## Instrucciones de Despliegue (Producción / Local)

Sigue estos pasos para levantar la infraestructura de la API:

1. **Clonar el repositorio:**
   git clone https://github.com/Jedua/challengeBanpay.git
   cd challengeBanpay

2. **Configurar el entorno:**
   Copia el archivo de ejemplo y configura tus credenciales seguras.
   cp .env.example .env
   
   Asegúrate de llenar las variables clave en el archivo `.env`, especialmente las de inicialización del administrador (ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD) y la SECRET_KEY.

3. **Construir y levantar los contenedores:**
   docker-compose up -d --build

4. **Aplicar migraciones de Base de Datos:**
   docker exec -it challengebanpay-api-1 alembic upgrade head

5. **Inicializar el usuario Administrador (Seed):**
   Para evitar la escalada de privilegios, los administradores no pueden registrarse públicamente. Ejecuta este script para crear el primer superusuario usando las credenciales de tu `.env`:
   docker exec -it challengebanpay-api-1 python seed.py

## Uso de la API y Documentación

Una vez levantado el proyecto, la documentación interactiva estará disponible en:
* **Swagger UI:** http://localhost:8000/docs

### Flujo de Autenticación y Autorización

1. **Registro:** Cualquier usuario puede registrarse mediante el endpoint `POST /users/` (restringido a roles estándar: films, people, locations, species, vehicles).
2. **Login:** Usa el endpoint `POST /login` para obtener un `access_token`.
3. **Consumo Ghibli:** Accede a `GET /ghibli/`. La API extraerá tu rol de forma segura desde el token y consumirá la API de Studio Ghibli, filtrando los resultados según tus permisos.
4. **Administración:** Los endpoints de gestión de usuarios (`GET /users/`, `PUT /users/{id}`, `DELETE /users/{id}`) están estrictamente protegidos. Cualquier usuario autenticado que posea el rol de `admin` tiene autorización para consumirlos. Dado que la creación pública de administradores está bloqueada por seguridad, el primer administrador del sistema debe generarse mediante el script `seed.py`.

## Pruebas de Seguridad (SAST)

Para verificar la integridad del código, puedes correr la auditoría de seguridad integrada en el contenedor:
docker exec -it challengebanpay-api-1 bandit -r app/