// build-bookmarklet.js
const fs = require('fs');
const path = require('path');

// REEMPLAZA ESTO CON TUS DATOS DE GITHUB:
const GITHUB_USER = 'juanqquevedo';
const REPO_NAME = 'mi-repo-python';
const BRANCH = 'main';

const RAW_URL = `https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/${BRANCH}/main.py`;

const loaderCode = `
(async function(){
    const notif = document.createElement('div');
    notif.style = 'position:fixed;top:15px;right:15px;background:#1e293b;color:#f8fafc;padding:10px 16px;border-radius:8px;font-family:sans-serif;font-size:13px;z-index:9999999;box-shadow:0 4px 12px rgba(0,0,0,0.15);';
    notif.innerText = 'Cargando Pyodide y paquetes...';
    document.body.appendChild(notif);

    const updateMsg = (msg) => { notif.innerText = msg; };

    try {
        if (!window.loadPyodide) {
            updateMsg('Descargando Pyodide Wasm...');
            await new Promise((res, rej) => {
                const s = document.createElement('script');
                s.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js';
                s.onload = res;
                s.onerror = rej;
                document.head.appendChild(s);
            });
        }

        if (!window.pyodideInstance) {
            updateMsg('Inicializando motor Python...');
            window.pyodideInstance = await window.loadPyodide();
        }

        const py = window.pyodideInstance;

        updateMsg('Cargando numpy y matplotlib...');
        await py.loadPackage(['numpy', 'matplotlib']);

        updateMsg('Descargando script desde GitHub...');
        const res = await fetch('${RAW_URL}?t=' + Date.now());
        if (!res.ok) throw new Error('HTTP ' + res.status + ' al descargar el script');
        const script = await res.text();

        updateMsg('Ejecutando script Python...');
        await py.runPythonAsync(script);
        notif.remove();
    } catch (err) {
        console.error(err);
        notif.style.background = '#ef4444';
        notif.innerText = 'Error: ' + err.message;
        setTimeout(() => notif.remove(), 4000);
    }
})();
`;

// Minificar y codificar
const bookmarklet = 'javascript:' + encodeURIComponent(loaderCode.replace(/\s+/g, ' ').trim());

// Guardar en dist/
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) fs.mkdirSync(distDir);

fs.writeFileSync(path.join(distDir, 'bookmarklet.txt'), bookmarklet);

console.log('✅ Bookmarklet compilado con éxito en dist/bookmarklet.txt');