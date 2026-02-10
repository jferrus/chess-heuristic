# Chess Heuristic

Este es un juego de ajedrez interactivo implementado en Python que utiliza la biblioteca `pygame` para la interfaz gráfica y `python-chess` para la lógica del juego. El sistema permite jugar contra una IA con heurísticas personalizables.

## Requisitos

- Python 3.12 instalado en el sistema.

## Cómo ejecutar el programa

Sigue estos pasos para configurar y ejecutar el juego en cualquier plataforma (Windows, macOS o Linux):

### 1. Preparar el entorno virtual

Es recomendable usar un entorno virtual para aislar las dependencias del proyecto.

**macOS / Linux:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar dependencias

Una vez activado el entorno, instala las bibliotecas necesarias:

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el juego

Para iniciar el juego, ejecuta el archivo principal:

```bash
python3.12 main.py
```

## Características

- Interfaz gráfica intuitiva con `pygame`.
- Lógica de juego robusta basada en `python-chess`.
- IA con búsqueda Minimax y heurísticas optimizadas.
