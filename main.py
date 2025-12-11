# main.py
from model import TetrisModel
from view import TetrisView
from controller import TetrisController

if __name__ == "__main__":
    # 1. Crear el Modelo
    model = TetrisModel()
    
    # 2. Crear la Vista (pasándole el modelo para que pueda leer los datos)
    view = TetrisView(model)
    
    # 3. Crear el Controlador (pasándole el modelo y la vista)
    controller = TetrisController(model, view)
    
    # 4. Iniciar el juego
    controller.run()
