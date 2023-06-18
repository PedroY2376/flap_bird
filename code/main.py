import pygame, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        #! SetUp
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flap Bird')
        self.clock = pygame.time.Clock()
        self.active = True
        
        #! Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        #! Scale Factor - Background
        bg_height = pygame.image.load('graphics/background.png').get_height()
        self.scale_factor = SCREEN_HEIGHT / bg_height

        #! Sprite SetUp
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
        
        #! Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
        
        #! Text - Font
        self.font = pygame.font.Font('font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0
        
        #! Menu
        self.menu_surf = pygame.image.load('graphics/menu.png'). convert_alpha()
        # self.menu_surf = pygame.transform.scale(self.menu_surf, pygame.math.Vector2(self.menu_surf.get_size()) * self.scale_factor * 0.7)
        self.menu_rect = self.menu_surf.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        
        #! Music
        self.music = pygame.mixer.Sound('sounds/music.wav')
        self.music.set_volume(0.15)
        self.music.play(loops=-1)
        
    #! Collison
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            self.active = False
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle': sprite.kill()
            self.plane.kill()
        
    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) /1000
            y = SCREEN_HEIGHT/10
        else:
            y = SCREEN_HEIGHT/2 + self.menu_rect.height
        
        score_surf = self.font.render(f'{int(self.score)}', True, (0,0,0))
        score_rect = score_surf.get_rect(midtop = (SCREEN_WIDTH/2, y))       
        self.screen.blit(score_surf, score_rect)
        
    def run(self):
        last_time = time.time()
        while True:
            #! Delta Time
            dt = time.time() - last_time
            last_time = time.time()

            #! Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                    
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.plane.jump()
                        
                    if self.active == False and event.key == pygame.K_KP_ENTER:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.start_offset = pygame.time.get_ticks()
                        self.active = True
                        
            #! Game logic
            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)
            self.display_score()
            
            if self.active: self.collisions()
            else: self.screen.blit(self.menu_surf, self.menu_rect)
            
            pygame.display.update()
            self.clock.tick(FRAME_RATE)
            
if __name__ == '__main__':
    game = Game()
    game.run()