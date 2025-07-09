#  API de Libros - Proyecto Redes de Datos

Este proyecto es una **API REST** desarrollada con **FastAPI**, que permite gestionar una colección de libros basada en un archivo `books.json`. Fue realizado como parte del proyecto final para la materia **Redes de Datos (IA3.5)** de la Tecnicatura Universitaria en Inteligencia Artificial (UNR).

---

##  Funcionalidades

- 🔐 **Autenticación básica** con usuario y contraseña.
- ⏱️ **Rate limiting** para limitar la cantidad de peticiones por IP.
- 🔄 **Operaciones CRUD** completas:
  - `GET /books` – Listar todos los libros.
  - `GET /books/{id}` – Obtener un libro por su ID.
  - `POST /books` – Agregar un nuevo libro.
  - `PUT /books/{id}` – Actualizar un libro existente.
  - `DELETE /books/{id}` – Eliminar un libro por ID.
- 💻 **Cliente HTTP** en Python usando la librería `requests`.
- 📄 Los datos se almacenan en un archivo `books.json`.

---

## ⚙️ Tecnologías utilizadas

- Python 3.10+
- FastAPI
- Uvicorn
- Requests
- Pydantic

---

## 🛠️ Instalación y ejecución



git clone https://github.com/Fabrote/API-libros.git
cd API-libros


🧪 Endpoints principales
GET /books
Devuelve la lista completa de libros.

GET /books/{id}
Devuelve los detalles de un libro según su ID.

POST /books
Agrega un nuevo libro. Requiere autenticación.

PUT /books/{id}
Modifica un libro existente. Requiere autenticación.

DELETE /books/{id}
Elimina un libro. Requiere autenticación.

🔐 Autenticación
La API utiliza autenticación básica HTTP.

🙋‍♂️ Autor
Fabri
Estudiante de la Tecnicatura Universitaria en Inteligencia Artificial – UNR
GitHub: @Fabrote