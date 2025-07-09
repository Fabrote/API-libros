import requests
from requests.auth import HTTPBasicAuth
import getpass

import webbrowser
import requests

API_URL = "http://127.0.0.1:8000"


def validar_credenciales(auth):
    try:
        response = requests.get(f"{API_URL}/validar_credenciales", auth=auth)
        if response.status_code == 401:
            print("Credenciales inválidas.")
            return False
        elif response.status_code == 429:
            print("Demasiadas solicitudes. Intentá más tarde.")
            return False
        return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False



def pedir_credenciales():
    """Solicita credenciales."""
    usuario = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña: ")
    return HTTPBasicAuth(usuario, password)


def listar_libros():
    """Solicita y muestra la lista de libros disponibles desde la API."""
    response = requests.get(f"{API_URL}/libros")
    if response.ok:
        for libro in response.json():
            print(f"Título: {libro['title']} \n Autor: ({libro['author']})")

    elif response.status_code == 429:
        print("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
        
    else:
       print("Error al obtener libros.")

def ver_libro_titulo():
    """Solicita al usuario un título y muestra la información del libro correspondiente."""
    titulo = input("Título del libro a buscar: ").strip()
    response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo})
    if response.ok:
        libro = response.json()
        print(f"\nTítulo: {libro['title']}\nAutor: {libro['author']}\nAño: {libro['year']}")
    elif response.status_code == 429:
        print("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
    else:
        print("Libro no encontrado.")
        

def ver_libro_wiki():
    """Busca un libro por título y devuelve la página de Wikipedia si existe."""
    titulo = input("Título del libro a buscar: ").strip()
    response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo})
    if response.ok:
        libro = response.json()
        if libro['link']:
            webbrowser.open(libro['link'])
        print(f"\nTítulo: {libro['title']}\nLink: {libro['link']}\n")
    elif response.status_code == 429:
        print("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
    else:
        print("Libro no encontrado.")



def obtener_imagen_libro(titulo):
    """Busca un libro y abre su imagen de portada en el navegador."""
    BASE_IMAGE_URL = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/static/"
    try:
        response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo})
        
        if response.status_code == 429:
            print("Demasiadas solicitudes. Por favor, espera un momento.")
            return

        response.raise_for_status()
        libro = response.json()

        imagen_relativa = libro.get("imageLink") 
        if not imagen_relativa:
            print("Este libro no tiene imagen asociada.")
            return None
        
        if imagen_relativa.startswith("images/"):
            url_imagen = BASE_IMAGE_URL + imagen_relativa

        webbrowser.open(url_imagen)

        return imagen_relativa

    except requests.HTTPError as e:
        print(f"Libro no encontrado")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return None




def agregar_libro():
    """Solicita al usuario los datos de un nuevo libro y lo agrega mediante autenticación básica."""
    auth = pedir_credenciales()
    
    if not validar_credenciales(auth):
        print("No podés agregar libros.")
        return

    autor = input("Autor: ").strip()
    pais = input("País: ").strip()
    imagen = input("URL de imagen (o ruta): ").strip()
    idioma = input("Idioma: ").strip()
    link = input("Link (Wikipedia u otro): ").strip()
    
    while True:
        try:
            paginas = int(input("Cantidad de páginas: "))
            break
        except ValueError:
            print("Por favor, ingresá un número válido.")

    
    while True:
        titulo = input("Título: ").strip()
        if titulo:
            break
        print("El título no puede estar vacío. Por favor, ingresalo.")


    while True:
        try:
            anio = int(input("Año de publicación (ej: 1984): "))
            break
        except ValueError:
            print("Por favor, ingresá un año válido.")

    nuevo_libro = {
        "author": autor,
        "country": pais,
        "imageLink": imagen,
        "language": idioma,
        "link": link,
        "pages": paginas,
        "title": titulo,
        "year": anio
    }

    response = requests.post(f"{API_URL}/agregar_libro", json=nuevo_libro, auth=auth)

    if response.ok:
        print("Libro agregado correctamente.")

    elif response.status_code == 429:
        print("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
    else:
        print("Error al agregar libro.")
        print(response.text)


def eliminar_libro():
    """Solicita un título y elimina el libro de la API con autenticación básica."""
    auth = pedir_credenciales()
    if not validar_credenciales(auth):
        print("No podés eliminar libros.")
        return
    
    while True:
        libro_title = input("Título a eliminar: ").strip()
        if libro_title:
            break
        print("El título no puede estar vacío. Por favor, ingresalo.")


    response = requests.delete(f"{API_URL}/borrar_libro/{libro_title}", auth=auth)
    if response.ok:
        print("Libro eliminado con éxito")
    elif response.status_code == 429:
        print("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
    else:
        print(response.json().get("mensaje", "Error al eliminar libro."))


def actualizar_libro():   
    """Actualiza los datos de un libro existente mediante autenticación básica."""
    auth = pedir_credenciales()
    if not validar_credenciales(auth):
        print("No podés actualizar libros.")
        return
    
    
    titulo_original = input("Título del libro que querés actualizar: ").strip()
    response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo_original})
    if response.status_code == 404:
        print("Libro no encontrado.")
        return
    print("Ingresá los nuevos datos del libro:")
    autor = input("Autor: ").strip()
    pais = input("País: ").strip()
    imagen = input("URL de imagen (o ruta): ").strip()
    idioma = input("Idioma: ").strip()
    link = input("Link (Wikipedia u otro): ").strip()
    
    while True:
        try:
            paginas = int(input("Cantidad de páginas: "))
            break
        except ValueError:
            print("Por favor, ingresá un número válido.")

    while True:
        titulo = input("Título Nuevo (Puede ser igual al anterior): ").strip()
        if titulo:
            break
        print("El título no puede estar vacío. Por favor, ingresalo.")

    
    while True:
        try:
            anio = int(input("Año de publicación (ej: 1984): "))
            break
        except ValueError:
            print("Por favor, ingresá un año válido.")

    datos_actualizados = {
        "author": autor,
        "country": pais,
        "imageLink": imagen,
        "language": idioma,
        "link": link,
        "pages": paginas,
        "title": titulo,
        "year": anio
    }

    response = requests.put(
        f"{API_URL}/actualizar_libro/{titulo_original}",
        json=datos_actualizados,
        auth=auth
    )

    if response.ok:
        print("Libro actualizado correctamente.")

    elif response.status_code == 429:
        print("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
    else:
        print("Error al actualizar el libro.")
        print(response.text)



# Menù interactivo

if __name__ == "__main__":
    while True:
        print("\n1. Listar libros\n2. Buscar por título\n3. Agregar libro\n4. Eliminar libro\n5. Buscar página de wikipedia\n6. Obtener Portada del libro\n7. Actualizar libro \n8. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            listar_libros()
        elif opcion == "2":
            ver_libro_titulo()
        elif opcion == "3":
            agregar_libro()
        elif opcion == "4":
            eliminar_libro()
        elif opcion == "5":
            ver_libro_wiki()
        elif opcion == "6":
            titulo = input("Título del libro a buscar: ").strip()
            url = obtener_imagen_libro(titulo)
            if url:
                print(f"Imagen: {url}")
        elif opcion == "7":
            actualizar_libro()
        elif opcion == "8":
            break
        else:
            print("Opción inválida.")
