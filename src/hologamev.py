# title:   HoloGameV
# author:  AILab-FOI
# desc:    short description
# site:    https://ai.foi.hr
# license: GPLv3
# version: 0.1
# script:  python


import random

state='menu' #varijabla za game state
level = 0 # koji level je ucitan (od 0 pa na dalje)
hacked_enemy = None
player_backup = None
hack_start_level = None
show_instructions = False
confetti = [ [random.randint(0,239), random.randint(-30,0), random.choice([6,11,12,1,2,15,5]), random.uniform(0.5,2.0)] for _ in range(30) ]

def TIC():
    update_keys()

    Final()

    global state
    global show_instructions

    if state=='game':
        IgrajLevel()
        if key_instruction:
            show_instructions = not show_instructions
        print("Press Select or 'O' for instructions", 5, 12, 12, False, 1, True)
        if show_instructions:
            # popup prozor
            rect(5, 10, 230, 52, 0)    # crna pozadina
            rectb(5, 10, 230, 52, 12)  # bijeli okvir

            # upute 
            print("Move - controller Arrows | keyboard 'AD'", 10, 15, 12, False, 1, True)
            print("Climb - controller Arrows | keyboard 'WS'", 10, 24, 12, False, 1, True)
            print("Jump - controller (B) | keyboard 'space'", 10, 33, 12, False, 1, True)
            print("Shoot - controller (A) | keyboard 'F'", 10, 42, 12, False, 1, True)
            print("Dash - keyboard 'shift'", 10, 51, 12, False, 1, True)
    if state=='menu':
        menu.Menu()
    elif state=='over':
        menu.EndScreen("GAME OVER", "Press START (space) for restart")
    elif state=='win':
        player.RestoreHealth(player)
        menu.EndScreen("YOU WON!", "Press START (space) for exit")

def Final():
	cls(13) 

prev_key_space = False
key_instruction = False
prev_key_instruction = False

def update_keys():
    global key_space, key_left, key_right, key_up, key_down, key_shoot, key_dash, key_hack, key_return, key_selfdestruct 
    global prev_key_space, prev_key_dash
    global key_instruction, prev_key_instruction

    current_key_space = key(48) # 'SPACE' ili 'START' ili 'B' na gamepadu (prirodno skakati na B, a birati na 'START')
    current_key_dash = key(64)
    current_key_instruction = key(15) # 'O' ili 'SELECT' na gamepadu

    key_space = current_key_space and not prev_key_space
    key_dash = current_key_dash and not prev_key_dash
    key_instruction = current_key_instruction and not prev_key_instruction

    key_left = key(1) # 'A' ili lijevo na gamepadu
    key_right = key(4) # 'D' ili desno na gamepadu
    key_up = key(23) # 'W' ili gore na gamepadu
    key_down = key(19) # 'S' ili dolje na gamepadu
    key_shoot = key(6) # 'F' ili 'A' na gamepadu
    key_hack = key(8) # 'H'
    key_selfdestruct = key(7) # 'G'
    key_return = key(18) #'R'
    prev_key_space = current_key_space
    prev_key_dash = current_key_dash
    prev_key_instruction = current_key_instruction
class collidable:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.draw_self()

    def check_collision(self, other):
        if self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y:
            return True
        return False

    def check_collision_rectangle(self, xleft, ytop, xright, ybottom):
        if self.x < xright and self.x + self.width > xleft and self.y < ybottom and self.y + self.height > ytop:
            return True
        return False

    def draw_self(self):
        rect(self.x - int(pogled.x), self.y - int(pogled.y), self.width, self.height, 15)


def DefinirajKolizije(listaObjekata, level, level_height):
    collidables = {}
    # ako objekt nije lista prvi dio koda se raunna, inace je drugi (else)
    tile_size = 8
    for objekt in listaObjekata:
      sirinaKolizija = 8
      if not isinstance (objekt, list):
        px = min(max(int(objekt.x/tile_size) - round(sirinaKolizija/2), 0), 239)
        py = min(max(int(objekt.y/tile_size) - round(sirinaKolizija/2), 0), 135)

        for xx in range(sirinaKolizija):
            for yy in range(sirinaKolizija):
                tileHere = mget(xx + px, yy + py + level*level_height)
                if tileHere != 0 and tileHere not in level_finish_tile_indexes and tileHere not in locked_door_tile_indexes and tileHere not in background_tile_indexes:
                    pos_key = ("x", xx + px, "y", yy + py)
                    if pos_key not in collidables:
                        collidables[pos_key] = collidable((xx + px)*tile_size, (yy + py)*tile_size, tile_size, tile_size)
      else:
          for obj in objekt:
              px = min(max(int(obj.x/tile_size) - round(sirinaKolizija/2), 0), 239)
              py = min(max(int(obj.y/tile_size) - round(sirinaKolizija/2), 0), 135)

              for xx in range(sirinaKolizija):
               for yy in range(sirinaKolizija):
                tileHere = mget(xx + px, yy + py + level*level_height)
                if tileHere != 0 and tileHere not in level_finish_tile_indexes and tileHere not in locked_door_tile_indexes and tileHere not in background_tile_indexes:
                    pos_key = ("x", xx + px, "y", yy + py)
                    if pos_key not in collidables:
                        collidables[pos_key] = collidable((xx + px)*tile_size, (yy + py)*tile_size, tile_size, tile_size)

    return list(collidables.values())

def pomakni(a, b, vrijednost):
    if vrijednost == 0:
        return a
    elif a < b:
        return min(a + vrijednost, b)
    else:
        return max(a - vrijednost, b)

ladder_tile_indexes = [
    13, 14, 29, 30, 45, 46, 61, 62
]

class player: 
    x=96
    y=24
    width=14
    height=14
    hsp=0
    vsp=0
    desno=False
    is_walking = False
    frame = 256
    shootTimer=0
    skok=0
    coll=[]
    spriteTimer = 0
    on_ladders = False
    on_ground = False
    dash_timer = 0 
    def ProvjeriKolizije(self, xdodatak, ydodatak):
        self.x += xdodatak
        self.y += ydodatak
        for obj in self.coll:
            if obj.check_collision(self):
                self.x -= xdodatak
                self.y -= ydodatak
                return True
        self.x -= xdodatak
        self.y -= ydodatak
        return False
    
    minY=120 #najniza tocka
    minX=10000 #najdesnija tocka

    #Osnovne Varijable
    acc_normal = 0.25
    acc_ladders = 1
    akceleracija = 0.25
    maxBrzina=2
    gravitacija=0.24


    #Varijable skakanja
    skokJacina=4.4
    
    #Koyote time
    coyoteTime=7
    ctVar=0
    jumped=False

    #hp
    health = 15
    hitTimer = 10
    hitVar = 0
    enemyHit = False

 
    def PlayerKontroler(self, coll):
        global hacked_enemy, player_backup, hack_start_level
        self.coll=coll
        self.CheckOnLadders(self)
        player.Hitters(player, enemies)

        #promjena akceleracije ovisno o ljestvama
        if self.on_ladders:
            self.akceleracija = self.acc_ladders
        else:
            self.akceleracija = self.acc_normal

        #skakanje
        if key_space and self.vsp == 0: #<- ovo je manje bugged ali bez coyote time  #and not self.jumped:
            sfx(9, "C-4", 10, 0, 2, 0)
            if self.ProvjeriKolizije(self, 0, 1) or self.y>=self.minY or self.ctVar < self.coyoteTime or self.on_ladders or self.on_ground:
                self.vsp = -self.skokJacina
                self.jumped = True
                self.on_ladders = False

        #coyote time
        if not self.on_ladders:
            if self.ProvjeriKolizije(self, 0, 1):
                self.ctVar = 0
                self.jumped = False
            else:
                self.ctVar += 1
        

        #kretanje lijevo desno
        if key_left: 
            self.hsp=pomakni(self.hsp,-self.maxBrzina,self.akceleracija)
            self.desno=False
            self.is_walking = True
        elif key_right:
            self.hsp=pomakni(self.hsp,self.maxBrzina,self.akceleracija)
            self.is_walking = True
            self.desno=True
        else:
            self.hsp=pomakni(self.hsp,0,self.akceleracija)
            self.is_walking = False
        

        #dash   
        if key_dash and self.dash_timer == 0:  
            dash_speed = 5
            if self.desno:
                self.hsp = dash_speed
            else:
                self.hsp = -dash_speed
            self.dash_timer = 60

        # smanji timer na dash-u
        if self.dash_timer > 0:
            self.dash_timer -= 1  
            if self.dash_timer == 0:
                self.hsp = 0

        #gravitacija i kolizije
        if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(self, 0, self.vsp + 1):
            if self.vsp > 0:
                while self.y<self.minY and not self.ProvjeriKolizije(self, 0, 1):
                    self.y+=1
            self.vsp=0
        else:
            if not self.on_ladders:
                self.vsp=self.vsp+self.gravitacija
                if self.ProvjeriKolizije(self, 0, self.vsp):
                    self.vsp = 0

        if self.vsp<0:
            if self.ProvjeriKolizije(self, 0, self.vsp - 1):
                self.vsp=0


        #pomicanje po ljestvama
        if self.on_ladders:
            if key_up: 
                self.vsp=pomakni(self.vsp,-self.maxBrzina,self.akceleracija)
            elif key_down:
                self.vsp=pomakni(self.vsp,self.maxBrzina,self.akceleracija)
            else:
                self.vsp=pomakni(self.vsp,0,self.akceleracija)
            
            if self.ProvjeriKolizije(self, 0, self.vsp) or self.y + self.vsp >= self.minY:
                self.vsp=0

        #blokiranje lijevo i desno
        if self.x>(pogled.ogranicenjeX - self.width) or self.ProvjeriKolizije(self, 1+self.hsp, 0):
            self.hsp=0
            while self.x > (pogled.ogranicenjeX - self.width):
                self.x-=1
            
        if self.x<0 or self.ProvjeriKolizije(self, -1+self.hsp, 0):
            self.hsp=0
            while self.x < 0:
                self.x+=1

        self.x=self.x+self.hsp
        self.y=self.y+self.vsp

        if self.is_walking == True:
            self.spriteTimer += 0.1
        elif self.on_ladders:
            if key_up or key_down:
                self.spriteTimer += 0.1
        
        if key_hack:
            for enemys in enemies:
                for enemy in enemys:
                    if not enemy.dead and abs(self.x - enemy.x) < 16 and abs(self.y - enemy.y) < 16:
                        hacked_enemy = enemy
                        player_backup = player
                        hack_start_level = level 
                        return
        


        #renderanje spritea
        if self.on_ladders:
            spr(290 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
        else:
            if self.desno==True and self.is_walking==True:
                spr(258 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
            elif self.desno==False and self.is_walking==True:
                spr(258 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)
            else:
                spr(self.frame,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,int(self.desno==False),0,2,2)

        if hacked_enemy:
            return  # Skip player control if we're hacked into an enemy

        if self.hitTimer > self.hitVar:
            self.hitVar += 1
            if self.desno==True and self.is_walking==True:
                spr(266 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
            elif self.desno==False and self.is_walking==True:
                spr(266 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)
            else:
                spr(266,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,int(self.desno==False),0,2,2)

        self.UnStuck(self)
     
    def Pogoden(self, dmg):
        global state
        self.health -= dmg
        self.hitVar = 0
        if self.health < 1:
            sfx(8, "C-4", 30, 0, 5, 0)
            state = 'over'

    def CheckOnLadders(self):
        if self.on_ladders:
            for i in range(0, int(self.width), int(self.width/2)):
                for j in range(0, int(self.height), int(self.height/2)):
                    if mget(round((self.x + i)/8), round((self.y + j)/8) + level*LEVEL_HEIGHT) in ladder_tile_indexes:
                        return
            self.on_ladders = False
        else:
            if not key_up and not key_down:
                return
            for i in range(0, int(self.width), int(self.width/2)):
                for j in range(0, int(self.height), int(self.height/2)):
                    if mget(round((self.x + i)/8), round((self.y + j)/8) + level*LEVEL_HEIGHT) in ladder_tile_indexes:
                        self.on_ladders = True

    def UnStuck(self):
        if self.ProvjeriKolizije(self, 0, 0):
            for skok in range (1, 3):
                for i in range (-skok, skok, skok):
                    for j in range (-skok, skok, skok):
                        if i == 0 and j == 0:
                            continue
                        if not self.ProvjeriKolizije(self, i, j):
                            self.x += i
                            self.y += j
                            return
                        
    def Hitters(self, enemies):
        hitt = False
        for enemys in enemies:
            for enemy in enemys:
                if player.x < enemy.x + enemy.width and player.y < enemy.y + enemy.height and player.x > enemy.x - enemy.width and player.y > enemy.y - enemy.height:
                    if not player.enemyHit and not enemy.dead:
                        player.Pogoden(player, 1)
                    player.enemyHit = True
                    hitt = True
        if not hitt:
            player.enemyHit = False

    def RestoreHealth(self):
        self.health = 15

#lista projektila
projectiles = []
def HackedEnemyController(enemy, coll):
    enemy.coll = coll
    global hacked_enemy, player_backup, level
    if key_left:
        enemy.x -= 2
        enemy.desno = False
    elif key_right:
        enemy.x += 2
        enemy.desno = True
    if key_up:
        enemy.y -= 2
    elif key_down:
        enemy.y += 2
    if key_selfdestruct:
        sfx(8, "C-4", 20, 0, 5, 0)
        enemy.dead = True
        ReturnToPlayer()
    if key_return:
        ReturnToPlayer() 
    tile_size = 8
    teleport_tile_index = 145  
    desired_x, desired_y = 78, 28 

    center_x = int((enemy.x + enemy.width // 2) / tile_size)
    foot_y   = int((enemy.y + enemy.height - 1) / tile_size)
    map_y = foot_y + level * LEVEL_HEIGHT
    tile_under = mget(center_x, map_y)
    print(f"[DEBUG] Enemy Tile: index={tile_under} at ({center_x}, {foot_y})")
    if tile_under == teleport_tile_index:
        level += 1
        ZapocniLevel(level)
        enemy.x = desired_x * tile_size
        enemy.y = (desired_y - level * LEVEL_HEIGHT) * tile_size
    enemy.vsp += enemy.gravitacija
    tile_size = 8

def ReturnToPlayer():
    global hacked_enemy, player, player_backup, level, hack_start_level
    hacked_enemy = None

    if player_backup:
        player = player_backup

    if hack_start_level is not None and level != hack_start_level:
        level = hack_start_level
        ZapocniLevel(level)

    hack_start_level = None

def RenderInactivePlayer():
    spr(256, int(player.x) - int(pogled.x), int(player.y) - int(pogled.y), 14, 1, 0, 0, 2, 2)        

class Enemy:
  x = 90 
  y = 90
  width = 16
  height = 16
  sprite = 1  
  dx = -1  
  vsp = 0
  gravitacija = 0.3
  skokJacina = 3
  minY = 120
  desno = False
  shotTimer = 0  # timer za pucanje
  shotFreq = 2 # koliko cesto puca
  coll = []
  health = 2
  dead = False

  def __init__(self, x, y, min_x=None, max_x=None):
    tile_size = 8
    self.x = x*tile_size
    self.y = y*tile_size
    self.min_x = min_x*tile_size if min_x is not None else 0
    self.max_x = max_x*tile_size if max_x is not None else pogled.ogranicenjeX

  def movement(self, coll):
    self.coll = coll
     
    if hacked_enemy != self:
        self.x = self.x + self.dx  
        if not self.dead and self.ProvjeriKolizije(6*self.dx, 0):
            if not self.ProvjeriKolizije(3*self.dx, -9):
                if self.ProvjeriKolizije(0, 1):
                    self.vsp = -self.skokJacina
                else:
                    self.dx = -self.dx
                    self.desno = not self.desno
        elif not self.dead and self.ProvjeriKolizije(3*self.dx, 0):
            self.dx = -self.dx
            self.desno = not self.desno
        if not self.dead and self.x <= self.min_x:
            self.dx = 1  # mijenja stranu kad takne lijevu stranu
            self.desno = True
        elif not self.dead and self.x >= self.max_x:
            self.dx = -1  # mijenja stranu kad takne desnu stranu
            self.desno = False

        self.shotTimer += 1  # svaki frame se povecava za 1

    # gravitacija
    if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(0, self.vsp + 1):
      self.vsp=0
      while self.y<self.minY and not self.ProvjeriKolizije(0, 1):
        self.y+=1
    else:
      self.vsp=self.vsp+self.gravitacija

    if self.vsp<0:
      if self.ProvjeriKolizije(0, self.vsp - 1):
        self.vsp=0

    self.y = self.y + self.vsp

    # puca svakih dvije sekunde
    if not self.dead and self.shotTimer >= 60 * self.shotFreq:
      self.shootProjectile()  # poziv funkcije za pucanje
      self.shotTimer = 0  # resetiranje timera

    #crtanje samog sebe
    if not self.dead and self.desno==True:
      spr(320,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
    elif not self.dead:
      spr(320,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)


  def render(self):#samo za kada je enemy hakiran
    if self.dead:
        return
    if self.desno:
        spr(320, int(self.x) - int(pogled.x), int(self.y) - int(pogled.y), 15, 1, 0, 0, 2, 2)
    else:
        spr(320, int(self.x) - int(pogled.x), int(self.y) - int(pogled.y), 15, 1, 1, 0, 2, 2)
  def shootProjectile(self):
    projectile = Projectile(self.x + 5, int(self.y)) 

    projectile.desno = self.desno
    # doda projektil u listu
    projectiles.append(projectile)
    sfx(7, "D-2", 3, 0, 2, 3)

  def ProvjeriKolizije(self, xdodatak, ydodatak):
    self.x += xdodatak
    self.y += ydodatak
    for obj in self.coll:
      if obj.check_collision(self):
        self.x -= xdodatak
        self.y -= ydodatak
        return True
    self.x -= xdodatak
    self.y -= ydodatak
    return False
  
  def Pogoden(self, damage, removeInt):
    self.health = self.health - damage
    if self.health < 1:
      self.dead = True

class Projectile:
  x=0
  y=0
    
  width=4
  height=4
  
  def __init__(self, x, y, _speed = 5):  # konstruktor klase
    self.x = x
    self.y = y
    self.dx = 1 
    self.dy = 0
    self.speed = _speed  # brzina projektila
    self.desno = True
    self.width = 4
    self.height = 4
  
  def movement(self):
    if self.desno == True:
      self.x = self.x + self.speed
    else:
      self.x = self.x - self.speed

    #crtanje sebe
    spr(363, self.x - int(pogled.x), self.y - int(pogled.y), 0, 1, 0, 0, 1, 1)
      
  def MetakCheck(metak, colls):
            metak.coll=colls
            # metak se unisti
            if metak.x < 0 or metak.x > pogled.ogranicenjeX or Projectile.ProvjeriKolizije(metak, 0, 1):
                if metak in projectiles:
                    projectiles.remove(metak)
                    del metak
                else:
                    del metak
            elif metak.x < player.x + player.width and metak.y < player.y + player.height and metak.x > player.x - player.width + 8 and metak.y > player.y - player.height:
                if metak in projectiles:
                    player.Pogoden(player, 1) # damage ovdje ide ako cemo ga mijenjati 
                    projectiles.remove(metak)
                    del metak
                else:
                    del metak
            # ako je pogoden player (elif)
              
    
  # 1-2.-3 5---8.---11
    
  def ProvjeriKolizije(self, xdodatak, ydodatak):
        self.x += xdodatak
        self.y += ydodatak
        for obj in self.coll:
            if obj.check_collision(self):
                self.x -= xdodatak
                self.y -= ydodatak
                return True
        self.x -= xdodatak
        self.y -= ydodatak
        return False
     
#lista projektila
projectiles = []

class Enemy2(Enemy):
  x = 90 
  y = 90
  width = 16
  height = 16
  sprite = 1  
  dx = -1  
  vsp = 0
  gravitacija = 0.3
  skokJacina = 4
  minY = 120
  desno = False
  shotTimer = 0  # timer za pucanje
  shotFreq = 1 # koliko cesto puca
  coll = []
  health = 4

  def __init__(self, x, y, min_x=None, max_x=None):
    tile_size = 8
    self.x = x*tile_size
    self.y = y*tile_size
    self.min_x = min_x*tile_size if min_x is not None else 0
    self.max_x = max_x*tile_size if max_x is not None else pogled.ogranicenjeX

  def movement(self, coll):
    self.coll = coll
    self.x = self.x + self.dx
    if not self.dead and self.ProvjeriKolizije(6*self.dx, 0):
      if not self.ProvjeriKolizije(3*self.dx, -9):
        if self.ProvjeriKolizije(0, 1):
          self.vsp = -self.skokJacina
        else:
          self.dx = -self.dx
          self.desno = not self.desno
    elif not self.dead and self.ProvjeriKolizije(3*self.dx, 0):
      self.dx = -self.dx
      self.desno = not self.desno
    if not self.dead and self.x <= self.min_x:
      self.dx = 1  # mijenja stranu kad takne lijevu stranu
      self.desno = True
    elif not self.dead and self.x >= self.max_x:
      self.dx = -1  # mijenja stranu kad takne desnu stranu
      self.desno = False
      

    self.shotTimer += 1  # svaki frame se povecava za 1

    # gravitacija
    if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(0, self.vsp + 1):
      self.vsp=0
      while self.y<self.minY and not self.ProvjeriKolizije(0, 1):
        self.y+=1
    else:
      self.vsp=self.vsp+self.gravitacija

    if self.vsp<0:
      if self.ProvjeriKolizije(0, self.vsp - 1):
        self.vsp=0

    self.y = self.y + self.vsp

    # puca svakih 1 sekundu
    if not self.dead and self.shotTimer >= 60 * self.shotFreq:
      self.shootProjectile()  # poziv funkcije za pucanje
      self.shotTimer = 0  # resetiranje timera

    #crtanje samog sebe
    if not self.dead and self.desno==True:
      spr(330,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
    elif not self.dead:
      spr(330,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)

  def shootProjectile(self):
    projectile = Projectile(self.x + 5, int(self.y)) 

    projectile.desno = self.desno
    # doda projektil u listu
    projectiles.append(projectile)

    sfx(10, "E-4", 3, 0, 2, 3)

  def ProvjeriKolizije(self, xdodatak, ydodatak):
    self.x += xdodatak
    self.y += ydodatak
    for obj in self.coll:
      if obj.check_collision(self):
        self.x -= xdodatak
        self.y -= ydodatak
        return True
    self.x -= xdodatak
    self.y -= ydodatak
    return False
  
  def Pogoden(self, damage, removeInt):
    self.health = self.health - damage
    if self.health < 1:
      self.dead = True
#lista projektila
projectiles = []

class Enemy3(Enemy):
  x = 90 
  y = 90
  width = 16
  height = 16
  sprite = 1  
  dx = -1  
  vsp = 0
  gravitacija = 0.3
  skokJacina = 3
  minY = 120
  desno = False
  shotTimer = 0  # timer za pucanje
  shotFreq = 2 # koliko cesto puca
  coll = []
  health = 6

  def __init__(self, x, y, min_x=None, max_x=None):
    tile_size = 8
    self.x = x*tile_size
    self.y = y*tile_size
    self.min_x = min_x*tile_size if min_x is not None else 0
    self.max_x = max_x*tile_size if max_x is not None else pogled.ogranicenjeX

  def movement(self, coll):
    self.coll = coll
    self.x = self.x + self.dx
    if not self.dead and self.ProvjeriKolizije(6*self.dx, 0):
      if not self.ProvjeriKolizije(3*self.dx, -9):
        if self.ProvjeriKolizije(0, 1):
          self.vsp = -self.skokJacina
        else:
          self.dx = -self.dx
          self.desno = not self.desno
    elif not self.dead and self.ProvjeriKolizije(3*self.dx, 0):
      self.dx = -self.dx
      self.desno = not self.desno
    if not self.dead and self.x <= self.min_x:
      self.dx = 1  # mijenja stranu kad takne lijevu stranu
      self.desno = True
    elif not self.dead and self.x >= self.max_x:
      self.dx = -1  # mijenja stranu kad takne desnu stranu
      self.desno = False

    self.shotTimer += 1  # svaki frame se povecava za 1

    # gravitacija
    if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(0, self.vsp + 1):
      self.vsp=0
      while self.y<self.minY and not self.ProvjeriKolizije(0, 1):
        self.y+=1
    else:
      self.vsp=self.vsp+self.gravitacija

    if self.vsp<0:
      if self.ProvjeriKolizije(0, self.vsp - 1):
        self.vsp=0

    self.y = self.y + self.vsp

    # puca svakih dvije sekunde
    if not self.dead and self.shotTimer >= 60 * self.shotFreq:
      self.shootProjectile()  # poziv funkcije za pucanje
      self.shotTimer = 0  # resetiranje timera

    #crtanje samog sebe
    if not self.dead and self.desno==True:
      spr(396,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
    elif not self.dead:
      spr(396,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)

  def shootProjectile(self):
    projectile = Projectile(self.x + 5, int(self.y), 3) 

    projectile.desno = self.desno
    # doda projektil u listu
    projectiles.append(projectile)

    sfx(7, "C-4", 3, 0, 2, 3)

class FinalBoss(Enemy):
  x = 90 
  y = 90
  width = 32
  height = 32
  sprite = 1  
  dx = -1  
  vsp = 0
  gravitacija = 0.3
  skokJacina = 3
  minY = 89
  desno = False
  shotTimer = 0  # timer za pucanje
  shotFreq = 1 # koliko cesto puca
  coll = []
  health = 30

  def __init__(self, x, y, min_x=None, max_x=None):
    tile_size = 8
    self.x = x*tile_size
    self.y = (y-3)*tile_size
    self.min_x = min_x*tile_size if min_x is not None else 0
    self.max_x = max_x*tile_size if max_x is not None else pogled.ogranicenjeX

  def movement(self, coll):
    self.coll = coll
    self.x = self.x + self.dx
    if not self.dead and self.ProvjeriKolizije(6*self.dx, 0):
      if not self.ProvjeriKolizije(3*self.dx, -9):
        if self.ProvjeriKolizije(0, 1):
          self.vsp = -self.skokJacina
        else:
          self.dx = -self.dx
          self.desno = not self.desno
    elif not self.dead and self.ProvjeriKolizije(3*self.dx, 0):
      self.dx = -self.dx
      self.desno = not self.desno
    if not self.dead and self.x <= self.min_x:
      self.dx = 1  # mijenja stranu kad takne lijevu stranu
      self.desno = True
    elif not self.dead and self.x >= self.max_x:
      self.dx = -1  # mijenja stranu kad takne desnu stranu
      self.desno = False

    self.shotTimer += 1  # svaki frame se povecava za 1

    # gravitacija
    if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(0, self.vsp + 1):
      self.vsp=0
      while self.y<self.minY and not self.ProvjeriKolizije(0, 1):
        self.y+=1
    else:
      self.vsp=self.vsp+self.gravitacija

    if self.vsp<0:
      if self.ProvjeriKolizije(0, self.vsp - 1):
        self.vsp=0

    self.y = self.y + self.vsp

    # puca svaku sekundu
    if not self.dead and self.shotTimer >= 60 * self.shotFreq:
      self.shootProjectile()  # poziv funkcije za pucanje
      self.shotTimer = 0  # resetiranje timera

    #crtanje samog sebe
    if not self.dead and self.desno==True:
      spr(426,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,4,4)
    elif not self.dead:
      spr(426,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,4,4)

  def shootProjectile(self):
    y_offset = 16
    projectile = Projectile(self.x + 5, int(self.y) + y_offset, 3) 
    projectile.desno = self.desno
    # doda projektil u listu
    projectiles.append(projectile)
    sfx(7, "C-4", 3, 0, 2, 3)

  def ProvjeriKolizije(self, xdodatak, ydodatak):
    self.x += xdodatak
    self.y += ydodatak
    for obj in self.coll:
      if obj.check_collision(self):
        self.x -= xdodatak
        self.y -= ydodatak
        return True
    self.x -= xdodatak
    self.y -= ydodatak
    return False
  
  def Pogoden(self, damage, removeInt):
    self.health = self.health - damage
    if self.health < 1:
        self.dead = True
        tileovi_za_ukloniti = [(236, 60), (236, 61), (236, 62), (236, 63), (236, 64), (236, 65), (235, 60), (235, 61), (235, 62), (235, 63), (235, 64), (235, 65)]
        for xy in tileovi_za_ukloniti:
            mset(xy[0], xy[1], 0)

def is_glitch():
    t = time() % 1500
    return t > 1430

class menu:
    m_ind=0

    def Menu():
        global state
        cls(0)
        menu.AnimateFrame()
        menu.AnimateTitle()

        # Opcije menija
        rect(45,58+10*menu.m_ind,150,10,11)
        if menu.m_ind == 0:
            print('PLAY', 106, 60, 0, False, 1, False)
        else:
            print('PLAY', 106, 60, 12, False, 1, False)

        if menu.m_ind == 1:
            print('QUIT', 106, 70, 0, False, 1, False)
        else:
            print('QUIT', 106, 70, 12, False, 1, False)

        #  Šetanje po opcijama na meniju
        if key_down and 48+10*menu.m_ind<50: #ako se budu dodavale još koje opcije, promijeniti uvjet
            menu.m_ind += 1
        elif key_up and 48+10*menu.m_ind>=50:
            menu.m_ind += -1

        # Odabir 
        if key_space and menu.m_ind==0:
            state = 'game'
            ZapocniLevel(level)
        elif key_space and menu.m_ind==1:
            exit()


    def AnimateTitle():
        t = time() % 1500  

        # glitch efekt traje 70ms svakih 1500ms
        if t > 1430:
            glitch_type = random.randint(1, 4)
            
            if glitch_type == 1:
                # nasumično se pomakne naslov i promijeni boja
                x = 33 + random.randint(-4, 4)
                y = 20 + random.randint(-2, 2)
                color = random.choice([10, 11, 12, 13, 2])
                print('CYBERTRACE', x, y, color, False, 3, False)
            
            elif glitch_type == 2:
                # zamjena slova 
                title = list('CYBERTRACE')
                for _ in range(random.randint(1, 3)):
                    idx = random.randint(0, len(title)-1)
                    title[idx] = random.choice(['#', '@', '!', '%', '3', '7', 'E', 'C'])
                print(''.join(title), 33, 20, 13, False, 3, False)
            
            elif glitch_type == 3:
                # ispis naslova u različitim bojama i pomacima (shadow efekt)
                for dx in [-2, 2]:
                    for dy in [-1, 1]:
                        print('CYBERTRACE', 33+dx, 20+dy, random.choice([10, 11, 12]), False, 3, False)
                print('CYBERTRACE', 33, 20, 12, False, 3, False)
            
            elif glitch_type == 4:
                # flash efekt - bijela boja i pomak
                print('CYBERTRACE', 33+random.randint(-1,1), 20+random.randint(-1,1), 15, False, 3, False)
        
        else:
            # normalan naslov
            print('CYBERTRACE', 33, 20, 12, False, 3, False) 

    def AnimateFrame():
        rectb(0, 0, 240, 136, 11)

    def EndScreen(text, subtext):
        global state, confetti, level
        cls(0)
        font_size = 2
        char_width = 6 * font_size
        text_width = len(text) * char_width
        x = (240 - text_width) // 2
        y = 50

        base_color = 6 if (time() % 500 > 250) else 12
        sub_x = 32

        if text == "YOU WON!":
            base_color = 11 if (time() % 500 > 250) else 12
            sub_x = 40
            music(4,0,-1)


        if is_glitch():
            glitch_type = random.randint(1, 3)
            if glitch_type == 1:
                # pomak i boja
                gx = x + random.randint(-4, 4)
                gy = y + random.randint(-2, 2)
                color = random.choice([2, 4, 7, 15])
                print(text, gx, gy, color, False, font_size, False)
            elif glitch_type == 2:
                # zamjena slova
                title = list(text)
                for _ in range(random.randint(1, 3)):
                    idx = random.randint(0, len(title)-1)
                    if title[idx] != ' ':
                        title[idx] = random.choice(['#', '@', '!', '%', '0', 'V'])
                print(''.join(title), x, y, 7, False, font_size, False)
            elif glitch_type == 3:
                # shadow efekt
                for dx in [-2, 2]:
                    for dy in [-1, 1]:
                        print(text, x+dx, y+dy, random.choice([2, 4, 7]), False, font_size, False)
                print(text, x, y, base_color, False, font_size, False)
        else:
            # normalan prikaz
            print(text, x, y, base_color, False, font_size, False)

        # konfeti
        if text == "YOU WON!":
            for i in range(len(confetti)):
                cx, cy, cc, cspeed = confetti[i]
                pix(cx, int(cy), cc)
                confetti[i][1] += cspeed
                if confetti[i][1] > 140:
                    confetti[i][0] = random.randint(0,239)
                    confetti[i][1] = random.randint(-30,0)
                    confetti[i][2] = random.choice([6,11,12,1,2,15,5])
                    confetti[i][3] = random.uniform(0.5,2.0)

        sub_font_size = 1
        sub_y = 75
        print(subtext, sub_x, sub_y, 13, False, sub_font_size, False)

        if key_space and text == "GAME OVER":
            reset()
        elif key_space and text == "YOU WON!":
            level = 0
            state = 'menu'

class Pogled:
    x = 0
    y = 0
    w = 240
    h = 136
    ograniceno = False
    ogranicenjeX = 0

    def __init__(self):
        self.postaviOgranicenja(240*8) # maks velicina levela

    def prati(self, objekt):
        self.x = objekt.x - (self.w - objekt.width)/2

    def postaviOgranicenja(self, maxX):
        self.ograniceno = True
        self.ogranicenjeX = maxX

    def pratiIgraca(self):
        if player.is_walking:
            self.x = round(player.x - (self.w - player.width)/2)

        if self.ograniceno:
            self.x = min(max(0, self.x), self.ogranicenjeX - self.w)

pogled = Pogled()



class prvaPuska:
    x=0
    y=0
    
    desno=False
    
    firerate = 0.6
    speed=16
    dmg=1
    
    explosive=False
    spr=363
    
class drugaPuska:
    x=0
    y=0
    
    desno=False
    
    firerate = 0.1
    speed=6
    dmg=1
    
    explosive=False
    spr=362
    
class trecaPuska:
    x=0
    y=0
    
    desno=False
    
    firerate = 0.2
    speed=9
    dmg=2
    
    explosive=True
    explLenght = 1
    explSize = 16
    spr=378


metci = []




class Metak:
    x=0
    y=0
    
    width=4
    height=4
    
    desno=False
    
    speed=9
    dmg=2
    
    explosive=False
    explVar = 0
    explSizeVar = 2
    
    spr=378
    coll = []
    
    
    
    def MetakCheck(metak, colls, enemies):
            metak.coll=colls
            metak = metak
            metakIsHere = True
            i = 0
            for enemys in enemies:
              for enemy in enemys:
                if metakIsHere and metak.x < enemy.x + enemy.width and metak.y < enemy.y + enemy.height and metak.x > enemy.x - enemy.width + 8 and metak.y > enemy.y - enemy.height:
                    if metak in metci:
                        enemy.Pogoden(metak.dmg, i)
                        metci.remove(metak)
                        del metak
                        metakIsHere = False
                    else:
                        del metak 
                        metakIsHere = False
            if metakIsHere: 
               if metak.x < 0 or metak.x > pogled.ogranicenjeX or Metak.ProvjeriKolizije(metak, 0, 1):
                if metak in metci:
                    # za rakete i ekpslozije
                    if metak.explosive and metak.explVar < trecaPuska.explLenght * 60:
                        metak.speed = 0
                        metak.explVar += 1
                        metak.explSizeVar += int(metak.explVar / 5)
                        
                        minSize = min(metak.explSizeVar, trecaPuska.explSize)
                        
                        rect(int(metak.x) - int(pogled.x) - int(minSize / 2) + 2, int(metak.y) - int(pogled.y) - int(minSize / 2) + 2, minSize, minSize, 3)
                    else:
                        metci.remove(metak)
                        del metak
                else:
                    del metak
            
            
    
    def ProvjeriKolizije(self, xdodatak, ydodatak):
        self.x += xdodatak
        self.y += ydodatak
        for obj in self.coll:
            if obj.check_collision(self):
                self.x -= xdodatak
                self.y -= ydodatak
                return True
        self.x -= xdodatak
        self.y -= ydodatak
        return False



class Puska:
    x=0
    y=0

    id=0
    
    svespr = [360, 361, 376]
    
    svep = [prvaPuska, drugaPuska, trecaPuska]  # sve puske
    tp = 0   # trenutna puska
    p = [0, 0]  # puske koje imamo
    
    
    def pucaj(puska):
        metak = Metak()  
        metak.x = int(Puska.x)
        metak.y = int(Puska.y)
        metak.desno = player.desno
  
        metak.dmg = Puska.svep[Puska.p[Puska.tp]].dmg
        metak.speed = Puska.svep[Puska.p[Puska.tp]].speed
        metak.explosive = Puska.svep[Puska.p[Puska.tp]].explosive
        metak.spr = Puska.svep[Puska.p[Puska.tp]].spr

        if Puska.svep[Puska.p[Puska.tp]].spr == 363:
            sfx(12, "C-4", 5, 0, 2, -4)
        elif Puska.svep[Puska.p[Puska.tp]].spr == 362:
            sfx(13, "G-4", 5, 0, 2, 2)
        elif Puska.svep[Puska.p[Puska.tp]].spr == 378:
            sfx(14, "C-6", 5, 0, 2, 1)

        metci.append(metak)
        player.shootTimer=Puska.svep[Puska.p[Puska.tp]].firerate * 60
    
    
    def PromijeniPusku():
        if Puska.p[0] == Puska.p[Puska.tp]:
            Puska.tp = 1
        else:
            Puska.tp = 0
    
    
    def Pucanje():
      if player.shootTimer < 0:
        if key_shoot:
            Puska.pucaj(prvaPuska)
      
      eksdes = 12
      ekslijevo = -4
      eksGori = 6
      fliph = 0
      
      # gdje i kako ce se puska renderati
      if player.desno:
        Puska.x = int(player.x) + eksdes
        Puska.y = int(player.y) + eksGori
      else:
        Puska.x = int(player.x) + ekslijevo
        Puska.y = int(player.y) + eksGori
        fliph = 1
    
    
      spr(int(Puska.svespr[Puska.p[Puska.tp]]), Puska.x - int(pogled.x), Puska.y - int(pogled.y), 0,1,fliph,0,1,1)
    
      player.shootTimer = player.shootTimer - 1
        
      for metak in metci:
          
            if metak.explosive:
                spr(metak.spr + (int(metak.x) % 2),metak.x - int(pogled.x),metak.y - int(pogled.y),0,1,0,0,1,1)
            else:
                spr(metak.spr,metak.x - int(pogled.x),metak.y - int(pogled.y),0,1,0,0,1,1)
            
            if metak.desno == True:   
                metak.x = metak.x + metak.speed
            else:
                metak.x = metak.x - metak.speed

flag_za_crvena_vrata = False
flag_za_zelena_vrata = False
flag_za_final_vrata = False

class Kartica:
    def __init__(self, x, y, tip='red'):
        tile_size = 8
        self.x = x * tile_size
        self.y = y * tile_size
        self.pokupio = False

        self.tip = tip
        if self.tip == 'red':
            self.sprite = 420  # sprite za crvenu karticu
        elif self.tip == 'green':
            self.sprite = 436  # sprite za zelenu karticu
        elif self.tip == 'final':
            self.sprite = 421  # sprite za final karticu
        elif self.tip == 'sister':
            self.sprite = 386  # sprite za sister
        else:
            raise ValueError(f"Nepoznat tip kartice: {tip}")

    def prikazi(self):
        if not self.pokupio:
            if self.tip == 'sister':
                spr(self.sprite,
                    int(self.x) - int(pogled.x),
                    int(self.y) - int(pogled.y),
                    15, 1, 0, 0, 2, 2)
            else:
                spr(self.sprite,
                    int(self.x) - int(pogled.x),
                    int(self.y) - int(pogled.y),
                    0, 1, 0, 0, 1, 1)

    def provjeri_pickup(self):
        # Provjera kolizije s igračem
        if (not self.pokupio and self.x < player.x + player.width and self.y < player.y + player.height and self.x > player.x - player.width + 8 and self.y > player.y - player.height):
            sfx(14, "D-3", 3, 0, 2, 2)
            self.pokupio = True

            global flag_za_crvena_vrata, flag_za_zelena_vrata, flag_za_final_vrata
            if self.tip == 'red':
                flag_za_crvena_vrata = True
            elif self.tip == 'green':
                flag_za_zelena_vrata = True
            elif self.tip == 'final':
                flag_za_final_vrata = True
            elif self.tip == 'sister':
                global state
                state = 'win'

    # alias za dosadašnju kompatibilnost
    def PickUp(self):
        self.prikazi()
        self.provjeri_pickup()  


class Platforma(collidable):
    def __init__(self, x, y, width):
        tile_size = 8
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = width * tile_size
        self.height = tile_size
        self.fall_timer = 0
        self.falling = False
        self.dead = False
        self.vsp = 0
        self.gravity = 0.3

    def update(self):
        if self.dead:
            return
        screen_y = self.y - level * LEVEL_HEIGHT * 8
        if (not self.falling and player.vsp > 0 and player.x + player.width > self.x and player.x < self.x + self.width and player.y + player.height <= screen_y and abs((player.y + player.height) - screen_y) < 4):
            player.y = screen_y - player.height
            player.vsp = 0
            player.on_ground = True

 
        if (player.x + player.width > self.x and player.x < self.x + self.width and abs((player.y + player.height) - screen_y) < 4 and not self.falling):
            self.fall_timer += 1
            if self.fall_timer > 7:
                self.falling = True
        else:
            self.fall_timer = 0


        if self.falling:
            self.vsp += self.gravity
            self.y += self.vsp


        if not self.falling and not self.dead:
            if ( player.x < self.x + self.width and player.x + player.width > self.x and player.y < screen_y + self.height and player.y + player.height > screen_y ):
                # compute penetration depths
                dx1 = (self.x + self.width) - player.x
                dx2 = (player.x + player.width) - self.x
                dy1 = (screen_y + self.height) - player.y
                dy2 = (player.y + player.height) - screen_y

                # find smallest overlap
                overlap_x = dx1 if dx1 < dx2 else -dx2
                overlap_y = dy1 if dy1 < dy2 else -dy2

                # resolve along the axis of least penetration
                if abs(overlap_x) < abs(overlap_y):
                    # push player horizontally
                    player.x += overlap_x
                    player.hsp = 0
                else:
                    # push player vertically
                    player.y += overlap_y
                    player.vsp = 0
                    # if we pushed them up onto the platform, set grounded
                    if overlap_y < 0:
                        player.on_ground = True

    def draw(self):
        if not self.dead:
            for i in range(0, self.width, 8):  # Iteriranje kroz širinu platforme
                pixel_x = int(self.x + i) - int(pogled.x)
                pixel_y = int(self.y) - level * LEVEL_HEIGHT * 8 - int(pogled.y)
                spr(1, pixel_x, pixel_y, 0, 1, 0, 0, 1, 1)

            
class PromjenaPuska:
    puskaBr = 0
    puskaSpr = 376
    x = -1
    y = -1
    
    pickUpBool = True
    
    def __init__(self, x, y, puskaBr = 0): # uzima x, y i broj puske (opcionalno)
        tile_size = 8
        self.x = x*tile_size
        self.y = y*tile_size
        self.puskaBr = puskaBr
        self.puskaSpr = Puska.svespr[puskaBr]
    
    def PickUp(self):
        spr(self.puskaSpr, int(self.x) - int(pogled.x), int(self.y) - int(pogled.y), 0,1,0,0,1,1)
        
        if self.pickUpBool and self.x < player.x + player.width and self.y < player.y + player.height and self.x > player.x - player.width + 8 and self.y > player.y - player.height:
            #zamijeni puske
            sfx(15, "C-2", 3, 0, 2, 3)
            self.puskaSpr = Puska.svespr[Puska.p[Puska.tp]]
            noviBr = self.puskaBr
            self.puskaBr = Puska.p[Puska.tp] 
            Puska.p[Puska.tp] = noviBr
            self.pickUpBool = False
        elif not (self.x < player.x + player.width and self.y < player.y + player.height and self.x > player.x - player.width + 8 and self.y > player.y - player.height):
            self.pickUpBool = True

def test( a, b ):
    return a+b

player_starting_positions = [ # pocetna pozicija igraca za svaki level (u map editoru se prikazuje):
    [2, 12], # level 0
    [3, 24], # level 1
    [5, 46], # level 2
    [3, 63], # level 3
]
level_finish_tile_indexes = [ # indexi tileova
    
]

locked_door_tile_indexes = [ # indexi tileova crvenih, zelenih i final level vrata
    67,68,69,83,84,85,99,100,101,
    70,71,72,86,87,88,102,103,104,
    176,177,178,192,193,194,208,209,210
]

red_door_tile_indexes = [ # indexi tileova crvenih vrata
    67,68,69,83,84,85,99,100,101
]

green_door_tile_indexes = [ # indexi tileova zelenih vrata
    70,71,72,86,87,88,102,103,104
]

final_level_door_tile_indexes = [ # indexi tileova final level vrata
    176,177,178,192,193,194,208,209,210
]

background_tile_indexes = [ # indexi tileova sa elementima koji nemaju definiraju koliziju (pozadinski elementi)
	4,5,6,7,8,9,
    16,20,21,22,24,25,26,27,32, 33, 34, 35,
    37,38,39,40,55,56,
    64,65,66,80,81,82,
    44,60, #zvijezde
    13,14,29,30,45,46,61,62, # ljestve
    76,77,92,93,108,109,124,125,140,141,156,157,172,173,#"hotel"
    2,3,#18,19,#box
    116,132,123,107,#spikes
    150,151,166,167,#ormari
    48,50,51, 52, 36, 41,
    70, 71, 72, 86, 87, 88, 102, 103, 104,  # zelena vrata
    67,68,69,83,84,85,99,100,101, # crvena vrata
    176, 177, 178, 192, 193, 194, 208, 209, 210, # final level vrata
	56, 57, 58,
    59, 231, 247,
    219, 220, 221, 222, 223, # oni "ormarici"
    235, 236, 237, 238, 239,
    251, 252, 253, 254, 255,
    185,186,187,188,201,202,203,204,217,218,219,220, #doctor
    137, 138, 139, 153, 154, 155, 169, 170, 171, #incubators
    179, 180, 181, 195, 196, 197, 211, 212, 213, 189, 190, 191, 205, 206, 207, 221, 222, 223, 224, #acid
    182, 183, 184, 198, 199, 200, 214, 215, 216 #acid container
]
falling_platforms_by_level = [
    [],
    [Platforma(132, 27, 2),Platforma(136, 26, 1)],  # level 1
    [Platforma(188, 42, 3), Platforma(193, 43, 3)],  # level 2
    [Platforma(11, 62, 2)],  # level 3
]
enemies = [ # pocetne pozicije enemyja za svaki level (u editoru se ispisuje koja)
    [], # level 0
    [Enemy(21, 30, 17, 34),Enemy(43, 30, 30, 45), Enemy(175, 30, 171, 185)], # level 1
    [Enemy2(75, 46, 44, 79), Enemy2(58, 46, 47, 68), Enemy2(107, 45, 104, 119)], # level 2
    [Enemy3(28, 64, 20, 37), Enemy3(34, 64, 19, 38), Enemy3(180, 64, 168, 183), Enemy3(211, 64, 203, 215), FinalBoss(228, 60, 219, 232)] # level 3
]
pickups = [ # pocetna pozicija pick up pusaka za svaki level (u editoru se ispisuje koja)
    [Kartica(33,6,'red')], # level 0
    [PromjenaPuska(130, 22, 1), Kartica(231,25,'green')], # level 1
    [PromjenaPuska(168, 40, 2), Kartica(221,40,'final')], # level 2
    [Kartica(237, 64, 'sister')] # level 3
]
spikes = [ # tileovi spikeova
    116,132,123,107
]
acid = [ # tileovi kiseline
    179, 180, 181, 195, 196, 197, 211, 212, 213, 189, 190, 191, 205, 206, 207, 221, 222, 223, 224 
]

# sljedece varijable NE MIJENJATI:
LEVEL_HEIGHT = 17

def ZapocniLevel(level, dest_x=-1, dest_y=-1): # poziva se u menu.py kada se odabere opcija da se uđe u level
    global falling_platforms
    falling_platforms = falling_platforms_by_level[level]
    tile_size = 8
    starting_pos = player_starting_positions[level]
    if (dest_x == -1):
        player.x = starting_pos[0]*tile_size
        player.y = (starting_pos[1] - LEVEL_HEIGHT*level)*tile_size
    else:
        player.x = dest_x*tile_size
        player.y = (dest_y - LEVEL_HEIGHT*level)*tile_size
    
    pogled.x = max(0, player.x - (pogled.w - player.width)/2)
    player.hsp = 0
    player.vsp = 0
    if level == 0:
        music(0, 0, -1)
    elif level == 1:
        music(1, 0, -1)
    elif level == 2:
        music(2, 0, -1)
    elif level == 3:
        music(3, 0, -1)
    

def IgrajLevel():
    cls(0)
    map(0, level*LEVEL_HEIGHT, 240, 18, -int(pogled.x), -int(pogled.y), 0)
    HUD()
    tile_size = 8
    levelEnemies = enemies[level]
    for enemy in levelEnemies:
        while (enemy.y > LEVEL_HEIGHT*tile_size):
            enemy.y -= LEVEL_HEIGHT*tile_size
    collidables = DefinirajKolizije([player, levelEnemies, metci, projectiles, falling_platforms], level, LEVEL_HEIGHT)
    for plat in falling_platforms:
        if not plat.dead:
            collidables.append(plat)
    for enemy in levelEnemies:
        enemy.movement(collidables)
    for projektil in projectiles:
        projektil.movement()
        Projectile.MetakCheck(projektil, collidables)
    Puska.Pucanje()
    global hacked_enemy
    if hacked_enemy:
        HackedEnemyController(hacked_enemy, collidables)
        RenderInactivePlayer()
        if hacked_enemy:
            hacked_enemy.render()
            pogled.prati(hacked_enemy)
        else:
            pogled.pratiIgraca()
    else:
        player.PlayerKontroler(player, collidables)
        pogled.pratiIgraca()
    for metak in metci:
        Metak.MetakCheck(metak, collidables, enemies)
    for metak in projectiles:
        Projectile.MetakCheck(metak, collidables)
    levelPickups = pickups[level]
    for pickup in levelPickups:
        while (pickup.y > LEVEL_HEIGHT*tile_size):
            pickup.y -= LEVEL_HEIGHT*tile_size
        pickup.PickUp()
    ProvjeravajJeLiIgracKodVrata()
    ProvjeravajJeLiIgracNaSiljku()
    ProvjeravajJeLiIgracUKiselini()
    for platform in falling_platforms:
        platform.update()
        platform.draw()

teleport_destinations = {
    (0, 99): (1, 4, 24),  # crvena vrata na levelu 0 -> (level, tile ID): (destination_level, x, y)
    (0, 100): (1, 4, 24),  # crvena vrata na levelu 0
    (0, 101): (1, 4, 24),  # crvena vrata na levelu 0

    (1, 99): (0, 79, 13),  # crvena vrata na levelu 1
    (1, 100): (0, 79, 13),  # crvena vrata na levelu 1
    (1, 101): (0, 79, 13),  # crvena vrata na levelu 1

    (1, 102): (2, 5, 46),  # zelena vrata na levelu 1
    (1, 103): (2, 5, 46),  # zelena vrata na levelu 1
    (1, 104): (2, 5, 46),  # zelena vrata na levelu 1

    (2, 102): (1, 161, 30),   # zelena vrata na levelu 2
    (2, 103): (1, 161, 30),   # zelena vrata na levelu 2
    (2, 104): (1, 161, 30),   # zelena vrata na levelu 2

    (2, 208): (3, 4, 64),   # final vrata na levelu 2
    (2, 209): (3, 4, 64),   # final vrata na levelu 2
    (2, 210): (3, 4, 64),   # final vrata na levelu 2

    (3, 208): (2, 85, 41),   # final vrata na levelu 3
    (3, 209): (2, 85, 41),   # final vrata na levelu 3
    (3, 210): (2, 85, 41)   # final vrata na levelu 3
}

def ProvjeravajJeLiIgracKodVrata():
    global level, flag_za_crvena_vrata, flag_za_zelena_vrata
    tile_size = 8
    # center‑foot tile
    center_tx = int((player.x + player.width / 2) / tile_size)
    ty = int((player.y + player.height - 1 ) / tile_size)
    map_y = ty + level * LEVEL_HEIGHT

    # left and right tiles
    left_tx  = center_tx - 2
    right_tx = center_tx + 1

    for tx in (left_tx, right_tx):
        tile = mget(tx, map_y)

    # locked door
    if tile in locked_door_tile_indexes:
        required_key = 'blue'
        if tile in red_door_tile_indexes:
            required_key = 'red' 
        elif tile in green_door_tile_indexes:
            required_key = 'green'
        elif tile in final_level_door_tile_indexes:
            required_key = 'final'
        
        has_key = False
        if required_key == 'red' and flag_za_crvena_vrata:
            has_key = True
        elif required_key == 'green' and flag_za_zelena_vrata:
            has_key = True
        elif required_key == 'final' and flag_za_final_vrata:
            has_key = True
        if has_key:
            door_key = (level, tile)
            if door_key in teleport_destinations:
                sfx(16, "C-4", 15, 0, 2, 1)
                
                # dohvati odredište
                dest_level, dest_x, dest_y = teleport_destinations[door_key]

                if dest_level < level:
                    VratiSeNaPrethodniLevel(dest_x, dest_y)
                elif dest_level > level:
                    ZavrsiLevel(dest_x, dest_y)
            else:
                # ako nema definirane destinacije, završi level
                ZavrsiLevel()
        else:
            if required_key == 'red':
                print("You need a red card for this door", 5, 20, 12)
            elif required_key == 'green':
                print("You need a green card for this door", 5, 22, 12)
            elif required_key == 'final':
                print("You need a yellow key for this door", 5, 22, 12)
            return
            
        # finish door?
        if tile in level_finish_tile_indexes:
            sfx(16, "C-4", 15, 0, 2, 1)
            ZavrsiLevel()
            return
    
def ProvjeravajJeLiIgracNaSiljku():
    tile_size = 8
    kojiTile = mget(round(player.x/tile_size), round(player.y/tile_size) + 1 + level*LEVEL_HEIGHT)
    if kojiTile in spikes:
        sfx(8, "C-4", 15, 0, 2, 1)
        player.Pogoden(player, 1)

def ProvjeravajJeLiIgracUKiselini():
    tile_size = 8
    kojiTile = mget(round(player.x/tile_size), round(player.y/tile_size) + level*LEVEL_HEIGHT)
    if kojiTile in acid:
        sfx(8, "C-4", 15, 0, 2, 1)
        player.Pogoden(player, 1)

def ZavrsiLevel(dest_x=-1, dest_y=-1):
    global level
    level = level + 1
    if level <=3:
        ZapocniLevel(level, dest_x, dest_y)
    else:
        global state
        state = 'win'

def VratiSeNaPrethodniLevel(dest_x=-1, dest_y=-1):
    global level
    if level > 0:
        level -= 1
        ZapocniLevel(level, dest_x, dest_y)
    else:
        print("You're on the first level", 10, 10, 12)

def HUD():
    rect(0, 0, 240, 8, 0)
    print("Level:" + str(level), 1, 1, 12, True, 1, False)
    # Prikaz zivota
    spr(364, 50, 0, 0, 1, 0, 0, 1, 1)
    rect(60, 1, player.health*10, 5, 6)
    if player.health > 0:
        rect(60+player.health*10, 1, 50-player.health*10, 5, 3)
        print(str(player.health) + "HP", 175, 1, 12, True, 1, False)
    else: 
        print("0HP", 120, 1, 12, True, 1, False)
    # Prikaz puske i metaka
    spr(Puska.svespr[Puska.p[Puska.tp]], 213, 0, 6, 1, 0, 0, 1, 1)

# <TILES>
# 000:7777777777777777777777777777777777777777777777777777777777777777
# 001:00000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 002:7777777777777777777777777777777777777777777777777000000070440999
# 003:7777777777777777777777777777777777777777777777770000007799999077
# 004:70eeeeee70eeeee070dddd0870eeee0870dddd0870dddd0870dddd0870dddd08
# 005:88dddddd8deeeeeedee00000ece0ddddeee0deeeece0d000ece0ddddece0deee
# 006:ddddddddeeeeeeee00000000ddddddddeeeeeeee00000000ddddddddeeeeeeee
# 007:ddddddddeeeeeeee00000000ddddddddeeeeeeee00000000ddddddddeeeeeeee
# 008:dddddd88eeeeeed800000eeddddd0eceeeed0eee000d0ecedddd0eceeeed0ece
# 009:eeeeee070eeeee0780dddd0780eeee0780dddd0780dddd0780dddd0780dddd07
# 010:000000000ddddddd0eeeeeee0eeeeeee0eeeeeee0eeeeeee0eeeeeee0ececccc
# 011:00000000ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeecccccccc
# 012:00000000ddddddd0eeeeeee0eeeeeee0eeeeeee0eeeeeee0eeeeeee0ccccece0
# 013:dddddddddd000000dddddddddd000000dddddddedd000000dddddeeedd000000
# 014:dddeeeee000000eedeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 015:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 016:8888888888888888888888888888888888888888888888888888888888888888
# 017:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 018:7044099370440933704403337044033370440333704403337044033370000000
# 019:3999307733993077333330773333307733333077338a30773333307700000077
# 020:70dddd0870dddd0870dddd0870dddd0870dddd0870dddd0870dddd0870dddd08
# 021:ece0d000ece0ddddece0deeeece0d000ece0ddddece0deeeeee0d000ece0eddd
# 022:00000000ddddddddeeeeeeee00000000ddddddddeeeeeeee00000000dddddddd
# 023:00000000ddddddddeeeeeeee00000000ddddddddeeeeeeee00000000dddddddd
# 024:000d0ecedddd0eceeeed0ece000d0ecedddd0eceeeed0ece000d0eeeddde0ece
# 025:80dddd0780dddd0780dddd0780dddd0780dddd0780dddd0780dddd0780dddd07
# 026:000000000deddddd0eeeeeee0d0660000d0600600eeeeeee0deddddd00000000
# 027:00000000ddddded0eeeeeee0600060d0006060d0eeeeeee0ddddded000000000
# 028:4444444444444444444444444444444444444444444444444444444444444444
# 029:dddeeeeedd000000ddeeeeeede000000deeeeeeede000000deeeeeeede000000
# 030:eeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 031:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 032:80dddd0780dddd0780dddd0780dddd0780dddd0780eddd0780eede0780eeee07
# 033:70dddd0870dddd0870dddd0870dddd0870dddd0870ddde0870edee0870eeee08
# 034:88dddddd8deeeeeedeeeeeeeece77777eee77777ece77777ece77777ece77777
# 035:dddddd88eeeeeed8eeeeeeed77777ece77777eee77777ece77777ece77777ece
# 036:70dddd0870dddd0870dddd0870dddd0870dddd0870dddd0870dddd0870dddd08
# 037:ece0eeddece07777ece07777ece07777ece07777ece07777eee07777ece07777
# 038:dddddddd77777777777777777777777777777777777777777777777777777777
# 039:d000000070440999704403337044033370440333704403337044033370440333
# 040:0dee0ece90000ece99900ece39300ece33300ece33300ece8a300eee33300ece
# 041:80dddd0780dddd0780dddd0780dddd0780dddd0780dddd0780dddd0780dddd07
# 042:7777770077770022777022227702222077022207702222070222207702222077
# 043:0000777720077777077777777777777777777777777777777777777777777777
# 044:7777777777707777770d077770ccc077770c0777777077777777777777777777
# 045:eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000
# 046:eeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 047:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# 048:0000000088888888888888888888888888888888888888888888888888888888
# 049:dddddddfdeeeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdfffffff
# 050:ece77777ece77777ece77777ece77777ece77777ece77777eee77777ece77777
# 051:77777ece77777ece77777ece77777ece77777ece77777ece77777eee77777ece
# 052:70eded0870eddd0870eede000dddddd00dddddd00eddede00eeedde000000000
# 053:0000000000000000800000008000000080000000800000008000000000000000
# 054:1111111111111111111111111111111111111111111111111111111111111111
# 055:dddddddd77777777777777777777777777777777777777777777777777777777
# 056:ddee0ece77770ece77770ece77770ece77770ece77770ece77770eee77770ece
# 057:80dede0780ddde0700edee070dddddd00dddddd00ededde00eddeee000000000
# 058:0222207702222207022222070222222070222222770222227700022277770000
# 059:7777777077777700777770207770020700022207222220772222077700007777
# 060:777777777777777777777777777c777777777777777777777777777777777777
# 061:eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000
# 062:eeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 064:8ddddddddeeeeeeeece77777eeeeeeeeece77777eceeeeeeeceeeeeeece77777
# 065:ddddddddeeeeeeee77777777eeeeeeee77777777eeeeeeeeeeeeeeee77777777
# 066:ddddddd8eeeeeeed77777eceeeeeeeee77777eceeeeeeeceeeeeeece77777ece
# 067:eeeeeeeee6666666e6000000e6000000e6002222e6002222e6002222e6002222
# 068:eeeddeee666dd666000dd000000dd000200dd002200dd002200dd002200dd002
# 069:eeeeeeee6666666e0000006e0000006e2222006e2222006e2222006e2222006e
# 070:eeeeeeeeefffffffef000000ef000000ef002222ef002222ef002222ef002222
# 071:eeeddeeefffddfff000dd000000dd000200dd002200dd002200dd002200dd002
# 072:eeeeeeeefffffffe000000fe000000fe222200fe222200fe222200fe222200fe
# 073:777ddddd77deeeee7deeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 074:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 075:ddddf777eeeeef77eeeeeef7eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 076:2222222225555555255555552555c5552555c5552555c5552555cccc2555c555
# 077:22222222555555525555555255c5555255c5555255c55552ccc5555255c55552
# 078:777777777777777b7777777777777777777777777777777b777777bbb777bbbb
# 079:77777bbb777bbbc7bbbbc877bbbc8777bbc87777bc877777bc877777c8777777
# 080:eceeeee7ece7777eece77777eceeeeeeeee77777ece77777eeeddddd8eeeeeee
# 081:77777777eeeeeeee77777777e77777777eeeeeee77777777ddddddddeeeeeeee
# 082:7eeeeecee7777ece77777eceeeeeeece77777eee77777ecedddddeeeeeeeeee8
# 083:e6000000e6000000e6000000e6000000e6000000e6000000e6000000e6000000
# 084:000dd000000dd000000dd0000eeddee00eeddee0000dd000000dd000000dd000
# 085:0000006e0000006e0000006e0000006e0000006e0000006e0000006e0000006e
# 086:ef000000ef000000ef000000ef000000ef000000ef000000ef000000ef000000
# 087:000dd000000dd000000dd0000eeddee00eeddee0000dd000000dd000000dd000
# 088:000000fe000000fe000000fe000000fe000000fe000000fe000000fe000000fe
# 089:deeeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee7deeeeee77deeeee777fffff
# 090:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 091:eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeef7eeeeef77fffff777
# 092:2555c5552555c55525555555255555552555cccc2555c5552555c5552555c555
# 093:55c5555255c555525555555255555552ccc5555255c5555255c5555255c55552
# 094:7bbbbbbb77bbbbbc777bbbbc777bbbbc7777bbc877777bc877777bc877777bc8
# 095:c877777787777777877777778777777777777777777777777777777777777777
# 099:e6000000e6000000e6000000e6000000e6000000e6000000e6666666eeeeeeee
# 100:000dd000000dd000000dd000000dd000000dd000000dd000666dd666eeeddeee
# 101:0000006e0000006e0000006e0000006e0000006e0000006e6666666eeeeeeeee
# 102:ef000000ef000000ef000000ef000000ef000000ef000000efffffffeeeeeeee
# 103:000dd000000dd000000dd000000dd000000dd000000dd000fffddfffeeeddeee
# 104:000000fe000000fe000000fe000000fe000000fe000000fefffffffeeeeeeeee
# 105:000000000ddddddd0ddddddd0eeeeeee0eeeeeee000000000dddd6660ddd6666
# 106:00000000ddddddd0ddddddd0eeeeeee0eeeeeee0000000006666ddd0666dddd0
# 107:5555555551111115511111155111111551111115511111155111111551111115
# 108:2555c5552555c5552555cccc25555555255555552555cccc2555555c2555555c
# 109:55c5555255c55552ccc555525555555255555552ccc555525555555255555552
# 110:77777bc87777bbc8777bbbc8777bbbc87bbbbbc8777bbbc87777bbc877777bbc
# 111:7777777777777777777777777777777777777777777777777777777787777777
# 112:22222222211111112111111121ccccc121c1111121c1111121c1111121ccccc1
# 113:2222222211111111111111111cccccc11c1111c11c1111c11c1111c11c1111c1
# 114:2222222211111111111111111cccccc11c1111c11c1111c11c1111c11c1111c1
# 115:2222222211111112111111121ccc11121c1cc1121c11cc121c111c121c111c12
# 116:77755777777557777751c5777751c57775111c5775111c5755111c55511111c5
# 117:000000000ddddddd0eeeeeee0eeeeeee0eedeeee0eeeeeee0eeeeeee0eeeeeee
# 118:00000000ddddddd0eeeeeee0eeeeeee0eeeedee0eeeeeee0eeeeeee0eeeeeee0
# 119:000000000ddddddd0deddddd0ddddeee0dddddee0ddeddde0ddeeddd0ddeeedd
# 120:00000000ddddddd0ddddded0eeedddd0eeddddd0edddedd0dddeedd0ddeeedd0
# 121:0dd666660d666666066666660666666d066666dd06666ddd0666dddd00000000
# 122:66ddddd06dddddd0dddddd60ddddd660dddd6660ddd66660dd66666000000000
# 123:511111c555111c5575111c5775111c577751c5777751c5777775577777755777
# 124:2555555c2555555c2555555c2555555c25555555255555552555cccc2555c555
# 125:555555525555555255555552555555525555555255555552ccc5555255555552
# 126:77777bbc77777bbc777777bb7777777b7777777b7777777b777777bb77777b77
# 127:8777777787777777c8777777c8777777bc877777bc8777777bc8777777bc8777
# 128:21c1111121c1111121c1111121c1111121c11111211111112111111122222222
# 129:1c1111c11c1111c11c1111c11c1111c11cccccc1111111111111111122222222
# 130:1c1111c11c1111c11c1111c11c1111c11cccccc1111111111111111122222222
# 131:1c111c121c111c121c11cc121c1cc1121ccc1112111111121111111222222222
# 132:5111111551111115511111155111111551111115511111155111111555555555
# 133:0eeeeeee0eeeeeee0eeeeeee0eeeeeee0eedeeee0eeeeeee0eeeeeee00000000
# 134:eeeeeee0eeeeeee0eeeeeee0eeeeeee0eeeedee0eeeeeee0eeeeeee000000000
# 135:0ddeeedd0ddeeddd0ddeddde0dddddee0ddddeee0deddddd0ddddddd00000000
# 136:ddeeedd0dddeedd0edddedd0eeddddd0eeedddd0ddddded0ddddddd000000000
# 137:7777777777777777777777777777777777777778777777887777777877777778
# 138:77777777777777777888888888888888888888888888888877777777aa777777
# 139:7777777777777777777777778777777788777777888777777877777778777777
# 140:2555c5552555cccc2555c5552555c5552555cccc25555555255555552555c555
# 141:55555552ccc555525555555255555552ccc55552555555525555555255555552
# 144:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee777777757777777e7777777e
# 145:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee55555555eeeeeeeeeeeeeeee
# 146:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee57777777e7777777e7777777
# 147:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee7777777f7777777e7777777e
# 148:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffffeeeeeeeeeeeeeeee
# 149:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef7777777e7777777e7777777
# 150:000000000eeeeee00dddddd00d7777d00dddddd00d7777d00dddddd00dddddd0
# 151:00000000eeeeee70dddddd70d7777d70dddddd70d7777d70dddddd70dddddd70
# 153:7777777877777778777777787777777877777778777777787777777877777778
# 154:7aa7777777aa7777777aa777777a777777a777777a77777777a77777777777a7
# 155:7877777778777777787777777877777778777777787777777877777778777777
# 156:2555c5552555c5552555c5552555c5552555c5552555cccc2555555525555555
# 157:5555555255555552555555525555555255555552ccc555525555555255555552
# 160:7777777e7777777e7777777e7777777e7777777e7777777e7777777e7777777e
# 161:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 162:e7777777e7777777e7777777e7777777e7777777e7777777e7777777e7777777
# 163:7777777e7777777e7777777e7777777e7777777e7777777e7777777e7777777e
# 164:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 165:e7777777e7777777e7777777e7777777e7777777e7777777e7777777e7777777
# 166:0dedddd00dedddd00dddddd00d7dddd00dddddd00dddddd00dddddd00dddddd0
# 167:dedddd70dedddd70dddddd70d7dddd70dddddd70dddddd70dddddd70dddddd70
# 169:777777787777777877777778777777787777777877777788777778887777888a
# 170:77777a77777777a77777777a777777778888888888888888aaaaaaaa77777777
# 171:787777777877777778777777787777778877777788877777a88877777a888777
# 172:2222222277777777777777777777777777777777777777777777777777777777
# 173:2222222277777777777777777777777777777777777777777777777777777777
# 176:888ddddd8deeeeeedeeeeeeeeceeeeeeeeeeeeeeece00000ece00000ece00000
# 177:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000ee000000ee000000ee000
# 178:dddddd88eeeeeed8eeeeeeedeeeeeeceeeeeeeee00000ece00000ece00000ece
# 179:ffffffffffffffffffffffffffffffffffffffffffffffffddddffffdddddddd
# 180:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffddddddff
# 181:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 182:777ddddd777ddddd777ddddd777ddddd77777ddd77777aaa77777aaa77777aaa
# 183:ddddddeedddddeeedddd0000dddeeeeedddeeeeeaaaaaa88aaaaaa88aaaaaa88
# 184:eeed7777eeed7777000d7777eeed7777eee7777788a7777788a7777788a77777
# 185:7777777e777eeeee777777ee777eeeee77777999777779997777779977777799
# 186:77e777eeeeeeeee7eddeeee7dddddeee999999976dd6d997dd9dd97799999977
# 187:ee777e777eeeeeee7eeeeddeeeeddddd79999999799d6dd6779dd9dd77999999
# 188:e7777777eeeee777ee777777eeeee77799977777999777779977777799777777
# 189:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdddddd
# 190:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 191:ffffffffffffffffffffffffffffffffffffffffffffffffddddffffdddddddd
# 192:ece00000ece00000ece00000ece00000ece00000ece00000ece00000ece00000
# 193:000ee000000ee000000ee000000ee000000ee00000dddd0000dddd00000ee000
# 194:00000ece00000ece00000ece00000ece00000ece00000ece00000ece00000ece
# 195:ddddddddfffdddddffffffffffffffffffffffffffffffffffffffffffffffff
# 196:ddddddddddddddddfffffdddfffffdddffffffffffffffffffffffffffffffff
# 197:ddddddffddddddddddddddddddddddddffddddddffffffffffffffffffffffff
# 198:77777aaa77777aaa77777aaa77777aaa77777ccc77777fff77777fff77777fff
# 199:aaaaaa88aaaaaa88aaaaaa88aaaaaa88ccccccccffffffddffffffddffffffdd
# 200:88a7777788a7777788a7777788a77777ccc77777ddf77777ddf77777ddf77777
# 201:7777777977777777ede7777ceee7777ceff9cccceffeecccefffe7cceeeee7cc
# 202:9ccc977779977777cbbcc777cbbccc77cbbcccc7cbbccccccbbccccccbbccccc
# 203:7779ccc977777997777cc11c77ccc11c7cccc11cccccc11cccccc11cccccc11c
# 204:9777777777777777c7777edec7777eeecccc9ffeccceeffecc7efffecc7eeeee
# 205:dddddddddddddddddddfffffdddfffffffffffffffffffffffffffffffffffff
# 206:ffddddddddddddddddddddddddddddddddddddffffffffffffffffffffffffff
# 207:ddddddddfffdddddffffffffffffffffffffffffffffffffffffffffffffffff
# 208:ece00000ece00000ece00000ece00000ece00000ece00000ece00000ece00000
# 209:000ee000000ee000000ee000000ee000000ee000000ee000000ee000000ee000
# 210:00000ece00000ece00000ece00000ece00000ece00000ece00000ece00000ece
# 211:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 212:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 213:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 214:77777fff77777fff77777fff77777fff77777ddd777ddddd777ddddd777ddddd
# 215:ffffffddffffffddffffffddffffffdddddddeeeddddeeeedddd0000ddddeeee
# 216:ddf00007ddfeee00ddfeeee0ddf000eeeed770eeeedd700e000d770eeeee770e
# 217:777777cc7777777c7777777c7777777c77777777777777777777777e777777ee
# 218:cbbccc99cbbccc77cbbccc77cbbccc77ee77ee77ee77ee77ee77eee7ee77eeee
# 219:99ccc11c77ccc11c77ccc11c77ccc11c77ee77ee77ee77ee7eee77eeeeee77ee
# 220:cc777777c7777777c7777777c77777777777777777777777e7777777ee777777
# 221:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 222:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 223:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 224:6666666666666666d6dd6666666dd6666666dd6d666666666666666666666666
# 225:000000000deddddd0eeeeeee0d0660000d0600600eeeeeee0deddddd00000000
# 226:00000000ddddded0eeeeeee0600060d0006060d0eeeeeee0ddddded000000000
# </TILES>

# <SPRITES>
# 000:fff0f0ffff030300ff033333f0333434f0344444f0444444ff044449ff049499
# 001:0f0fffff3030ffff33330fff434340ff444440ff44440fff99940fffcb90ffff
# 002:fff0f0ffff030300ff033333f0333434f0344444f0444444ff044449ff049499
# 003:0f0fffff3030ffff33330fff434340ff444440ff44440fff99940fffcb90ffff
# 004:fff0f0ffff030300ff033333f0333434f0344444f0444444ff044449ff049499
# 005:0f0fffff3030ffff33330fff434340ff444440ff44440fff99940fffcb90ffff
# 006:fff0f0ffff030300ff033333f0333434f0344444f0444444ff044449ff049499
# 007:0f0fffff3030ffff33330fff434340ff444440ff44440fff99940fffcb90ffff
# 008:fff0f0ffff030300ff033333f0333434f0344444f0444444ff044449ff049499
# 009:0f0fffff3030ffff33330fff434340ff444440ff44440fff99940fffcb90ffff
# 010:fff0f0ffff060600ff066666f0666666f0666666f0666666ff066666ff066666
# 011:0f0fffff6060ffff66660fff666660ff666660ff66660fff66660fff0060ffff
# 012:fff0f0ffff060600ff066666f0666666f0666666f0666666ff066666ff066666
# 013:0f0fffff6060ffff66660fff666660ff666660ff66660fff66660fff0060ffff
# 016:ff004999fff00999ff00e089ff0ee088ff0990aafff0077dff008800ff05500f
# 017:cb900fff99990fff999000ff888ee0ffaaa090ffdd770fff008800fff00550ff
# 018:ff000999fffee999ff0ee089ff0ee088f09900aaf000077dfff05500ffff00ff
# 019:cb900fff99990fff999090ff888ee0ffaaa000ffdd770fff00550fffff00ffff
# 020:ff000999fffee999ff0ee089ff0ee088f09900aaf000077dfff08800ff05500f
# 021:cb900fff99990fff999090ff888ee0ffaaa000ffdd770fff008800fff00550ff
# 022:ff000999ff0ee999f0eee089f0ee0088f0eee90aff0ee97dfff08880ffff0550
# 023:cb900fff99990fff9990ffff888effffaaa0ffffdd70ffff0880fffff0550fff
# 024:fff00999ff00ee99f0ee0ee9f0ee0ee8f0990eeaff00077dffff0880fff0550f
# 025:cb900fff99990fff999090ff888e90ffa8ae90ffdd770fff00880fffff0550ff
# 026:ff006666fff00666ff006666ff066066ff066060fff00666ff006600ff06600f
# 027:00600fff66660fff666000ff666660ff006060ff66660fff006600fff00660ff
# 028:ff000666fff66666ff066066ff066066f0660060f0000666fff06600ff06600f
# 029:00600fff66660fff666060ff666660ff006000ff66660fff006600fff00660ff
# 032:fff0f0ffff060600ff066666f0666666f0666666f0666666ff066666ff066666
# 033:0f0fffff6060ffff66660fff666660ff666660ff66660fff66660fff0060ffff
# 034:ffff0f0ffff03030ff034333ff034433f0044444099044440ee044440eee0444
# 035:f0f0ffff03030fff333430ff433440ff444440ff444440ff44440fff4440000f
# 036:ffff0f0ffff03030ff034333ff044334ff044444ff044444fff04444f0000444
# 037:f0f0ffff03030fff333430ff334430ff4444400f4444099044440ee04440eee0
# 038:ff0f0ff0f0303003f0333333033343440344444404444444f0444499f049499c
# 039:f0ffffff030fffff3330ffff34340fff44440fff4440ffff9940ffffb90fffff
# 040:ff0f0ff0f0303003f0333333033343440344444404444444f0444499f049499c
# 041:f0ffffff030fffff3330ffff34340fff44440fff4440ffff9940ffffb90fffff
# 042:ff0f0ff0f0303003f0333333033343440344444404444444f0444499f049499c
# 043:f0ffffff030fffff3330ffff34340fff44440fff4440ffff9940ffffb90fffff
# 044:ffffff00ffff000affff0aaaffff0a8affff0888ffff0888ffff08d8fffff0dd
# 045:000fffffaa00ffffaaa00fffaaaa0fffaaa80fff88880fffdbdd0fffdddd0fff
# 048:ff000666fff66666ff066066ff066066f0660060f0000666fff06600ffff00ff
# 049:00600fff66660fff666060ff666660ff006000ff66660fff00660fffff00ffff
# 050:f00ee000ff0ee0eeff000eeeffff0777fff00888fff08880ff05500fff0000ff
# 051:00000990eee0eee0ee0eee00777000ff88800fff00550ffff0000fffffffffff
# 052:099000000eee0eee00eee0eeff000777fff00888fff05500fff0000fffffffff
# 053:000ee00fee0ee0ffeee000ff7770ffff88800fff08880ffff00550ffff0000ff
# 054:f004999cff009999f00e0899f0ee0888f0990aaaff0077ddf0088000f05500ff
# 055:b900ffff9990f00f9900055088955900aa9500ffd7700fff08800fff00550fff
# 056:f004999cff009999f00e0899f0ee0888f0990aaaff0077ddf0088000f05500ff
# 057:b90000009990aaa099000a00889a0ba0aa9aba00d770000f08800fff00550fff
# 058:f004999cff009999f00e0899f0ee0888f0990aaaff0077ddf0088000f05500ff
# 059:b900ffff9990f00f9900088088988688aa986888d7708800088000ff00550fff
# 060:ffffff0dfffff0ddfffff0edffffff0dffffff00fffff077fffff077fffff0bb
# 061:ddcc0fffded00fffdee0ffffeee0ffffdee0ffff77770fff007700ffb07bb0ff
# 064:fffff00affff0aaaffff0a8affff0888ffff0888ffff08d8fffff0ddffffff0d
# 065:aa0fffffaaa0ffffaaaa0fffaaa80fff88880fffdbdd0fffdddd0fffddcc0fff
# 070:fff00000ff00ddddfb0ddd00fb0dd006ff0dd060fb0ed060ffa0ee06ff000eee
# 071:0fffffff00ffffffe00fffff6e0fffff2e0fffff4e0fffff600fffff00ffffff
# 072:fffbff00fffff0ddffbf0dddffbb0dd0fffb0dd0ffba0ed0fffaa0eeffff000e
# 073:000fffffddd0fbff000d0fff06600bff60260bff60460fff06600fffee00ffff
# 074:ffffff00fffff00dffff00ddffff0eddffff0eddffff0eedffff00eefffff000
# 075:000fffffddd0ffffdddd0fffd0660fffd0620fffd0660fffee000fffeee0ffff
# 080:fffff0ddfffff0edffffff0dfffffff0ffffff0dffffff07ffffff0bffffff0b
# 081:ded0ffffdee0ffffeee0ffffdee0ffffe770ffff7770ffff7bb0ffffb0bb0fff
# 086:f0dd0000f0d00ddd0ee00ee00e000000f00dd000ff0e0ff0f000fff0f000fff0
# 087:0e0fffff000ffffff0e0fffff000ffff0fffffffefffffffe0ffffff00ffffff
# 088:fff0dd00fff0d00dfff0e00efff0ee00ffff00d0fffff0e0ffff000fffff000f
# 089:00000fffddd00fffee00d0ff00f000ff000ffffff0effffff0e0fffff000ffff
# 090:ffff0de0ffff0d00ffff0ee0ffff0ee0fffff00effffff00fffff00ffffff000
# 091:000fffffee0fffffe000ffff0000ffff000ffffff00ffffff0e0fffff000ffff
# 104:0000000000500000555555550575000005500000050000000000000000000000
# 105:0000000000aaa000a00a0000baabaaaaaa0a0a000aa00a000a00000000000000
# 106:0000000000000000bbbbb0bb00bbbb000b0000bbbbbb0bb00000000000000000
# 107:0000000000000000002222200000000000222220000000000000000000000000
# 108:000000000cc00cc0c6cccc6cc66cc66cc666666ccc6666cc0cc66cc000cccc00
# 120:000000008855888e8888588e0868000008800000080000000000000000000000
# 122:0000000000000000007766000777666000776600000000000000000000000000
# 123:0000000000000000007667000776677000766700000000000000000000000000
# 128:ffffffffffffff00fffff044ffff0444fff04434fff04494ffff049affff049b
# 129:ffffffff00ffffff440fffff4340ffff33440fff44440fff99440fff94440fff
# 130:ffffff00fffff044ffff0444fff04434fff04494ffff049affff049bfffff088
# 131:00ffffff440fffff4340ffff33440fff44440fff99440fff94440fff4340ffff
# 132:ffffff00fffff00dffff00ddffff0eddffff0eddffff0eedffff00eeffff0d00
# 133:000fffffddd0ffffdddd0fffd0060fffd0060fffd0060fffee000fffeee0ffff
# 134:ffffff00fffff00dffff00ddffff0eddffff0eddffff0eedffff00eefffff000
# 135:000fffffddd0ffffdddd0fffd0000fffd0060fffd0060fffee000fffeee0ffff
# 136:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 137:fffffffffffffffffffffffffffffffffffffffffffffffffffffffff00fffff
# 138:ffffff00fffff00dffff00ddffff0eddffff0eddffff0eedffff00eefff0d000
# 139:000fffffdd00ffffddd00fffd0e60fffd0e60fffd0e60fffee000fffeee0ffff
# 140:fbf00000ff00ddddbf0dddd0bb0dd006fb0dd060fa0dd060ffa0ee06f0000eee
# 141:ffffffff0fffffffe0ffffff00ffffff60ffffff60ffffff00ffffff0fffffff
# 144:fffff088fffff7aafffff07affff07aaffff078afffff077fffff079ffffff09
# 145:4440ffff4740ffff87c40fffa8740fff8870ffff7740ffff7940ffff7790ffff
# 146:fffff7aafffff08affff07aaffff078afffff077fffff07affffff09ffffff09
# 147:3730ffff87c40fffa8740fff8870ffff7740ffff7a40ffff7940ffff0900ffff
# 148:fff0de00fff0d00efff0ee0effff0000fffff0e0ffff000ffff000fffff000ff
# 149:000fffffee0fffffe0000fff0f000fff00ffffff0e0fffff000fffff000fffff
# 150:ffff00d0ffff0d00fff00d0efff00ee0ffff0000ffff00fffff00ffffff000ff
# 151:000fffff00ffffffe000ffff0000ffff00ffffff0e0fffff000fffff000fffff
# 152:ffffff0ffff00f00fff0000ffff00000ff00000ef000ff0e000fff0000ffff00
# 153:f0f00fff0000ffffffffffffffffffff0fffffff0fffffffffffffff0fffffff
# 154:fff0e0d0fff000d0ff0e000dff000000ffff000efff000f0ff000ff0ff000ff0
# 155:000fffff0fffffffd0ffffff00ffffff0fffffff0fffffffe0ffffff00ffffff
# 156:0dde00000e00eee00ee0ee0ff0000000ff0d0000ff0e0f0ef000ff00f000ff00
# 157:0fffffff000fffff000fffffffffffffffffffff0fffffff0fffffff0fffffff
# 160:fffff00affff0aaaffff0a8affff0888ffff0888ffff08d8fffff0ddffffff0d
# 161:aa0fffffaaa0ffffaaaa0fffaaa80fff88880fffdbdd0fffdddd0fffddcc0fff
# 162:fffff00affff0aaaffff0a8affff0888ffff0888ffff08d8fffff0ddffffff0d
# 163:aa0fffffaaa0ffffaaaa0fffaaa80fff88880fffdbdd0fffdddd0fffddcc0fff
# 164:0000000000222200006666000022220000222200002222000000000000000000
# 165:0222220002000200020202000222220000020000000220000002000000000000
# 166:fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0
# 167:fffffffffffffffffffffffffffffffffffffffff00fffff0e0fffffe0fff000
# 168:fffffffffffffffffffffffffffffffffffffffffff00ffffff0e0ff00ff0e0f
# 169:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 170:fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0
# 171:fffffffffffffffffffffffffffffffffffffffff00fffff0e0fffffe0fff000
# 172:fffffffffffffffffffffffffffffffffffffffffff00ffffff0e0ff00ff0e0f
# 173:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 176:fffff0ddfffff0edffffff0dfffffff0fffff00dffff0b77ffff0b77fffff0b0
# 177:ded0ffffdee0ffffeee0ffffdee0ffffe770ffff7770ffff7bb0ffff00bb0fff
# 178:fffff0ddfffff0edffffff0dfffffff0fffff00dffff0b77ffff0b77fffff0b0
# 179:ded0ffffdee06060eeed060fdee0f0ffe770ffff7770ffff7bb0ffff00bb0fff
# 180:000000000022220000ffff000022220000222200002222000000000000000000
# 182:fffffff0fffffff0fffffff0fffff000ffff0eeefff07deefff07eeefff077ee
# 183:e0f007ee7e0077ee77e077ee0770777e00000777e0007670e000766670007066
# 184:ee0f0d0feee00e0feee0e70feee000ff777000ff77060000076607ee076007ee
# 185:ffffffffffffffffffffffffffffffffffffffffffffffff0fffffff0fffffff
# 186:fffffff0fffffff0fffffff0fffff000ffff07eefff07eeefff07eeeff0077ee
# 187:e0f007ee7e0077ee77e077ee0770777e00000777e0007670e000766670007066
# 188:ee0f0d0feee00e0feee0e70feee000ff777000ff77060000076607ee076007ee
# 189:ffffffffffffffffffffffffffffffffffffffffffffffff0fffffff0fffffff
# 192:fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0
# 193:fffffffffffffffffffffffffffffffffffffffff00fffff0e0fffffe0fff000
# 194:fffffffffffffffffffffffffffffffffffffffffff00ffffff0e0ff00ff0e0f
# 195:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 196:fffffffffff0fffffffffffffffff0fffff0f00fffffff00fff0f000fff0f00e
# 197:ffff0ffff0fff0ff00fff0ff000f00f0f00007000700000f0007000007000e00
# 198:ff000777ff000000ff077e00f0000007f07ee007f07eee00f07ee700f0777070
# 199:0007770000007606007076660077076600077000700000777077070000070777
# 200:0007077e660607700666000066600070000700007770000e0000007077000070
# 201:0fffffff0fffffffffffffffffffffff0fffffff000fffff0000ffff07e0ffff
# 202:ff000000ff070000f0770070f070ee0ef07077eef00007eeff077077fff00000
# 203:000777000000760607000666e0700760e07000000070007e0000000000000077
# 204:0007077e06060770666600000060000000000070eee007700000077077070070
# 205:0fffffff0fffffffffffffff0fffffff7000ffff70ee0fff000e0fff07e70fff
# 208:fffffff0fffffff0fffffff0fffff000ffff07eefff07eeefff07eeeff0077ee
# 209:e0f007ee7e0077ee77e077ee0770777e00000777e0006670e000766670007060
# 210:ee0f0d0feee00e0feee0e70feee000ff77700fff770600ff076600ff076000ff
# 211:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 212:ffff0070fffff000fffff000ff0fff00fffff000f0fff007ffff0077ff000000
# 213:700e000f0000070f700000ff0700ffff000fff0f7070ffff000fffff0000ff0f
# 214:f000ee70ff007700fff00000fffffff0ffffff00ffffff00ffffff07ffffff00
# 215:07ee000007ee70007777000070000fff7770ffff0000ffffee70ffff0000ffff
# 216:000e0000007de00000777e00f000770fff00000fff07700fff077ee0ff000000
# 217:7700ffff000fffff00ffffffffffffffffffffffffffffffffffffffffffffff
# 218:fffffff0ffffff00fffff007ffff0007ffff0077fff00070fff07770fff00000
# 219:070000007700000077000000ee0fffffe00fffff00ffffff0fffffffffffffff
# 220:000700000070fff0007e0ffff00770ffff0000ffff0700fff007700ff000000f
# 221:07700fff0000ffffffffffffffffffffffffffffffffffffffffffffffffffff
# 224:ff000777ff070000f077e070f077ee00f0077700f0077070ff077770fff00007
# 225:0007770000007600077006060077076600770000700770777000000000077770
# 226:00007000000000070660007066600077000000077700700000f0000f70ffffff
# 227:ffffffff70ffffff70ffffff70ffffff0fffffffffffffffffffffffffffffff
# 240:fffffff0ffffff00ffffff00fffff000ffff0000ffff000fffff0000ffffffff
# 241:000777770700077700070007000f0f000fffff07ffffff070fffff00ffffffff
# 242:000fffffee00ffff7e00ffff7700ffff700fffff7700ffff0000ffffffffffff
# 243:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# </SPRITES>

# <MAP>
# 000:0000000000000000000000c300000000c2000000000000000000000000000000c20000000000000000000000c30000000000000000c300000000000000c20000c30000000000c2000000c300a0b0b0b0b0b0b0b0b0b0b0b0b0c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 001:0000c200000000c200c300000000c30000000000c20000c30000c200c30000c30000c2000000c200000000000000000000c300000000000000c3c20000c30000000000c300000000c30000004001d0e001010101010101010190000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 002:00c30000c300000000000000c20000c30000c3000000000000c3000000c2000000c300c4d400000000c200c30000c2000000a2b2000000c20000000000000000c30000000000c3000000c3004101d1e1010101010101a1b10191000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 003:0000000000c20000c30000000000c30000c200000000a0b0b0b0b0b0b0b0b0b0b0b0c0c5d50000c300000000000000000000a3b3000000000000000000c3000000c2000000c20000000000004101d1e101010101010101010192000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 004:00c200c30000000717273700c300000000000000c30040030303030303030303030390c6d60000000000000000c30000c30000000000c30000c300000000c200000000c300000000c20000c34101d2e224010101010414240191000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 005:000000a0b0b0b008182838b0b0b0b0c00000c300000042010414240101010414240192c7d7000000c200c300c300000000000000000000000000000000000000c30000000000c300000000004101d3e325010101010515250191000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 006:0000004003030303030303030303039000000000c20042010515250101010515250192c8d800c3000000000000000000c20000c300c2000000c200000000c300000000c30000000000c300004201d2e201010101010101010192000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 007:000000420104142401a1b101010101920000000000001201010101d0e0010101010102c9d90000000000000000000000000000000000000000000000000000000000000000000000000000004301d3e301010101010101010193000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 008:00000042010515250101010122320192000000000000a0b0b0b0b0d1e1b0b0b0b0b0c0caca000000000000000000000000000000000000000000000000000000000000000000000000000000a0b0b0b0b0b0b0b0b0b0b0b0b0c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 009:000000120101010101010101233301020000000000004003030303d2e203030303039000000000000000000000000000000000000000000000000000000000000000000000000000000000004001010101010101010101010190000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 010:000000a0b0b0b0b0b0b0b0b0b0b0b0c00000000000004101010101d2e2607070800191000000000000000000000000000000000000000000000000000000000000000000000000000000000041010414240101010101a1b10191000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 011:000000400303030303030303030303900000000000004201223201d2e2616161810192000000000000000000000000000000000000000094a4a4a4a4a4a4b40000000000000000000000000041010515250101010101a1b10191000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 012:000000410101010101506070708001910000000000004301233301d3e3626273830193000000000000000000000000000000000000000095a5a5a5a5a5a5b50000000000000000000000000041010101010134445401a1b10191000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 013:0000004201223201015161616181019200001010101010101010101010101010101010101010100000000000000000000000000000000000000000000000000000000000000000000000000042010101010135455501a1b10192000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 014:000000430123330101526262728201930010111111111111111111111111111111111111111111100000000000000000000000004747474747474747474747474747000000000000000000004301010101013646560101010193000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 015:101010101010101010101010101010101011111111111111111111111111111111111111111111111010101010101010101010104848484848484848484848484848101010101010101010101010101010101010101010101010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 016:111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 017:000000000000000000000000576757675767778777875767000000000000000000000057677787778757675767576700000000000000000000005767576777875767576757670000000000000000000000000000131313131313131313131313131313131313131313131313131313131313131313131313000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000130013000000001313130000000000130013000000005868586858685868576758685857
# 018:000000000000000000000000586858685868788878885868000000000000000000000058687888788858685868586800000000000000000000005868586878885868586858680000000000000000000000000000000013131313131313131313131313131313131313131313131313131313131313131313000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000130013000000001313130000000000130013000000000000000000000000586800000058
# 019:0000000000000000000000005767576757675767576757670000000000000000000000b6b65767576757677787576700000000000000000000000000576757675767576700000000000000000000000000000000000000131313131313131313131313131313131313131313131313131313131313131313000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000130013000000131300130000000000130013130000000000000000000000000000000057
# 020:0000000000000000000000005868586858685868586858680000000000000000000000b7b75868586858687888586800000000000000000000000000586858685868586800000000000000000000000000000000000000001313131313000013131313131313131313131313131313131313131313131313000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001300130000000000130013000000000000000000000000000000000058
# 021:000000000000000000000000b6b6b6b6b6b6b6b6b6b6b6b600000000000000000000000000b6b6576757675767576700000000000000000000000000000000000000000000000000000000000000000000000000000000000013131300000000131300001313131313131313131313131313131313131313000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000077875767000000000057
# 022:000000000000000000000000b7b7b7b7b7b7b7b7b7b7b7b700000000000000000000000000b7b75868586858685868000000000000000000000000000000000000000000000000000000000000000000000000000000000000001300000000001300000000001313130000131313000013131300000013130000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e2e00000095a5a5a5b5000000000000000000000000000000000000d0e0778778885868576700000058
# 023:344454000000000000000000000000000000000000000000000000000000000000000000000000b6b6b6b6b6b6b6b6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000013000000001300000000130000000000130000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e2e00000000130013000000000000000000000095a5a5a5b5000000d1e1788893930000586800000057
# 024:354555000000000000000000000000000000000000000000000000000000000000000000000000b7b7b7b7b7b7b7b7000000000000d0e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e1e1e1e2e0000000013001300000000000000000000000000000000000000d2e2778700000000576700000058
# 025:3646560000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d1e194a4a4a4a4a4b400000094a4a4a4a4a4b40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e1e1e1e1456142e0000000013001300000095a5a5a5b50000000000000000000000d3e378880000000058680000001e
# 026:5767576757677787576700000000000000000000000000000000000000000000000000000000000000000000000000000000000000d2e295a5a5a5a5a5b500000095a5a5a5a5a5b50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e1456145614562e0000000013001300000000130013000000000000000000000000d2e277870000000000000000571e
# 027:5868586858687888586800000000000000000000000000000000000000000000000000000000000000000000000000000000000000d2e2000000000000000000000000000000000000000000000000000000000000000094a4a4a4a4a4b400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e1e1e1e5614561456142e0000000013001300000000130013000000000000000000000000d0e078881e2e0000000000005767
# 028:5767576757675767576777870000000000000000000000000000000000000000000000000000000000000000000000000000000000d2e2000000000000000000000000000000000000000000000000000000000000000095a5a5a5a5a5b5000000000000000000000000000077877787000000000000000000000000d0e05767576700000000000000000000000000576757670000000000000000000000000000000000002030000000000000000000000000000000000000000000001e5614561456145614562e0000000013001300000000130013000000000000000000000000d1e177871e2e0000000057675868
# 029:5868586858685868586878880000000000000000000000000000000000000000000000000000000000000000000000001313000000d2e2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000078887888000000000000000000000000d1e15868586800000000000000000000000000586858680000000020300000000064748400000000002131002030000000000000000000000000000000001e1e1e1e1456145614561456142e0000000013001300000000130013000000000000000000000000d2e2788877870000000058685767
# 030:5767576757675767576777877787000000000000000000697900000069796979000000000000000000000000000000131313130000d3e3000000000000000000000000000000000000000000003949590000000000000000000000000000000000000000000000000000778777877787778700000000000000000000d2e25767576700000000000000000000000000576757670000002021313000000065758500000000002131202131300414240000000000000000000000001e1456145614561456145614562e0000000013001300000000130013000000001313131313000000d3e3904078880000000093935868
# 031:58685868586858685868788878880000000000000000006a7a0000006a7a6a7a000000000000000000000000000013131394a4a4a4a4a4b44747474747474747474747474747474747000000003a4a5a0000004747474747474747474747474747470000000000000000788878887888788800000000000000000000d3e35868586800000000000000000000000000586858680000002131213100000066768600000000002131213121310414240000000000000000000000001e5614561456145614561456142e47474747134713474747471347134747131313131313131313131313576757675767576757675767
# 032:101010101010101010101010101096a696a696a696a696a696a696a696a696a696a696a65821316810101010101010101095a5a5a5a5a5b548484848484848484848484848484848481010101010101010101048484848484848484848484848484896a696a696a696a6576757675767576713131313131313131313576757675767474747474747474747474747475767576710101010101010101010101010101010101010101010101010101010101010101010101010101096a696a696a696a696a696a696a648484848134813484848481348134848111111111111111111111111a1b1a1b1a1b1a1b1a1b1a1b1
# 033:111111111111111111111111111197a797a797a797a797a797a797a797a797a797a797a7213121311111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111197a797a797a797a7586858685868586813131313131313131313586858685868484848484848484848484848485868586811111111111111111111111111111111111111111111111111111111111111111111111111111197a797a797a797a797a797a797a711111111111111111111111111111111111111111111111111111111586858685868586858685868
# 034:778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787
# 035:788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888
# 036:40000000a1b10000000000000000b6b6b6b6b6b6b60000000000000000000000000000000000000000000000000000000000000000000000b6b6b6b6778777877787778777877787778700000000000000000000004000000000009000000000000000930093000000000000000000000000000000000000783d3d3d780000000000000000000000000000000000000000000000000000000013130000000013131300000000785d5d5d5d5d7800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400077874040
# 037:4100000000000000000000000000b7b7b7b7b7b7b70000000000000000000000000000000000000000000000000000000000000000000000b7b7b7b7788878887888788878887888788800000000000000000000004100000000009100000000000000005b000000000000000000a1b1a1b1a1b10000000000783d78000000000000000000000000000000000000000000000000000000000013130000000013131300000000785d5d5d5d5d780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c36b7b8b77874040
# 038:410000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b6b6b6b6b6b67787778777877787000000000000000000000041000000000091000000000000005b5b5b0000000000000000a1b10000000000000000000078000000000000000000000000000000000000000000000000000000000013130000000000130013130000000078785d7878000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c26c7c8c78884040
# 039:410000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b7b7b7b7b7b77888788878887888000000000000000000000041000000000091000000000000000000000000000000000000a1b1000000000000000000000000000000000000000000000000000000000000000000000000000000001300000000000013000013000000000000780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c36d7d8d77874040
# 040:410000000000000000000000000000000000000000000000000000000000000000000000005767000000000000000000000000000000000000000000000000000000b6b6778777877787000000000000000000000041000b1b2b0091000000000000000000000000000000000000a1b100a1b1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001313130000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006b7b8b78884040
# 041:410000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b7b7788878887888000000000000000000000041000c1c2c0091000000000000000000000000000000000000a1b1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000131313130000000000000000000000000000000000000000000000000000000000000000000000230033000000000000000000006c7c8c77874040
# 042:4100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000094a4a4a4a4b400000000000000000000000000000000b6b677877787000000000000000000000043000d1d2d009300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000131313131300000000000000000000000000000000000000000000000000000000000000000000a0b0b0b0c00000000000000000006d7d8d78884040
# 043:4100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000095a5a5a5a5b500000000000000000000000000000000b7b7788878880000000000000000000000131313131313130000000000000000000000000000000000000000000000000000d0e0101010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000013131313131300000000000000000000000000000000000000000000000000000000000000474795a5a5a5a5a5b547470000000000c36b7b8b77874040
# 044:41000000000000000000000000000000000000000000000000000000000000000057670000000000000000000000000000000000000000000000000000000000000000000000b6b6b6b60000000000000000000013131313131313131300000000000000c2000000000000000000009bab0000000000d1e1113d1110000000000000000000000094a4a4a4a4a4a4a4b400000000000000000000000000000000000000000000000000000000000000000000131313131313130000000000000000000000000000000000000000000000000000000000000048486767676767676748480000000000006c7c8c78884040
# 045:41647484000000002030000000000000000000000050607080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b7b7b7b7000000000000000000131313131313131313131300000000100000c21000000069790000009cac0000000000d2e2113b3d11000000000000000000000095a5a5a5a5a5a5a5b50000000000006b7b8b00000000000000000000c200000000009bab000000000000131313131313131300000000006b7b8b0000c20020300000000000000000c2000000000000000067676767676767676767670000000000c26d7d8d77874040
# 046:4165758569790000213100000000000000000057675161718100000000000000000000000000000000000000000000000000000000000069796979000000000000000000000000000000000000000000000013131313131313131313131313000000113b4b5b110000006a7a0000009dad0000000000d3e3113c4c11101010101000c2000000000000000000c20000000000000000006c7c8c0000000000000013c300c313000000009cac000000000013131313131313131300000000006c7c8cc3c3c30021312030000000000098a8b80000000047476767676767676767676767676747470000006b7b8b78884040
# 047:426676866a7a000057677787470047004700475767576772820000000000000000000000000000000000000000000000000000000000006a7a6a7a000000000000000000000000000000000000000000001313131313131313131313131313132131113c4c5c11101010101010101010101010101010101011113b4b5b3d3d3d3ddddd00c3c200c30000c3000000c30000c2c30000006d7d8d00000000000013133b4b5b13130000009dad000000001313131313131313131300000000006d7d8ddbebfb1057672131203000000099a9b900000047484896a696a696a696a696a696a6a648484700006c7c8c77874040
# 048:77877787576757675767788848474847484748586858681010101010101010a600000000000000000000a610101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010113d4d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d10103c4c5c5c5cdc3d3d3d3d3ddbebfb3d3d3d3d3d3d3ddbebfb3d3d101010101010101010101010103c4c5c1010101010101010101010101010101010101010101010101010101011dcecfc115868213121310000009aaaba0000004897a797a797a797a797a797a797a7a797a74800c36d7d8d78884040
# 049:78887888586858685868576763486348634863576757675767576757675767a700000000000000000000a7675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767ddfcfcdcecfcdddddddddddddddcecfcfcdd576757675767576757675767113d4d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5dddedfd1110101010101010101010101010576757675767576757675767576757675767576757675767576757675767
# 050:101010101010101010105868a0b0c0b0a0b0c0586858685868586858685868a747474747474747474747a768586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586857675767576757675767576757675767576758685868586858685868586811111111111111111111111111111111111111111111111111111111111111111111111111a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b168
# 051:11a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a4a41111111111111111111111111111111111111111111111111111111111117787778777875868685868586858685868586858685868b6b6b6b6b6b6b600b7b70013b7b7b7b700000000b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b740778797979713979797979713979797979797979797971313131313131313131313131313131313131313131313131313131313131313131313131313131313131313131313131313131313131313131313131313c2000000000000c300c200c300000000c20000000000c30000c2000000c3
# 052:778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787788878887888b100000000000000000000005070800000b7b7b7b7b7b7b7000000001300000000000000000000000000000000000000000000000000000000000041788800000013000000000013000000000000000000000000131313131313131313000013000069790000000000000000000000000000b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6131313131313131313131313c300c200c300000000c3000000c20000c30000c200000000000000a2b200
# 053:78887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788896a696a696a6b100000000000000006979005171810000000000000000000000000013000000000000000000000000000000000000000000000000000000000000417787a300131313130000001300000000000000000000000013000013131313131300001300006a7a0000000000000000000000000000b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7131313131313131313131313000000000000c200000000c30000c300000000000000c200000000a3b300
# 054:778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787778777877787b6b6b6b6b6b6b100000000000000006a7a005272820000000000000000000000000013000000000000000000000000000000000000000000000000000000001313417888a4001300001300001313000000000000000000000000b70000001313130000000013131313131313131300000000000000000000000000000000000000000000000000000000b71313131313131313131313c300c30000000000c300000000000000c3000000c3000000c300c3000000
# 055:788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888788878887888b7b7b7b7b7b7000000000000000010101010101010100000000000000000000000001300000000000096a696a696a694a4a4a4a4a4a4a4a4b41e2e90a30000000041778700001300001300131313000000000000000000000000000000000013b7000000001300000013000000130000000000000000000000000000000000000000000000000000000000b71313131313131313131300000000c200c3000000c300c300c3000000c300000000000000000000c3
# 056:0000000000000000000000000000000000000000000000000000000000000000000000000000007787778777877787778777870000000000000000000000000000000000000000000000000000000000000000000000000000000000000013000000004057675767405767000000000000000000001e2e4113000000004178880000000000000013000000000000000000000000000000000000000000000000001300000013000000b7000000000000000000000000000000000000000000000000000000000000b713131313131313131300c2000000000000c200000000000000c2000000c200c300c200c3000000
# 057:0000000000000000000000000000000000000000000000000000000000000000000000000000007888788878887888788878880000000000000000000000000000000000000000000000000000000000000000000000000000000000000013000000004157675868415868000000000000000000001e2e41000000000041778700000000000000000000000000000000000000000000000000000000000000000013000000b70000000000000000000000000000000000000000000000000000000000000000000000b71313131313131313000000c30000c300000000c30000c3000000c3000000000000000000c200
# 058:000000000000000000000000000000000000000000000000000000000000000000000000000000000000b70000000000b700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000013a5b500004158685767415767000000000000000000001e2e41131300000041788800000000000000000000a0576700000000000000000095a5a5b500000000000000b700000000000000000000000000000000000000000000000000000000000000000000000000000000b713131313131313000000000000000000000000000000000000000000000000000000000000
# 059:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004747474747000000000013000000004157675868415868000000000000000000001e2e41a300000000417787000000000000000000a05767680000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b7b71313131313000000000000000000000000000000000000000000000000000000000000
# 060:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005767576757675767576795a5a5a5b52e00000000430000000041586857674157670000006b7b8b0000000e1e2e41130000000041788800000000000000a05767585767000095a5a5b5000000000000000000000000000000000000000095a5a5b500000000000000000000000000000000000000000000000000000000000000000000b7b713131300000000000000000000000000000000000000000000000000e4f4000000
# 061:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000047000000000000000000000000000000000000000096a696a696a696a658685868586858685868c200c300c32e00000000000000000041576758684158680e00006c7c8c00000e0e1e2e410000001313417787000000000000a087585767586800000000000000000000000095a5a5b50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b7b71300000000000000000000000000000000000000000000000000e5f5000000
# 062:000000000000000000000000000000000000000000000000000000000000000000000000000000000057675767576757670000000000000000000000000057675767506070707070707070707070707070708000c30000c2002e0000000000000095a541586857674157670e0e006d7d8d0e0e0e0e1e2e4100000000004178880000000000a087875767685767110000000000000000000000000000000000000000000000000000000000000000000000000000000000d0e0778700000000000077870000000000000000000000000000b700000000000000000000000000000000000000000000000000e600000000
# 063:0b1b2b00000000000000000000000000000000000098a8b898a8b898a8b898a8b898a8b800000000005868586858685868000000000000000000000000005868586851616100c2bbcb00c300c30000c271718100c200c300002e0414240000000000004157675868415868230e0e0e0e0e0e0e0ed21e2e43000000000043b30000000000a08757576768576768a400000000000000000000000000000000000095a5a5a5a5a5a5b5000000506070800000000000000000d1e17888000000000000788800000000000000000000000000000000000000000000000000000000000000000000000000000000e600000000
# 064:0c1c2c00000057670000000000000000576700000099a9b999a9b999a9b999a9b999a9b9000000576757675767576757675767000000000000000000576757675767516979c300bccc00006b7b8bc3c2041424c200c2006b7b8b051525000000000000435868576741576723e20e0e2333e20e0ed24087871313000000000000000000a0576757586867576767000000000000000095a5a5b5000000000000000000000000000000000000516171810000000000000000d2e27787000077870000778700000000000000000000000000000000000000000000000000000000000000000000000000000000e6f6000000
# 065:0d1d2d0000005868000000000000000058680000009aaaba9aaaba9aaaba9aaaba9aaaba000000586858685868586858685868000000000000000000586858685868526a7a00c3bdcd00c36c7c8cc20005152500c300006c7c8ca0b0b0b0b0b0b0b0c098a8b8586841586823e396a62333e396a6d341878700000000000000000000a0875767576757675767680095a5a5b5000000000000000000000000000000000000000000000000005262a1b10000000000000000d3e37888474778884747788800000000000000000000000000000000000000000000000000000000000000000000000000000000e7f7000000
# 066:576757675767576700000000000000005767576757675767576757675767576757675767576757675767576757675767576757675767576757675767576757675767b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1111111111111110e0e99a9b9576743576723e297a72333e297a7d2438787870000000000000000a087575868586858685868670e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e5767576757675767576757675767576757675767576757675767576757675767570e0e0e0e675767576757675767576757675767576757675767576757675767576757675767576757675767
# 067:586858685868586847474747474747475868586858685868586858685868586858685868586858685868586858685868586858685868586858685868586858685868a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b1a1b11111111111110e0e0e9aaaba586810586823e397a72333e397a7d37787778777877787778777877787586858685868586858680e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e5868586858685868586858685868586858685868586858685868586858685868580e0e0e0e685868586858685868586858685868586858685868586858685868586858685868586858685868
# </MAP>

# <WAVES>
# 000:00000000ffffffff00000000ffffffff
# 001:0123456789abcdeffedcba9876543210
# 002:0123456789abcdef0123456789abcdef
# 003:89abcdeeeeedcba98765432111112345
# 005:00000000ffffffff00000000ffffffff
# 011:bcceefceedddddc84333121268abaa99
# 012:fffff00000000000fffff00000000000
# 013:fffffff000000000fffffff000000000
# 014:fffffff0000000000000015ddeffabbc
# 015:01357899aabbccdeffeca65433322100
# </WAVES>

# <SFX>
# 000:a000b000b00fb000a000f000f000f000f000f000f000f000f070f000f000f000f000f000f000f001f000f003f000f000f000f000f000f000f000f000344000000000
# 001:a200920082007200723072006200620052005200420042000200020002000200020002000200020002000200020002000200020002000200020002000000000c0500
# 002:c300c300c300c300c3000300030003000300030003000300030003000300030003000300030003000300030003000300030003000300030003000300000000050000
# 003:330043004300430043005300530053005300630063006300630063007300730073008300830083009300930093009300a300a300b300b300b300b300100000000000
# 004:44008400e4008400e400c400e400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400502000000000
# 005:f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400f400e400d4f0c4c0b490a460946094b084f074f0437000000000
# 006:b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000b000304000000000
# 007:0497047504540442144214411441145414502450246f346f347f448f448f448f548e548e548e648e648d748d749d849d849d94ada4cdc4dce4fcf4fc112000000000
# 008:3748873837188748476897485708a70867099709470a970b670b970c770db70e670fb70f8701d7029703d703c704d705d706d706d707d707e707f700360000000000
# 009:e700970f670ed70df700e70dc70ca70b570cf700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700b60000000000
# 010:0af01ac02ab03aa04a905a806a707a608a409a30aa30ba20ca20da10da10ea10fa00fa00fa00fa00fa00fa00fa00fa00fa00fa00fa00fa00fa00fa00304000000500
# 011:07168730076d1777470e8708e700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700370000000406
# 012:5596859695d5a5b4b593c592c59fd59ed58de58de57ce56cf55cf53bf53bf52af51af519f518f518f508f508f508f508f508f508f508f508f508f508300000000400
# 013:11f721d631c441a35191518f617c716981589150a140a140b130c130d120e120f120f120f120f120f120f120f120f120f120f120f120f120f120f120307000000009
# 014:0807081608250834084308520861087f088e289d48ac68bb88caa8d9c8e8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8d80000000000
# 015:3708570837f157ffa7f7c7f7d7f7d7f7e7f7e7f7f7f7770887089708b708c708c708e708e708e708e708e708f708f708f708f708f708f708f708f708900000000000
# 016:c6077604060416013600460f560e760d860ca60bb60ac609c609d600d600d600e600e600e600f600f600f600f600f600f600f600f600f600f600f600b6000000000d
# 017:0f001f005f009f00bf00bf00bf00bf00bf00bf00bf00bf00bf00bf00bf00bf00cf00cf00cf00cf00cf00cf00cf00df00df00df00df00ef00ef00ff00375000000000
# 018:de00de00ce00ce00ce00ce00ce00be00be00be00be00be00ae00ae00ae00ae00ae009e009e009e009e008e008e008e008e007e007e007e007e006e00b75000000000
# 019:3d004d00bd00cd00cd00dd00dd00dd00dd00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00ed00fd00400000000000
# 020:3c004c00bc00cc00cc00dc00dc00dc00dc00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00ec00fc00405000000000
# 021:090b090729036900990ec90de90ce90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90bf90ba05000000000
# 022:090219071902090739008903d904e905f906f906f906f907f907f907f907f907f907f907f907f907f907f907f907f907f907f907f907f907f907f907b05000000000
# 023:0b000b000b000b000b005b008b008b009b009b009b00ab00ab00ab00ab00ab00bb00bb00bb00bb00cb00cb00cb00db00db00db00eb00eb00eb00fb00481000000000
# </SFX>

# <PATTERNS>
# 000:405400455102400000066100723204777100000000000000000000000000000000000000000000100000100000100000100000000000000000000000000000000000100000000000723204777100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 001:b33116000010a11716100050100210100210e00214b01716a80716000010100010000010000000000000000000000000b10614b00018a11716000000e00014b00016002410a00018000000000000100010000010000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 002:433638000000000000000000000040000040000040000000000030000000000000000000933636000000000000000000000040000040000000000000000030000000000000000000c33636000000000000000030000030000000000000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 003:40004600004000000000000090004e00004000000000000000004000004000004000000000004000004000000000000040004600004000000000000002325040005e10005000000000004000004000005040004e40004e40004e40004e100040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 004:100050400056100050100050100050100050100050100050100050400054100050100050100050400058100050100050100050100050100050100050100050100050100050000050000050404756100050400054100050400054100050100050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 005:455162100060400062100060500062100060400062100060400062100060400062100060500062100060400062100060400062100060400062100060500062100060400062100060700062100060500062100060400062100060400062100060100060100060900066100060c00066100060b00066100060100060100060900066100060c00066100060b00066100060100060100060900066100060c00066100060b00066100060900066100060700066100060600066100060400066100060
# 006:822162100060800062100060900062100060800062100060800062100060800062100060900062100060800062100060800062100060800062100060900062100060800062100060b00062100060900062100060900062100060900062100060100060100060d00064100060500066100060f00064100060100060100060d00064100060500066100060f00064100060100060100060d00064100060500066100060f00064100060d00064100060b00064100060a00064100060800064100060
# 007:455166100060400066100060500066100060400066100060400066100060400066100060500066100060400066100060400066100060400066100060500066100060400066100060700066100060500066100060400066100060400066100060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060
# 008:433160100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000000000000000400060000000100060000000000000000000000000000000400060000000100060000000000000000000000000000000400060000000100060000000000000000000000000000000000000000000000000000000000000000000
# 009:a88136000000000000000000000000000000000000000000000030000000400036000000600036000000000000000030000030000000000000000000000030000000000000000030c00036000000000000000000000000000000000000000000000000000030800036000030a00036000000000000000000000000000000000000000000000000000000000000000000b00036000000000000000000000000000000600036000000000030000000900036000000000030000000d00036000000
# 010:155150000000100050100050100050100050100050100050100050100050000000000000000000100050100050000000100050100050100050100050400058100050100050100050100050100050000000000000000000000050000000000000000000100050100050000000100050100050000000000000100050100050000000100050400058100050100050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 011:055100000000100010000000d10412000000100010000010000000000000000000000400100010000000000000000000000000000000000000000000000000000010000000000010000010000010100010000000100010000000000000000000000000000000000000000000000000000000000000000000100010000010100010000010100010000000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 012:055100000000100010000000d00012000000100010000010000000000000000000000400100010000000000000000000000000000000000000000000000000000010000000000010000010000010100010000000100010000000000000000000000000000000000000000000000000000000000000000000100010000010100010000010100010000000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 013:055100000000100010000000b00018000000100010000010000000000000000000000400100010000000000000000000000000000000000000000000000000000010000000000010000010000010100010000000100010000000000000000000000000000000000000000000000000000000000000000000100010000010100010000010100010000000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 014:cbb117000011000011000000000011a00019000011000000c00017000000800017000000000011000000000000000000c00017000011000011000030000000000030000000000011000000000011000011000011000011000011000011000011000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 015:b88155100041000041000000477169100041000041000000b881551000410000110000004771691000410000000000000000110000110000110000300000000000300000004bb1694881690000114bb1694881694bb1694bb1694881694bb169000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 016:c88123000050000050000050000000000000000000000000000000000000000000000000000000000000000000000050000050000050000050000050800023000050000050000000000050000050000050000050000050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 017:0bb100000000c00037c00037000000000030000030000030000000000000000030000030c00037c00037000000000000000000000030000030000030000000000030c00037c00047c00037c00047c00037000030000030000030000030000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 018:c00025000000000000000000700025000000000000000000500025000000000000000000000000000000000000000000000000000000000000000000800025000000000000000000700025000000000000000000a00025000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 019:c00037000000700037000000c00037000000000000000000900037700037500037000000700037d00037000000600037000000900047000000c00037800037500037c00037000000000000700047900047900037900037b00047d00037f00047000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 020:8bb179a00079600079000000900079000000000000000000b00079000000000000800079000000600079000000800079800079a00079600079000000900079000000000000000000b00079000000000000800079b00079000000800079000000000000000000000000000000000000000000000000000000000000000000000000800079000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 021:800023000000000000000000100021000000000000000000800023000000000000000000100021000000000000000000000000000000000000000000b00023000000000000000000100021000000000000000000b00023000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 022:800075a00075600075000000900075000000000000000000b00077000000000000800077000000600077000000800077800075a00075600075000000900077000000000000000000b00077000000000000800077b00077000000800077000000000000000000000000000000000000000000000000000000000000000000000000800079000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 023:8bb129000000000000000000100021000000000000000000800027000000000000000000100021000000000000000000000000000000000000000000b00023000000000000000000100021000000000000000000b00023000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </PATTERNS>

# <TRACKS>
# 000:0003000003000003000003000803000803000803000803001803000803001803000803001803411803411003410803417e0200
# 001:6c1842000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000bf0020
# 002:a00000a00000a00c00a00000ac2c00ac2d00ac2000ac2e00ac2c00ac2d00ac2000ac2c00ac2e00ac2d00a00000a00000ec0100
# 003:f00000f00000f00110f00110f00194f00194f04084f00394f00394f00394f04005f00315f00315f00315f04310f00000000210
# 004:8100008d50008d50008d50006d50006d50006550006550008550008550000000000000000000000000000000000000006f0200
# </TRACKS>

# <PALETTE>
# 000:1a1c2cff008cffff37ba794c9d4c288913e8f548371a1a4d182489ffc6951824ca61daf7f4f4f49daeca5d6d9138b764
# 001:040400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </PALETTE>

