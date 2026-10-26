<h1>EFI-Python-y-JavaScript</h1>


<h3>"El Imaginario"</h3>
Cartelera colaborativa de eventos, talleres e itinerarios culturales. Creamos una interfaz para aglomerar los establecimientos/eventos culturales/recreativos de Río Cuarto en una misma página web y aplicación

API utilizada: Fastapi

Pasos para ejecutar la aplicación:

<h2>REACT:</h2>

1-Clonar repositorio

    git clone https://github.com/Framus29/EFI-Python-y-Javascript
    cd <nombre-de-la-carpeta>

2-Estando ya ubicado en la carpeta de tu proyecto y ejecuta este comando: 

    npm install

3-Para ejecutar la aplicacion:

  -si usas vite:
  
    npm run dev
    
  -si usas Create React App:

    npm start
  
4-Abre tu navegador web e ingresa a la dirección local que aparece en la terminal.

<h2>FastAPI:</h2>

1-Instalar uv (solo la primera vez si no lo tienes instalado):

    curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

2-Crear el proyecto e ingresar:

    uv init <nombre_archivo>
    cd <nombre_archivo>
  
3-Instalar FastAPI en modo standard:

    uv add "fastapi[standard]"

4-Crear el archivo main.py dentro de la estructura de carpetas:

    touch src/<nombre_archivo>/main.py

5-Instalar el proyecto en modo editable dentro del .venv:(Permite que FastAPI detecte automáticamente el código dentro de src/)

    uv pip install -e .

6-Levantar el servidor:

    uv run fastapi dev
7-Abre tu navegador web e ingresa a la dirección local que aparece en la terminal.
  
<h4>Integrantes: 
  -Noel Rüegger Albert
  -Lucas Ezequiel Lorenzoni Brown
  -Francisco Sbarra
</h4>
