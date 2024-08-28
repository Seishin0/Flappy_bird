import pygame
import time 
import os 
import random
pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3.png")))]

SKINS = {
    "Default":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3.png")))],
    "Black":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1black.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2black.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3black.png")))] ,
    "Blue":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1blue.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2blue.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3blue.png")))] ,
    "Green":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1green.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2green.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3green.png")))] ,
    "Orange":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1orange.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2orange.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3orange.png")))] ,
    "Pink":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1pink.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2pink.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3pink.png")))] ,
    "Purple":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1purple.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2purple.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3purple.png")))] ,
    "Red":[pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1red.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2red.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3red.png")))] ,
}
current_skin = BIRD_IMGS

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bg.png")))

Points = pygame.font.SysFont("Consolas", 40)
MENU_FONT = pygame.font.SysFont("Consolas", 70)
max_score=0
frame_count=0

class Bird:
    imgs = BIRD_IMGS
    max_rotation = 25
    rot_vel=20
    animation_time = 5 
    
    def __init__(self,x,y,skin):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count = 0
        self.img = self.imgs[0]
        self.imgs=skin
    
    def jump(self):
        self.vel = -10
        self.tick_count=0
        self.height = self.y
    
    def move(self):
        self.tick_count +=1

        d = self.vel*self.tick_count+ 1.5*self.tick_count**2

        if d>=16:
            d=16
        if d<0:
            d-=2
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -=self.rot_vel


    def draw(self, win):
        self.img_count +=1
        if self.img_count< self.animation_time:
            self.img=self.imgs[0]
        elif self.img_count< self.animation_time*2:
            self.img=self.imgs[1]
        elif self.img_count< self.animation_time*3:
            self.img=self.imgs[2]
        elif self.img_count< self.animation_time*4:
            self.img=self.imgs[1]
        elif self.img_count< self.animation_time*4+1:
            self.img=self.imgs[0]
            self.img_count=0

        if self.tilt<= -80:
            self.img = self.imgs[1]
            self.img_count=self.animation_time*2

        #this part is from stackoverflow
        rotated_image=pygame.transform.rotate(self.img, self.tilt)
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    gap = 200
    vel = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 200
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(PIPE_IMG,False,True)
        self.pipe_bottom = PIPE_IMG
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random. randrange(40,450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap
    
    def move(self):
        self.x -= self.vel

    def draw(self,win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def colldie(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False


class Base:
    VEL = 5
    Width = BASE_IMG.get_width()
    IMG=BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1  = 0
        self.x2  = self.Width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.Width < 0:
            self.x1  = self.x2 + self.Width

        if self.x2 + self.Width < 0:
            self.x2  = self.x1 + self.Width
    def draw(self,win):
        win.blit(self.IMG, (self.x1,self.y))
        win.blit(self.IMG, (self.x2,self.y))


def skin_menu(win):
    win.blit(BG_IMG, (0,0))
    y_offset = 100
    count=0
    skin_rects={}
    for skin_name, skin_imgs in SKINS.items():
        skin_button = skin_imgs[0]
        if count % 2 ==0:
            skin_rect = skin_button.get_rect(center=(WIN_WIDTH/4, y_offset))
        else:
            skin_rect = skin_button.get_rect(center=(3*WIN_WIDTH/4, y_offset))
        win.blit(skin_button, skin_rect)

        skin_text = Points.render(skin_name, 1, (255,255,255))
        skin_text_rect = skin_text.get_rect(midtop=skin_rect.midbottom)
        win.blit(skin_text, skin_text_rect)

        skin_rects[skin_name] = skin_rect
        if count % 2 == 1:
            y_offset +=150
        count+=1
    pygame.display.update()

    return skin_rects

def draw_window(win, bird, pipes, base, score, max_score):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    point = Points.render("Score: "+str(score),1,(255,255,255))
    max_point = Points.render("Best: "+str(max_score),1,(255,255,255))
    win.blit(point,(WIN_WIDTH - 10 - point.get_width(),10))
    win.blit(max_point,(10 ,10))
    base.draw(win)
    bird.draw(win)
    pygame.display.update()
    
def draw_menu(win,max_score,frame_count, current_skin):
    win.blit(BG_IMG, (0,0))
    
    play_button = MENU_FONT.render("Play", 1, (255,255,255))
    exit_button = MENU_FONT.render("Exit", 1, (255,255,255))
    skin_button = current_skin[frame_count // 10 % len(current_skin)]

    play_rect = play_button.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 - 100))
    exit_rect = exit_button.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 100))
    skin_rect = skin_button.get_rect(topright=(WIN_WIDTH - 30, 30))

    win.blit(play_button, play_rect)
    win.blit(exit_button, exit_rect)
    win.blit(skin_button, skin_rect)

    skin_text = Points.render("Skins", 1, (255, 255, 255))
    skin_text_rect = skin_text.get_rect(midtop=skin_rect.midbottom)
    win.blit(skin_text, skin_text_rect)

    max_point = Points.render("Best:"+str(max_score),1,(255,255,255))
    win.blit(max_point,(20 ,20))
    pygame.display.update()

    return play_rect, exit_rect, skin_rect

def main_menu(current_skin):
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    run=True
    in_skin_menu= False
    global max_score
    global frame_count
    while run:
        
        frame_count+=1
        if in_skin_menu:
            skin_rects= skin_menu(win)
        else:
            play_rect, exit_rect, skin_rect =draw_menu(win, max_score,frame_count, current_skin)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if in_skin_menu:
                    if in_skin_menu:
                        for skin_name, rect in skin_rects.items():
                            if rect.collidepoint(mx, my):
                                current_skin = SKINS[skin_name]
                                in_skin_menu = False 
                else:  
                    if skin_rect.collidepoint(mx, my):
                        in_skin_menu=True
                    if play_rect.collidepoint(mx, my):
                        main(current_skin)

                    if exit_rect.collidepoint(mx, my):
                        pygame.quit()
                        quit()

def main(current_skin):
    bird= Bird(200,300,current_skin) #230,300
    base= Base(730)
    pipes=[Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    score=0
    global max_score
    run=True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w) or  (event.key == pygame.K_SPACE) :
                    bird.jump()
                
        bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.colldie(bird):
                run = False
            if pipe.x + pipe.pipe_top.get_width()<0:
                rem.append(pipe)
            if not pipe.passed and pipe.x<bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score+=1
            pipes.append(Pipe(700))
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >=730 or bird.y <0:
            run = False
        base.move()
        draw_window(win,bird,pipes, base,score,max_score)
        
        if score>max_score:
            max_score=score

    main_menu(current_skin)

main_menu(current_skin)




