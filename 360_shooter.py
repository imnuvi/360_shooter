import pygame, math, random
import sys

pygame.init()

FPS = 30
Width = 800
Height = 800
screen = pygame.display.set_mode((Width,Height))
clock = pygame.time.Clock()
font = pygame.font.SysFont('ubuntu',18, bold = True)
p_surface = pygame.image.load('spaceship_small.jpg')


class Player():
    def __init__(self, surface, xpos, ypos, color, colorkey, size):
        global p_surface
        self.pl = surface
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        # self.pl.fill(color)
        self.pl.set_colorkey(colorkey)
        self.rect = self.pl.get_rect()
        self.rect.center = (self.xpos,self.ypos)
        self.angle = 0
        self.alive = True
    def update(self,parent):
        parent.blit(self.newpl,self.rect)
    def rotate(self,newangle):
        # change = abs(newangle-self.angle)
        old_center = self.rect.center
        self.newpl = pygame.transform.rotate(self.pl,newangle)
        self.angle = newangle
        self.rect = self.newpl.get_rect()
        # self.pl = newpl
        self.rect.center = old_center
        # pygame.draw.rect(screen, Blue, self.rect)
class enemy():
    def __init__(self, color, shape, size, vel, aim):
        self.color = color
        self.alive = True
        self.size = size
        self.shape = shape
        self.spawn_point = [0,0]
        self.vel = vel
        self.vel_x = 0
        self.vel_y = 0
        self.aim = aim
        self.current_point = self.spawn_point
    def spawn(self):
        direction = random.choice(["top","bottom","left","right"])
        x_spawn = random.randrange(1,Width)
        y_spawn = random.randrange(1,Height)
        spawn_vel = 2
        if direction == "top":
            spawn_point = (x_spawn,0)
        elif direction == "bottom":
            spawn_point = (x_spawn,Height)
        elif direction == "left":
            spawn_point = (0,y_spawn)
        elif direction == "right":
            spawn_point = (Width,y_spawn)
        self.spawn_point = list(spawn_point)
        s = self.spawn_point
        self.vel_x = float((self.aim[0]-s[0]))/self.vel
        self.vel_y = float((self.aim[1]-s[1]))/self.vel

    def move_one_step(self,endpos):
        s = self.spawn_point
        dx = int(s[0]+self.vel_x)
        dy = int(s[1]+self.vel_y)
        self.current_point = [dx,dy]
        s[0] = s[0]+self.vel_x
        s[1] = s[1]+self.vel_y
        self.spawn_point = [s[0],s[1]]

    def disp(self):
        if self.alive == True:
            if self.shape == "circle":
                pygame.draw.circle(screen,self.color,tuple(self.current_point),self.size)
                pygame.draw.circle(screen,Black,tuple(self.current_point),self.size//2)
            # elif self.shape == "square":
            #     pygame.draw.rect(screen,self.color,(self.current_point[0]-self.size*2,self.current_point[1]-self.size*2,self.size*2,self.size*2))
            #     # pygame.draw.rect(screen,Black,(self.current_point[0]-self.size,self.current_point[1]-self.size,self.size,self.size))
def add_enemy(enemy):
    enemy_list.append(enemy)

def add_score():
    global score_count
    score_count += 1

def bullet_collision(aim_angle):
    global enemy_list, angle_diff
    for i in enemy_list:
        if (angle(i.spawn_point[0],i.spawn_point[1])-angle_diff < aim_angle < angle(i.spawn_point[0],i.spawn_point[1])+angle_diff):
            add_score()
            i.alive = False

def check_collision(enemy,player):
    global game_over, playerpos
    if (player.xpos-player.size[0]//2-enemy.size <= enemy.current_point[0] <=  player.xpos+player.size[0]//2+enemy.size) and (player.ypos-player.size[1]//2-enemy.size <= enemy.current_point[1] <=  player.ypos+player.size[1]//2+enemy.size):
        # game_over = True
        enemy.alive = False
        player.alive = False
        restart()
    else:
        game_over = False
def update_enemies(enemy_list):
    for loc,i in enumerate(enemy_list):
        if i.alive == False:
            enemy_list.pop(loc)
        i.move_one_step(playerpos)
        i.disp()
        check_collision(i,p1)


def angle(aim_x,aim_y):
    x_len = abs(aim_x-Width//2)
    y_len = abs(aim_y-Height//2)
    if x_len ==0 or y_len == 0:
        aim_angle = 0
    else:
        aim_angle = (math.atan(x_len/y_len) * 180)/math.pi
    if aim_x > Width/2 and aim_y<Height/2:
        # quadrant 1
        aim_angle = 90 - aim_angle
    elif aim_x < Width/2 and aim_y<Height/2:
        # quadrant 2
        aim_angle += 90
    elif aim_x< Width/2 and aim_y>Height/2:
        # quadrant 3
        aim_angle = 180 + 90 - aim_angle
    elif aim_x > Width/2 and aim_y>Height/2:
        # quadrant 4
        aim_angle += 270
    return aim_angle

def gen_col():
    return (random.randint(50,255),random.randint(50,255),random.randint(50,255))
def shoot(event):
    shoot_x = event.pos[0]
    shoot_y = event.pos[1]
    aim_angle = angle(shoot_x,shoot_y)
    draw_end(aim_angle)
    # screen.fill(White)
    bullet_collision(aim_angle)
    pygame.display.update()

def draw_end(angle):
    map_center = [x-Width//2,y-Height//2]
    radius = math.sqrt((Height//2)**2 + (Width//2)**2)

    map_zero_degrees = [565,0]
    theta = math.radians(360-angle)

    u = map_zero_degrees[0]*math.cos(theta) + map_zero_degrees[1]*math.sin(theta)
    v = -map_zero_degrees[0]*math.sin(theta) + map_zero_degrees[1]*math.cos(theta)

    new_pos = [u+Width//2,-(v-Height//2)]
    pygame.draw.line(screen, White,(400,400),tuple(new_pos),2)

def display_score(score):
    # global surface
    txt = font.render("SCORE",True,White,Black)
    txt_rect = txt.get_rect()
    txt_rect.center = (Width//2,100)
    screen.blit(txt,txt_rect)
    score_text = font.render(str(score),True,White,Black)
    score_rect = score_text.get_rect()
    score_rect.center = text_center
    screen.blit(score_text,score_rect)
    pygame.display.update()

def restart():
    global Blue,Black,Red,White,playerpos,x,y,playersize,game_over,aim_x,aim_y,aim_angle,speed,spawn_val,angle_diff,score_count,text_center,p1,e1,enemy_list,count
    Blue = (5,70,240)
    Black = (0,0,0)
    Red = (240,50,80)
    White = (255,255,255)

    playerpos = x,y = 400 , 400
    playersize = (40,40)


    game_over = False
    aim_x = 400
    aim_y = 400
    aim_angle = 180
    speed = 100
    spawn_val = 50
    angle_diff = 2

    score_count = 0
    text_center = (Width//2,150)

    # p_surface = pygame.Surface((40,40))


    p1 = Player(p_surface,400,400,Blue,Black,playersize)



    e1 = enemy(Red,"circle",10,100,playerpos)
    e1.spawn()
    enemy_list = [e1]

    count = 0

    while not game_over:
        change = clock.tick(FPS)
        screen.fill(Black)
        display_score(score_count)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                break
            shoot_yes = False

            if event.type == 4:
                # print(event.pos)
                aim_x = event.pos[0]
                aim_y = event.pos[1]
                aim_angle = angle(aim_x,aim_y)
            if event.type == 5:
                shoot(event)
        
        count = change + count
        
        if count > FPS*spawn_val:
            col = gen_col()
            e = enemy(col,"circle",10,100,playerpos)
            e.spawn()
            enemy_list.append(e)
            count = 0
            if spawn_val > 15:
                spawn_val -= 1

        update_enemies(enemy_list)

        p1.rotate(aim_angle)
        p1.update(screen)
        pygame.display.flip()


restart()