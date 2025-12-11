# view.py
import pygame

# --- Constantes de Visualización ---
BLOCK_SIZE = 30
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
GRID_X_OFFSET = (SCREEN_WIDTH - 10 * BLOCK_SIZE) // 2
GRID_Y_OFFSET = 50

# Colores (R, G, B)
COLORS = [
    (0, 0, 0),        # Negro (fondo)
    (0, 255, 255),    # Cian (I)
    (255, 255, 0),    # Amarillo (O)
    (128, 0, 128),    # Púrpura (T)
    (255, 165, 0),    # Naranja (L)
    (0, 0, 255),      # Azul (J)
    (0, 255, 0),      # Verde (S)
    (255, 0, 0),      # Rojo (Z)
    (128, 128, 128)   # Gris (borde)
]

class TetrisView:
    """Maneja toda la renderización del juego en la pantalla."""
    def __init__(self, model):
        self.model = model
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris MVC")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)

    def draw_block(self, x, y, color_index):
        """Dibuja un solo bloque en la pantalla."""
        color = COLORS[color_index]
        pygame.draw.rect(
            self.screen,
            color,
            (GRID_X_OFFSET + x * BLOCK_SIZE, GRID_Y_OFFSET + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )
        pygame.draw.rect(
            self.screen,
            COLORS[8], # Borde gris
            (GRID_X_OFFSET + x * BLOCK_SIZE, GRID_Y_OFFSET + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1
        )

    def draw_grid(self):
        """Dibuja las piezas fijas en la cuadrícula."""
        for y, row in enumerate(self.model.grid):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(x, y, cell)

    def draw_piece(self, piece):
        """Dibuja la pieza actual."""
        if piece:
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(piece.x + x, piece.y + y, piece.color)

    def draw_ui(self):
        """Dibuja la interfaz de usuario: puntuación, nivel, etc."""
        # Fondo del UI
        pygame.draw.rect(self.screen, (20, 20, 20), (0, 0, GRID_X_OFFSET - 10, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (20, 20, 20), (GRID_X_OFFSET + 10 * BLOCK_SIZE + 10, 0, 200, SCREEN_HEIGHT))

        # Texto de Puntuación
        score_text = self.font.render(f"Score: {self.model.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (GRID_X_OFFSET + 10 * BLOCK_SIZE + 20, 100))

        # Texto de Nivel
        level_text = self.font.render(f"Level: {self.model.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (GRID_X_OFFSET + 10 * BLOCK_SIZE + 20, 150))
        
        # Texto de Siguiente Pieza
        next_text = self.small_font.render("Next:", True, (255, 255, 255))
        self.screen.blit(next_text, (GRID_X_OFFSET + 10 * BLOCK_SIZE + 20, 200))
        
        # Dibujar la siguiente pieza
        if self.model.next_piece:
            for y, row in enumerate(self.model.next_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            self.screen, COLORS[self.model.next_piece.color],
                            (GRID_X_OFFSET + 10 * BLOCK_SIZE + 40 + x * (BLOCK_SIZE-10), 230 + y * (BLOCK_SIZE-10), BLOCK_SIZE-10, BLOCK_SIZE-10)
                        )

    def draw_game_over(self):
        """Muestra la pantalla de Game Over."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(game_over_text, text_rect)

    def update(self):
        """Función principal de dibujo que se llama en cada fotograma."""
        self.screen.fill(COLORS[0]) # Fondo negro
        self.draw_grid()
        self.draw_piece(self.model.current_piece)
        self.draw_ui()
        
        if self.model.game_over:
            self.draw_game_over()
            
        pygame.display.flip()
