# main.py
import js
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

print("[Python] Iniciando pruebas de cálculo y renderizado...")

# 1. Prueba de computación con NumPy
x = np.linspace(0, 4 * np.pi, 200)
y = np.sin(x) * np.exp(-x / 5)
promedio = float(np.mean(y))
desviacion = float(np.std(y))

# 2. Generación de gráfico en memoria con Matplotlib
fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
ax.plot(x, y, color="#2563eb", linewidth=2, label="Onda amortiguada")
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.set_title("Gráfico generado desde Python (Wasm)", fontsize=11)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
plt.tight_layout()

# Guardar figura en base64
buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)
img_b64 = base64.b64encode(buf.read()).decode("utf-8")
plt.close(fig)

# 3. Inyección visual en el DOM de la página activa
modal_id = "pyodide-test-modal"

# Si ya existía un modal anterior, eliminarlo
existente = js.document.getElementById(modal_id)
if existente:
    existente.remove()

# Crear tarjeta flotante en la esquina
modal = js.document.createElement("div")
modal.id = modal_id
modal.style.position = "fixed"
modal.style.bottom = "20px"
modal.style.right = "20px"
modal.style.zIndex = "999999"
modal.style.backgroundColor = "#ffffff"
modal.style.color = "#1e293b"
modal.style.padding = "16px"
modal.style.borderRadius = "12px"
modal.style.boxShadow = "0 10px 25px rgba(0,0,0,0.25)"
modal.style.fontFamily = "sans-serif"
modal.style.maxWidth = "420px"
modal.style.border = "1px solid #e2e8f0"

modal.innerHTML = f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <strong style="color:#0f172a; font-size:14px;">Pyodide + GitHub Raw OK</strong>
        <button id="pyodide-close-btn" style="border:none; background:transparent; font-size:18px; cursor:pointer; color:#64748b;">✕</button>
    </div>
    <p style="margin:0 0 8px 0; font-size:12px; color:#475569;">
        <strong>NumPy:</strong> Media = {promedio:.4f} | Desv = {desviacion:.4f}
    </p>
    <img src="data:image/png;base64,{img_b64}" style="width:100%; border-radius:6px; display:block;"/>
"""

js.document.body.appendChild(modal)

# Botón para cerrar
def cerrar_modal(event):
    modal.remove()

btn_cerrar = js.document.getElementById("pyodide-close-btn")
btn_cerrar.onclick = cerrar_modal

print("[Python] Modal inyectado con éxito.")