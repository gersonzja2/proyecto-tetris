# controller.py
import pygame

class TetrisController:
    """Maneja la entrada del usuario y el bucle principal del juego."""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = 500  # milisegundos para caer una unidad

    def run(self):
        """Inicia y ejecuta el bucle principal del juego."""
        while not self.model.game_over:
            self.handle_events()
            self.update_game_state()
            self.view.update()
            self.clock.tick(60) # Limita el juego a 60 FPS

        # Bucle de Game Over
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    return
            self.view.update() # Sigue dibujando la pantalla de Game Over

    def handle_events(self):
        """Procesa los eventos de entrada del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.model.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.model.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.model.drop()
                elif event.key == pygame.K_UP:
                    self.model.rotate()
                elif event.key == pygame.K_SPACE:
                    # Hard drop (caída rápida)
                    while self.model.move(0, 1):
                        pass
                    self.model.lock_piece()

    def update_game_state(self):
        """Actualiza el estado del juego basado en el tiempo."""
        self.fall_time += self.clock.get_rawtime()
        
        # Ajustar velocidad de caída según el nivel
        self.fall_speed = max(100, 500 - (self.model.level - 1) * 50)

        if self.fall_time > self.fall_speed:
            self.fall_time = 0
            self.model.drop()
