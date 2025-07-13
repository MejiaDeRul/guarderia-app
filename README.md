
# 🚀 FastAPI MVC Boilerplate

Plantilla base para aplicaciones FastAPI organizada con arquitectura **MVC (Modelo - Vista - Controlador)**. Ideal para escalar proyectos de forma clara y mantenible.

---

## 📁 Estructura del Proyecto

```
app/
├── main.py                # Punto de entrada de la aplicación (con lifespan)
├── config.py              # Variables de configuración y entorno

├── models/                # Modelos ORM de SQLAlchemy
├── schemas/               # Esquemas Pydantic (entrada/salida de datos)
├── controllers/           # Lógica de negocio
├── views/                 # Endpoints de la API
├── services/              # Lógica auxiliar (auth, helpers, etc.)
├── database/              # Configuración de la base de datos
├── dependencies/          # Dependencias reutilizables (como get_db)
├── middlewares/           # Middlewares personalizados (opcional)
├── utils/                 # Funciones utilitarias comunes
```

---

## ⚙️ Requisitos

- Python 3.10+
- `pip`
- Virtualenv (opcional, pero recomendado)

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/fastapi-mvc-boilerplate.git
cd fastapi-mvc-boilerplate

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 Ejecución de la app

```bash
uvicorn app.main:app --reload
```

Abre en tu navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Correr tests (con base de datos en memoria)

```bash
pytest
```

Esto ejecuta los tests definidos en `tests/`, usando una base de datos SQLite en memoria (`sqlite://`) para no afectar tu entorno real.

---

## 📄 Licencia

MIT © 2025 Juan Mejía
