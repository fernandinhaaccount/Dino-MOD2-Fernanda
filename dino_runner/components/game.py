import pygame
 
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager

class Game:
    def __init__(self): #construtor/ base do jogo
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False #jogador sempre está correndo
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0 #plano de fundo
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
    
    def execute(self):
        self.running = True #quando meu jogo excutar ele vai correr
        while self.running:
            if not self.playing: #inverte o bool e ele fica falso. mostrando que ele morreu
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
    
    def run(self): #função correr
        self.playing = True #jogador correndo/ativo
        self.obstacle_manager.reset_obstacles() #os obstaculos
        self.power_up_manager.reset_power_ups() #quando o jogo começa do zero(pontuação zero, reseta os obstaculos e a velocidade 0)
        self.game_speed = 20
        self.score = 0
        while self.playing: #game loop
            self.events()
            self.update()
            self.draw() #base do jogo
            
    def events(self):
        for event in pygame.event.get(): #realidade 2d
            if event.type == pygame.QUIT: #se o jogador para de jogar e correr/ false/
                self.playing = False
                self.running = False 
    
    def update(self):
        user_input = pygame.key.get_pressed() #qualquer tecla inicia o jogo
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player) #atulizações da pontuação, da velocidade, vida
    
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0: #a cada 100 pontos aumenta mais 5 de velocidade
            self.game_speed += 5
    
    def draw(self): #base dos desenhos
        self.clock.tick(FPS) 
        self.screen.fill((255, 255, 255)) #cor branca do jogo, tudo desenhado em branco
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update() 
        pygame.display.flip()
    
    def  draw_background(self):
        image_width = BG.get_width() #desenhando o background da tela
        self.screen.blit(BG(self.x_pos_bg, self.y_pos_bg)) 
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed                    
    
    def draw_score(self):
        draw_message_component(
            f"pontuação: {self.score}", #aparecer a pontuação atualizada na tela
            self.screen,
            pos_x_center= 1000, #lugar onde vai aparecer na tela a pontuação
            pos_y_center= 50
        )
    
    def draw_power_up_time(self): #tempo para o escudo aparacer e o poder
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_tick())/ 1000, 2) #numero limitado por milesimo de segundos/se meu dinossauro tem 
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} Disponivel por: {time_to_show} segundos", 
                    self.screen,
                    font_size= 18, #fonte da letra
                    pos_x_center= 500,
                    pos_y_center=40
                )
            else:
                self.player.has_power_up = False # se acabar o jogadoor perde o escudo, voltando a ficar vuneravel
                self.player.type = DEFAULT_TYPE
     def handle_events_on_menu(self):

     def show_menu(self):
