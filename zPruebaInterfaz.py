import requests
from requests.auth import HTTPBasicAuth
import getpass
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO

API_URL = "http://127.0.0.1:8000"
BASE_IMAGE_URL = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/static/"

class ClienteLibrosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cliente Libros API")
        self.geometry("700x600")

        # Área de texto para mostrar resultados/mensajes
        self.texto = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20)
        self.texto.pack(fill=tk.BOTH, expand=True)

        # Label para imagen
        self.label_imagen = tk.Label(self)
        self.label_imagen.pack(pady=10)

        # Frame para botones
        frame_botones = tk.Frame(self)
        frame_botones.pack(fill=tk.X)

        botones = [
            ("Listar libros", self.listar_libros),
            ("Buscar libro", self.ver_libro_titulo),
            ("Agregar libro", self.agregar_libro),
            ("Eliminar libro", self.eliminar_libro),
            ("Buscar Wiki", self.ver_libro_wiki),
            ("Mostrar portada", self.mostrar_portada),
            ("Salir", self.quit)
        ]

        for (txt, cmd) in botones:
            b = tk.Button(frame_botones, text=txt, command=cmd)
            b.pack(side=tk.LEFT, padx=5, pady=5)

    def pedir_credenciales(self):
        usuario = simpledialog.askstring("Credenciales", "Usuario:", parent=self)
        if usuario is None:
            return None
        password = simpledialog.askstring("Credenciales", "Contraseña:", parent=self, show="*")
        if password is None:
            return None
        return HTTPBasicAuth(usuario.strip(), password)

    def imprimir(self, texto):
        self.texto.insert(tk.END, texto + "\n")
        self.texto.see(tk.END)

    def listar_libros(self):
        self.texto.delete(1.0, tk.END)
        try:
            response = requests.get(f"{API_URL}/libros")
            if response.ok:
                libros = response.json()
                if not libros:
                    self.imprimir("No hay libros disponibles.")
                    return
                for libro in libros:
                    self.imprimir(f"Título: {libro['title']}\nAutor: {libro['author']}\n")
            elif response.status_code == 429:
                self.imprimir("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
            else:
                self.imprimir("Error al obtener libros.")
        except Exception as e:
            self.imprimir(f"Error: {e}")

    def ver_libro_titulo(self):
        self.texto.delete(1.0, tk.END)
        titulo = simpledialog.askstring("Buscar libro", "Título del libro a buscar:", parent=self)
        if not titulo:
            return
        try:
            response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo.strip()})
            if response.ok:
                libro = response.json()
                self.imprimir(f"Título: {libro['title']}\nAutor: {libro['author']}\nAño: {libro['year']}")
            elif response.status_code == 429:
                self.imprimir("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
            else:
                self.imprimir("Libro no encontrado.")
        except Exception as e:
            self.imprimir(f"Error: {e}")

    def ver_libro_wiki(self):
        self.texto.delete(1.0, tk.END)
        titulo = simpledialog.askstring("Buscar Wiki", "Título del libro a buscar:", parent=self)
        if not titulo:
            return
        try:
            response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo.strip()})
            if response.ok:
                libro = response.json()
                self.imprimir(f"Título: {libro['title']}\nLink: {libro['link']}\n")
            elif response.status_code == 429:
                self.imprimir("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
            else:
                self.imprimir("Libro no encontrado.")
        except Exception as e:
            self.imprimir(f"Error: {e}")

    def obtener_imagen_libro(self, titulo):
        try:
            response = requests.get(f"{API_URL}/buscar_libro", params={"book_title": titulo.strip()})
            if response.status_code == 429:
                self.imprimir("Demasiadas solicitudes. Por favor, espera un momento.")
                return None
            response.raise_for_status()
            libro = response.json()
            imagen_relativa = libro.get("imageLink")
            if not imagen_relativa:
                self.imprimir("Este libro no tiene imagen asociada.")
                return None
            if imagen_relativa.startswith("images/"):
                return BASE_IMAGE_URL + imagen_relativa
            return imagen_relativa
        except Exception as e:
            self.imprimir(f"Error al obtener imagen: {e}")
            return None

    def mostrar_portada(self):
        titulo = simpledialog.askstring("Mostrar portada", "Título del libro:", parent=self)
        if not titulo:
            return
        url_imagen = self.obtener_imagen_libro(titulo)
        if not url_imagen:
            return
        try:
            resp = requests.get(url_imagen)
            resp.raise_for_status()
            imagen_data = resp.content
            imagen = Image.open(BytesIO(imagen_data))
            imagen.thumbnail((300, 400))
            self.foto = ImageTk.PhotoImage(imagen)
            self.label_imagen.config(image=self.foto)
            self.imprimir(f"Mostrando portada de '{titulo.strip()}'")
        except Exception as e:
            self.imprimir(f"No se pudo cargar la imagen: {e}")

    def agregar_libro(self):
        auth = self.pedir_credenciales()
        if auth is None:
            return

        autor = simpledialog.askstring("Agregar libro", "Autor:", parent=self)
        if autor is None: return
        pais = simpledialog.askstring("Agregar libro", "País:", parent=self)
        if pais is None: return
        imagen = simpledialog.askstring("Agregar libro", "URL de imagen (o ruta):", parent=self)
        if imagen is None: return
        idioma = simpledialog.askstring("Agregar libro", "Idioma:", parent=self)
        if idioma is None: return
        link = simpledialog.askstring("Agregar libro", "Link (Wikipedia u otro):", parent=self)
        if link is None: return

        while True:
            paginas_str = simpledialog.askstring("Agregar libro", "Cantidad de páginas:", parent=self)
            if paginas_str is None:
                return
            try:
                paginas = int(paginas_str)
                break
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresá un número válido.")

        titulo = simpledialog.askstring("Agregar libro", "Título:", parent=self)
        if titulo is None: return

        while True:
            anio_str = simpledialog.askstring("Agregar libro", "Año de publicación (ej: 1984):", parent=self)
            if anio_str is None:
                return
            try:
                anio = int(anio_str)
                break
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresá un año válido.")

        nuevo_libro = {
            "author": autor.strip(),
            "country": pais.strip(),
            "imageLink": imagen.strip(),
            "language": idioma.strip(),
            "link": link.strip(),
            "pages": paginas,
            "title": titulo.strip(),
            "year": anio
        }

        try:
            response = requests.post(f"{API_URL}/agregar_libro", json=nuevo_libro, auth=auth)
            if response.ok:
                self.imprimir("Libro agregado correctamente.")
            elif response.status_code == 401:
                self.imprimir("Credenciales inválidas.")
            elif response.status_code == 429:
                self.imprimir("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
            else:
                self.imprimir("Error al agregar libro.")
                self.imprimir(response.text)
        except Exception as e:
            self.imprimir(f"Error al agregar libro: {e}")

    def eliminar_libro(self):
        auth = self.pedir_credenciales()
        if auth is None:
            return
        titulo = simpledialog.askstring("Eliminar libro", "Título a eliminar:", parent=self)
        if not titulo:
            return
        try:
            response = requests.delete(f"{API_URL}/borrar_libro/{titulo.strip()}", auth=auth)
            if response.ok:
                self.imprimir("Libro eliminado con éxito")
            elif response.status_code == 401:
                self.imprimir("Credenciales inválidas.")
            elif response.status_code == 429:
                self.imprimir("Demasiadas solicitudes. Esperá un momento y probá de nuevo.")
            else:
                msg = response.json().get("mensaje", "Error al eliminar libro.")
                self.imprimir(msg)
        except Exception as e:
            self.imprimir(f"Error al eliminar libro: {e}")

if __name__ == "__main__":
    app = ClienteLibrosApp()
    app.mainloop()
