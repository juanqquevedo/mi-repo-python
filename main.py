# main.py
import js

# 1. Leer datos de la página actual
url_actual = js.window.location.href
titulo = js.document.title

print(f"[Python] Analizando página: {titulo} ({url_actual})")

# 2. Modificar el DOM o ejecutar tu lógica
parrafos = js.document.querySelectorAll("p")
total_parrafos = len(parrafos)

# 3. Mostrar una alerta nativa del navegador
mensaje = f"Hola desde GitHub Raw!\n\nTítulo: {titulo}\nPárrafos detectados: {total_parrafos}"
js.alert(mensaje)