# Cosecheros server backend 0.1

### Primeros pasos
- Clonar el repo
- Ejecutar `pip install -r requirements.txt` para instalar las dependencias
- Obtener el json de google

### Iniciar firebase
- Ejecutar la siguiente linea en una terminal `export GOOGLE_APPLICATION_CREDENTIALS="path/to/firebase/keys.json"`

### Iniciar el servidor
- Ejecutar `python init_server.py`
- La variable `reload=True` permite que es el servidor escuche los cambios mientras se trabaja en el código.

## Estructura de código
```
├── server
│   ├── __init__.py
│   ├── init_app.py             # Init app and variables
│   ├── init_server.py          # Run server
│   ├── requirements.txt        # Dependencies to install
│   ├── api                     # Router
│   │   ├── __init__.py
│   │   ├── api.py              # List all endpoints
│   │   └── endpoints           # Avalaibles endpoints
│   │       ├── __init__.py
│   │       ├── tweets.py       # paths for tweets
│   │       └── fire_docs.py    # paths for firebase documents
│   ├── scripts                 # Scripts
│   │   ├── __init__.py
│   │   ├── get_tweets.py       # Return tweets
│   │   └── test_firebase.py    # script for testing
│   └── templates               # Templates
│       ├── __init__.py
│       └── mainpage.html       # Init page
```

### TODO
- Agregar modelos para tomar las respuestas (hay uno de ejemplo)
- Agregar "tabular_datos" en la api de fire_docs
- Agregar "busqueda_tweets" en una api que se ejecute cada 10min
