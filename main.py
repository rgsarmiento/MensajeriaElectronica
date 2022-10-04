# aca importamos de la carpeta app una variable llamada app del archivo __init__.py
from my_app import app, page_400


#Ejecutar la aplicacion
if __name__ == '__main__':
    app.register_error_handler(404, page_400)
    app.run()

