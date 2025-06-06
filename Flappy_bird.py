import pygame
import json
import os 
import random
import sys,time
pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

#skins and themes
SKINS = {
    "Classic":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3.png")))],
    "Black":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1black.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2black.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3black.png")))] ,
    "Blue":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1blue.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2blue.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3blue.png")))] ,
    "Green":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1green.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2green.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3green.png")))] ,
    "Orange":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1orange.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2orange.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3orange.png")))] ,
    "Pink":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1pink.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2pink.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3pink.png")))] ,
    "Purple":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1purple.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2purple.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3purple.png")))] ,
    "Red":[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird1red.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird2red.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\SKINS","bird3red.png")))] ,
}
PRICE = {
    "Classic":0,
    "Black":100,
    "Blue":100,
    "Green":100,
    "Orange":200,
    "Pink":200,
    "Purple":300,
    "Red":300,
    "Sky":300,
    "Hell":400,
    "Jungle":500
}
OWNED = {
    "Classic":True,
    "Black":False,
    "Blue":False,
    "Green":False,
    "Orange":False,
    "Pink":False,
    "Purple":False,
    "Red":False,
    "Sky":False,
    "Hell":False,
    "Jungle":False
}
PIPES = {
    "Classic":pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","pipe.png"))),
    "Sky": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","pipe_sky.png"))),
    "Hell":pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","pipe_hell.png"))) ,
    "Jungle": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","pipe_jungle.png")))
}
BACKGROUNDS = {
    "Classic":pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","bg.png"))),
    "Sky": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","bg_sky.png"))),
    "Hell":pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","bg_hell.png"))) ,
    "Jungle": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","bg_jungle.png")))

}
BASES = {
    "Classic":pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","base.png"))),
    "Sky": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","base_sky.png"))),
    "Hell":pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","base_hell.png"))) ,
    "Jungle": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs\\THEMES","base_jungle.png")))

}
THEMES = {
    "Classic":pygame.image.load(os.path.join("imgs\\THEMES","theme_classic.png")),
    "Sky": pygame.image.load(os.path.join("imgs\\THEMES","theme_sky.png")),
    "Hell":pygame.image.load(os.path.join("imgs\\THEMES","theme_hell.png")) ,
    "Jungle": pygame.image.load(os.path.join("imgs\\THEMES","theme_jungle.png"))
}
GOLD_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","Gold.png")))
SCORE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","Score.png")))
MAXSCORE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bestScore.png")))

Points = pygame.font.SysFont("Consolas", 40)
MENU_FONT = pygame.font.SysFont("Consolas", 70)
frame_count=0


def get_skin_name(current_skin):
    for skin_name, skin_imgs in SKINS.items():
        if skin_imgs == current_skin:
            return skin_name
    return "Classic" #If found none

def save(max_score , gold, skin, theme, filename="Data.json"):
    skin_name=get_skin_name(skin)
    owned_skins = list(OWNED.values())
    data = {
        "max_score": max_score,
        "gold":gold,
        "skin":skin_name,
        "theme":theme,
        "skins_owned":owned_skins
    }
    with open(filename, 'w') as file:
        json.dump(data, file)

def load(filename="Data.json"):
    try:
        with open(filename, 'r') as file:
            data=json.load(file)
            return data["max_score"],data["gold"],data["skin"],data["theme"],data["skins_owned"]
    except:
        return 0,0,"Classic","Classic",[True,False,False,False,False,False,False,False,False,False,False]

max_score, gold, current_skin_name,theme, owned_skins = load()
current_skin=SKINS.get(current_skin_name)
OWNED=dict(zip(OWNED.keys(),owned_skins))

class Bird:
    max_rotation = 25
    rot_vel=20
    animation_time = 5 
    
    def __init__(self,x,y,skin):
        self.x = x
        self.y = y
        self.imgs=skin
        self.tilt = 0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count = 0
        self.img = self.imgs[0]
        
    
    def jump(self):
        self.vel = -10
        self.tick_count=0
        self.height = self.y
    
    def move(self,dt):
        self.tick_count +=1

        d = self.vel*self.tick_count+ 1.5*self.tick_count**2

        if d>=16:
            d =16
        if d<0:
            d-=2
        self.y = self.y + d* dt

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

    def __init__(self, x,theme):
        self.x = x
        self.height = 0
        self.gap = 200
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(PIPES[theme],False,True)
        self.pipe_bottom = PIPES[theme]
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random. randrange(40,450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap
    
    def move(self,dt):
        self.x -= self.vel *dt

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

    def __init__(self,y,theme):
        self.y = y
        self.IMG=BASES[theme]
        self.Width = self.IMG.get_width()
        self.x1  = 0
        self.x2  = self.Width

    def move(self,dt):
        self.x1 -= self.VEL*dt
        self.x2 -= self.VEL*dt

        if self.x1 + self.Width < 0:
            self.x1  = self.x2 + self.Width

        if self.x2 + self.Width < 0:
            self.x2  = self.x1 + self.Width
    def draw(self,win):
        win.blit(self.IMG, (self.x1,self.y))
        win.blit(self.IMG, (self.x2,self.y))

def skin_menu(win,gold,theme):
    win.blit(BACKGROUNDS[theme], (0,0))
    y_offset = 100
    count=0
    win.blit(GOLD_IMG,(10,10))
    gold_text = Points.render(str(gold),1,(255,255,255))
    win.blit(gold_text,(70 ,15))
    skin_rects={}
    for skin_name, skin_imgs in SKINS.items():
        if OWNED.get(skin_name):
            skin_button = skin_imgs[0]
            skin_text = Points.render(skin_name, 1, (255,255,255))
        else:
            skin_button = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","Locked.png")))
            skin_text = Points.render(str(PRICE.get(skin_name)), 1, (255,255,255))
        if count % 2 ==0:
            skin_rect = skin_button.get_rect(center=(WIN_WIDTH/4, y_offset))
        else:
            skin_rect = skin_button.get_rect(center=(3*WIN_WIDTH/4, y_offset))
        win.blit(skin_button, skin_rect)
    
        skin_text_rect = skin_text.get_rect(midtop=skin_rect.midbottom)
        win.blit(skin_text, skin_text_rect)

        skin_rects[skin_name] = skin_rect
        if count % 2 == 1:
            y_offset +=150
        count+=1
    pygame.display.update()

    return skin_rects

def theme_menu(win,gold,theme):
    win.blit(BACKGROUNDS[theme], (0,0))
    y_offset = 200
    count=0
    win.blit(GOLD_IMG,(10,10))
    gold_text = Points.render(str(gold),1,(255,255,255))
    win.blit(gold_text,(70 ,15))
    theme_rects={}
    for theme_name, theme_img in THEMES.items():
        if OWNED.get(theme_name):
            theme_button = pygame.transform.scale2x(theme_img)
            theme_text = Points.render(theme_name, 1, (255,255,255))
        else:
            theme_button = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","Lockedtheme.png")))
            theme_text = Points.render(str(PRICE.get(theme_name)), 1, (255,255,255))
        if count % 2 ==0:
            theme_rect = theme_button.get_rect(center=(WIN_WIDTH/4, y_offset))
        else:
            theme_rect = theme_button.get_rect(center=(3*WIN_WIDTH/4, y_offset))
        win.blit(theme_button, theme_rect)
    
        theme_text_rect = theme_text.get_rect(midtop=theme_rect.midbottom)
        win.blit(theme_text, theme_text_rect)

        theme_rects[theme_name] = theme_rect
        if count % 2 == 1:
            y_offset +=300
        count+=1
    pygame.display.update()

    return theme_rects

def draw_window(win, bird, pipes, base, score, max_score, theme, gold):
    win.blit(BACKGROUNDS[theme], (0,0))
    for pipe in pipes:
        pipe.draw(win)

    win.blit(SCORE_IMG,(WIN_WIDTH-SCORE_IMG.get_width()-10,10))
    point = Points.render(str(score),1,(2,2,2))
    win.blit(point,(WIN_WIDTH - 22 - point.get_width(),24))

    win.blit(MAXSCORE_IMG,(10,10))
    max_point = Points.render(str(max_score),1,(255,255,255))
    win.blit(max_point,(70 ,20))
    win.blit(GOLD_IMG,(10,65))
    gold_text = Points.render(str(gold),1,(255,255,255))
    win.blit(gold_text,(70 ,70))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()
    
def draw_menu(win,max_score,frame_count, current_skin, theme, gold):
    win.blit(BACKGROUNDS[theme], (0,0))
    
    play_button = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","Play.png")))
    exit_button = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","Exit.png")))
    skin_button = current_skin[frame_count // 10 % len(current_skin)]
    theme_button = THEMES[theme]

    play_rect = play_button.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 100))
    exit_rect = exit_button.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 250))
    skin_rect = skin_button.get_rect(topright=(WIN_WIDTH - 35, 30))
    theme_rect = theme_button.get_rect(topright=(WIN_WIDTH - 40, 140))

    win.blit(play_button, play_rect)
    win.blit(exit_button, exit_rect)
    win.blit(skin_button, skin_rect)
    win.blit(theme_button, theme_rect)

    skin_text = Points.render("Skins", 1, (255, 255, 255))
    skin_text_rect = skin_text.get_rect(midtop=skin_rect.midbottom)
    win.blit(skin_text, skin_text_rect)

    theme_text = Points.render("Themes", 1, (255, 255, 255))
    theme_text_rect = theme_text.get_rect(midtop=theme_rect.midbottom)
    win.blit(theme_text, theme_text_rect)

    win.blit(MAXSCORE_IMG,(10,10))
    max_point = Points.render(str(max_score),1,(255,255,255))
    win.blit(max_point,(70 ,20))

    win.blit(GOLD_IMG,(10,65))
    gold_text = Points.render(str(gold),1,(255,255,255))
    win.blit(gold_text,(70 ,70))
    pygame.display.update()

    return play_rect, exit_rect, skin_rect, theme_rect

def main_menu(current_skin,theme):
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    run=True
    in_skin_menu= False
    in_theme_menu = False
    global max_score
    global frame_count
    global gold
    while run:
        
        frame_count+=1
        if in_skin_menu:
            skin_rects= skin_menu(win,gold,theme)
        elif in_theme_menu:
            theme_rects= theme_menu(win,gold,theme)
        else:
            play_rect, exit_rect, skin_rect, theme_rect = draw_menu(win, max_score,frame_count, current_skin, theme, gold)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(max_score,gold,current_skin,theme)
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                main(current_skin,theme)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if in_skin_menu:
                    for skin_name, rect in skin_rects.items():
                        if rect.collidepoint(mx, my):
                            if OWNED.get(skin_name):
                                current_skin = SKINS[skin_name]
                                in_skin_menu = False
                            else:
                                if gold>=PRICE.get(skin_name):
                                    gold -= PRICE.get(skin_name)
                                    OWNED[skin_name]=True
                elif in_theme_menu:
                    for theme_name, rect in theme_rects.items():
                        if rect.collidepoint(mx, my):
                            if OWNED.get(theme_name):
                                theme = theme_name
                                in_theme_menu = False
                            else:
                                if gold>=PRICE.get(theme_name):
                                    gold -= PRICE.get(theme_name)
                                    OWNED[theme_name]=True
                else:  
                    if skin_rect.collidepoint(mx, my):
                        in_skin_menu=True
                    if theme_rect.collidepoint(mx, my):
                        in_theme_menu=True
                    if play_rect.collidepoint(mx, my):
                        main(current_skin,theme)
                    if exit_rect.collidepoint(mx, my):
                        save(max_score,gold,current_skin,theme)
                        pygame.quit()
                        sys.exit()

def main(current_skin,theme):
    bird= Bird(200,300,current_skin) #230,300
    base= Base(730,theme)
    pipes=[Pipe(700,theme)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    score=0
    global max_score
    global gold
    last_time = time.time()
    run=True
    while run:
        dt=time.time() - last_time
        last_time = time.time()
        dt*=30
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(max_score , gold,current_skin,theme)
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w) or  (event.key == pygame.K_SPACE) :
                    bird.jump()
                
        bird.move(dt)
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

            pipe.move(dt)

        if add_pipe:
            score+=1
            gold+=1
            if score<=70:
                pipes.append(Pipe(700-(2*score),theme))
            else:
                pipes.append(Pipe(560,theme))
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >=730 or bird.y <0:
            run = False
        base.move(dt)
        draw_window(win,bird,pipes, base,score,max_score,theme, gold)
        
        if score>max_score:
            max_score=score

    main_menu(current_skin,theme)

main_menu(current_skin,theme)




