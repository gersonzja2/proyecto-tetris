# model.py
import random

# --- Constantes del Juego ---
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Formas de los Tetrominós (piezas)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]

class Piece:
    """Representa una pieza (Tetrominó) con su forma, posición y rotación."""
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.randint(1, len(SHAPES)) # Un número para representar el color

    def rotate(self):
        """Rota la forma de la pieza 90 grados."""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisModel:
    """Contiene toda la lógica y el estado del juego de Tetris."""
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.current_piece = None
        self.next_piece = None
        self.new_piece()

    def new_piece(self):
        """Crea una nueva pieza y la prepara para ser la siguiente o la actual."""
        shape = random.choice(SHAPES)
        if not self.next_piece:
            self.next_piece = Piece(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape)
        
        self.current_piece = self.next_piece
        self.next_piece = Piece(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, random.choice(SHAPES))

        if self.check_collision(self.current_piece):
            self.game_over = True

    def check_collision(self, piece):
        """Verifica si la pieza está en una posición inválida."""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = piece.y + y
                    grid_x = piece.x + x
                    if not (0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT and self.grid[grid_y][grid_x] == 0):
                        return True
        return False

    def lock_piece(self):
        """Fija la pieza actual en la cuadrícula."""
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        """Busca y elimina las líneas completas."""
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        if lines_to_clear:
            for i in lines_to_clear:
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            
            # Actualizar puntuación y nivel
            num_cleared = len(lines_to_clear)
            self.lines_cleared += num_cleared
            self.score += (num_cleared ** 2) * 100 * self.level
            self.level = 1 + self.lines_cleared // 10

    def move(self, dx, dy):
        """Mueve la pieza actual si es posible."""
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.check_collision(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        return True

    def drop(self):
        """Hace caer la pieza una unidad. Si no puede, la fija."""
        if not self.move(0, 1):
            self.lock_piece()

    def rotate(self):
        """Rota la pieza actual si la rotación es válida."""
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.shape = original_shape # Revertir si hay colisión
