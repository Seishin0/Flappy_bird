import neat.population
import neat.statistics
import pygame
import time 
import neat
import os 
import random
pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Flappy_bird\\imgs","bg.png")))

Points = pygame.font.SysFont("Consolas", 40)
MENU_FONT = pygame.font.SysFont("Consolas", 70)
generation = 0

class Bird:
    imgs = BIRD_IMGS
    max_rotation = 25
    rot_vel=20
    animation_time = 5 
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
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

def draw_window(win, birds, pipes, base, score, generation):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    point = Points.render("Score: "+str(score),1,(255,255,255))
    gen = Points.render("Gen: "+str(generation),1,(255,255,255))
    win.blit(point,(WIN_WIDTH - 10 - point.get_width(),10))
    win.blit(gen,(10 ,10))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
    

def main(genomes, config):
    nets=[]
    gen=[]
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200,300))
        g.fitness=0
        gen.append(g)

    base= Base(730)
    pipes=[Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    score=0
    global generation
    generation +=1

    run=True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds)>0:
            if len(pipes)>1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind=1
        else:
            run = False
            break

        for x,bird in enumerate(birds):
            bird.move()
            gen[x].fitness+=0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0]>0.5:
                bird.jump()
            
        
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.colldie(bird):
                    birds.pop(x)
                    nets.pop(x)
                    gen.pop(x)

                if not pipe.passed and pipe.x<bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.pipe_top.get_width()<0:
                rem.append(pipe)            

            pipe.move()

        if add_pipe:
            score+=1
            for g in gen:
                g.fitness+=5

            pipes.append(Pipe(700))
        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >=730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                gen.pop(x)


        if score>100:
            break
        base.move()
        draw_window(win,birds,pipes, base,score,generation)
        



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    winner = pop.run(main,50)

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)