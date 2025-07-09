# Descarga de paquetes necesario
# pip install fastapi
# pip install requests
# pip install slowapi
# pip install uvicorn


# Importa librerías
import requests
import json
from pydantic import BaseModel
from typing import List 
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


url = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/books.json"
response = requests.get(url)
books_data = response.json()

# Guardar el JSON localmente
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4)

print("Archivo books.json descargado y cargado exitosamente.")

# Archivo de datos
JSON_FILE = "books.json"


app = FastAPI()

#Límite de velocidad:
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


#Seguridad:
security = HTTPBasic()
USER = "admin"
PASSWORD = "1234"


def verificar_credenciales(credentials: HTTPBasicCredentials = Depends(security)):
    """"Verifica las credenciales del usuario para determinar a qué funcionalidades puede acceder"""
    
    correct_user = secrets.compare_digest(credentials.username, USER)
    correct_pass = secrets.compare_digest(credentials.password, PASSWORD)
    
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return credentials.username 



# Modelo de libro
class Book(BaseModel):
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int


def cargar_libros():
    """Carga los libros desde el archivo JSON local."""

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_libros(books):
    """Guarda la lista de libros en el archivo JSON."""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2)


@app.get("/validar_credenciales")
def validar(user: str = Depends(verificar_credenciales)):
    """Valida que las credenciales ingresadas sean correctas"""
    return {"mensaje": f"Usuario {user} autenticado correctamente"}


@app.get("/libros", response_model=List[Book])
@limiter.limit("5/second")
async def listar_libros(request: Request):
    """Devuelve la lista completa de libros almacenados. Rate limit: 5 peticiones por segundo."""
    return cargar_libros()

@app.get("/buscar_libro", response_model=Book)
@limiter.limit("3/second")
async def buscar_libro(request: Request, book_title: str):
    """ Busca un libro por título.Rate limit: 3 peticiones por segundo."""
    books = cargar_libros()
    for book in books:
        if book_title == book["title"]:
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/agregar_libro")
@limiter.limit("2/second")
async def agregar_libro(request: Request, book: Book, user: str = Depends(verificar_credenciales)):
    """Agrega un nuevo libro a la colección. Rate limit: 2 peticiones por segundo."""
    if not book.title.strip():
        raise HTTPException(status_code=400, detail="El título no puede estar vacío.")
    books = cargar_libros()
    books.append(book.model_dump())
    guardar_libros(books)
    print(books[-1])
    return {"mensaje": "Libro agregado correctamente."}

@app.put("/actualizar_libro/{book_title}")
@limiter.limit("2/second")
async def actualizar_libro(request: Request, book_title: str, libro_actualizado: Book, user: str = Depends(verificar_credenciales)):
    """Actualiza un libro existente. Rate limit: 2 peticiones por segundo."""
    if not libro_actualizado.title.strip():
        raise HTTPException(status_code=400, detail="El título no puede estar vacío.")
    
    books = cargar_libros()
    titulo_low = book_title.strip().lower()
    for i, book in enumerate(books):
        if book["title"].strip().lower() == titulo_low:
            books[i] = libro_actualizado.model_dump()
            guardar_libros(books)
            return {"mensaje": f"Libro '{book_title}' actualizado correctamente."}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/borrar_libro/{book_title}")
@limiter.limit("2/second")
async def delete_libro(request: Request, book_title: str, user: str = Depends(verificar_credenciales)):
    """Elimina un libro por su título.Rate limit: 2 peticiones por segundo."""
    books = cargar_libros()
    for i, book in enumerate(books):
        if book["title"] == book_title:
            eliminado = books.pop(i)
            guardar_libros(books)
            return {"mensaje": f"Libro '{eliminado['title']}' eliminado correctamente."}

    raise HTTPException(status_code=404, detail="Libro no encontrado")





# uvicorn server:app --reload (se ejecuta despues de ejecutar el codigo)
#Documentación interactiva: http://127.0.0.1:8000/docs