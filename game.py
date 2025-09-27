import pygame

class Game:
    def __init__(self, state_machine, gameboard):
        pygame.init()
        self.state_machine = state_machine
        self.gameboard = gameboard
        self.width = 600
        self.height = 600
        self.square_size = 30
        self.FPS = 10
        self.lg_font = pygame.font.SysFont("Calibri", 58)
        self.md_font = pygame.font.SysFont("Calibri", 32)
        self.sm_font = pygame.font.SysFont("Calibri", 16)
        self.y_boundary = (0, 19)
        self.x_boundary = (0, 9)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Drop Da Blockz")
        self.clock = pygame.time.Clock()
        self.running = True
        if hasattr(Game, "_instance"):
            raise Exception("Game is a singleton! Use Game.get_instance().")
        Game._instance = self

    @staticmethod
    def get_instance():
        if not hasattr(Game, "_instance"):
            Game()
        return Game._instance
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state_machine.handle_events(event)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.render()
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)


