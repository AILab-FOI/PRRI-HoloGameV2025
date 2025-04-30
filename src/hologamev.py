# title:   HoloGameV
# author:  AILab-FOI
# desc:    short description
# site:    https://ai.foi.hr
# license: GPLv3
# version: 0.1
# script:  python


state='menu' #varijabla za game state
level = 0 # koji level je ucitan (od 0 pa na dalje)
hacked_enemy = None
player_backup = None

def TIC():
 update_keys()

 Final()

 global state

 if state=='game':
   IgrajLevel()
   if level == 0:
     print("Keys (AD) for moving left and right", 0, 16)
     print("Keys (WS) for moving up and down by laders", 0, 24)
     print("Key (B) for jump, key (E) for weapon change", 0, 32)
     print("Key (F) for shooting. Be aware of lava nad spikes!!!", 0, 40)
     print("Touching the enemy also decreases health!!!", 0, 48)
     print("Key (shift) for dash", 0, 56)
     print("Key H for hacking the enemy and G is for killing the enemy", 0, 64)
 elif state=='menu':
   menu.Menu()
 elif state=='over':
   menu.Over()
 elif state=='win':
   menu.PrikaziZaslonPobjede()

def Final():
	cls(13) 

prev_key_space = False
prev_key_switch = False

def update_keys():
    global key_space, key_left, key_right, key_up, key_down, key_shoot, key_switch, key_dash, key_hack, key_return, key_selfdestruct 
    global prev_key_space, prev_key_switch, prev_key_dash

    current_key_space = key(48) # 'SPACE' ili 'START' ili 'B' na gamepadu (prirodno skakati na B, a birati na 'START')
    current_key_switch = key(5) # 'E' ili 'SELECT' na gamepadu
    current_key_dash = key(64)

    key_space = current_key_space and not prev_key_space
    key_switch = current_key_switch and not prev_key_switch
    key_dash = current_key_dash and not prev_key_dash

    key_left = key(1) # 'A' ili lijevo na gamepadu
    key_right = key(4) # 'D' ili desno na gamepadu
    key_up = key(23) # 'W' ili gore na gamepadu
    key_down = key(19) # 'S' ili dolje na gamepadu
    key_shoot = key(6) # 'F' ili 'A' na gamepadu
    key_hack = key(8) # 'H'
    key_selfdestruct = key(7) # 'G'
    key_return = key(18) #'R'
    prev_key_space = current_key_space
    prev_key_switch = current_key_switch
    prev_key_dash = current_key_dash
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
                if tileHere != 0 and tileHere not in level_finish_tile_indexes and tileHere not in level_locked_tile_indexes and tileHere not in background_tile_indexes:
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
                if tileHere != 0 and tileHere not in level_finish_tile_indexes and tileHere not in level_locked_tile_indexes and tileHere not in background_tile_indexes:
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
    48, 49, 64, 65, 80, 81, 96, 97
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
    health = 5
    hitTimer = 10
    hitVar = 0
    enemyHit = False


    def PlayerKontroler(self, coll):
        global hacked_enemy, player_backup
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
            if self.ProvjeriKolizije(self, 0, 1) or self.y>=self.minY or self.ctVar < self.coyoteTime or self.on_ladders:
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
#lista projektila
projectiles = []
def HackedEnemyController(enemy, coll):
    enemy.coll = coll
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

def ReturnToPlayer():
    global hacked_enemy, player, player_backup
    hacked_enemy = None
    if player_backup:
        player = player_backup
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

  def __init__(self, x, y):
    tile_size = 8
    self.x = x*tile_size
    self.y = y*tile_size

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
        if not self.dead and self.x <= 0:
            self.dx = 1  # mijenja stranu kad takne lijevu stranu
            self.desno = True
        elif not self.dead and self.x >= pogled.ogranicenjeX:
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
    spr(104, self.x - int(pogled.x), self.y - int(pogled.y), 0, 1, 0, 0, 1, 1)
      
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

  def __init__(self, x, y):
    tile_size = 8
    self.x = x*tile_size
    self.y = y*tile_size

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
    if not self.dead and self.x <= 0:
      self.dx = 1  # mijenja stranu kad takne lijevu stranu
      self.desno = True
    elif not self.dead and self.x >= pogled.ogranicenjeX:
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
      spr(326,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
    elif not self.dead:
      spr(326,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)

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

  def __init__(self, x, y):
    tile_size = 8
    self.x = x*tile_size
    self.y = y*tile_size

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
    if not self.dead and self.x <= 0:
      self.dx = 1  # mijenja stranu kad takne lijevu stranu
      self.desno = True
    elif not self.dead and self.x >= pogled.ogranicenjeX:
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
      spr(352,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,0,0,2,2)
    elif not self.dead:
      spr(352,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),15,1,1,0,2,2)

  def shootProjectile(self):
    projectile = Projectile(self.x + 5, int(self.y), 3) 

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
     


class menu:
    m_ind=0

    def Menu():
        global state
        cls(0)
        menu.AnimateFrame()
        menu.AnimateTitle()

        # Opcije menija
        rect(1,48+10*menu.m_ind,238,10,2)
        print('Play', 100, 50, 4, False, 1, False)
        print('Quit', 100, 60, 4, False, 1, False)

        #  Šetanje po opcijama na meniju
        if key_down and 48+10*menu.m_ind<50: #ako se budu dodavale još koje opcije, promijeniti uvijet
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
        if(time()%500>250):
            print('NEON ESCAPE', 57, 20, 6, False, 2, False)
        elif(time()%500>150):
            print('NEON ESCAPE', 57, 20, 2, False, 2, False)
        elif(time()%500>350):
            print('NEON ESCAPE', 57, 20, 3, False, 2, False)
        elif(time()%500>550):
            print('NEON ESCAPE', 57, 20, 10, False, 2, False)

    def AnimateFrame():
        if(time()%500>250):
            rectb(0,0,240,136,6)
        elif(time()%500>150):
            rectb(0,0,240,136,2)
        elif(time()%500>350):
            rectb(0,0,240,136,3)
        elif(time()%500>550):
            rectb(0,0,240,136,10)

    def AnimateWinTitle():
        if(time()%500>250):
            print('YOU WON!', 80, 50, 6, False, 2, False)
        elif(time()%500>150):
            print('YOU WON!', 80, 50, 6, False, 2, False)
        elif(time()%500>350):
            print('YOU WON!', 80, 50, 6, False, 2, False)
        elif(time()%500>550):
            print('YOU WON!', 80, 50, 6, False, 2, False)
            
    def Over():
        cls(0)
        print('GAME OVER', 75, 50, 2, False, 2, False)
        print('START (space) for restart', 58, 70, 4, False, 1, False)

        
        if key_space:
            reset()

    def PrikaziZaslonPobjede():
        global state
        cls(0)
        menu.AnimateFrame()
        menu.AnimateWinTitle()

        print('START (space) for exit', 62, 70, 4, False, 1, False)

        if key_space:
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
        if key_switch:
            Puska.PromijeniPusku()
      
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
    [5, 28], # level 1
    [9, 44], # level 2
    [3, 63], # level 3
    [3, 72] # nepostojeci opet peti level
]
level_finish_tile_indexes = [ # indexi tileova sa vratima za zavrsetak levela
    50, 51, 52, 
    66, 67, 68, 
    82, 83, 84,
    211, 212, 213, 
    227, 228, 229, 
    243, 244, 245
]

level_locked_tile_indexes = [ # indexi tileova sa zakljucanim vratima
    161, 162, 163,
    177, 178, 179,
    193, 194, 195
]

background_tile_indexes = [ # indexi tileova sa elementima koji nemaju definiraju koliziju (pozadinski elementi)
	69, 70, 71, 
	56, 57, 58, 72, 73, 74, 
	85, 86, 87, 
	102, 103,
    88, 89, 90,
    118, 119, 120, # zuti stol, no ima problem jer neki leveli koriste sredinu stola za platformu
    48, 49, 64, 65, 80, 81, 96, 97, # ljestve
    104, 11, 30,
    59, 231, 247,
    219, 220, 221, 222, 223, # oni "ormarici"
    235, 236, 237, 238, 239,
    251, 252, 253, 254, 255,
    133, 134, # torta
]
enemies = [ # pocetne pozicije enemyja za svaki level (u editoru se ispisuje koja)
    [Enemy(77, 14)], # level 0
    [Enemy(60, 30),Enemy(79, 30), Enemy(182, 35)], # level 1
    [Enemy2(139, 46), Enemy2(79, 46), Enemy2(58, 46), Enemy2(127, 46), Enemy2(184, 46), Enemy2(174, 46)], # level 2
    [Enemy3(64, 62), Enemy3(154, 56), Enemy3(167, 61), Enemy3(206, 65), Enemy3(197, 65)] # level 3
]
pickups = [ # pocetna pozicija pick up pusaka za svaki level (u editoru se ispisuje koja)
    [], # level 0
    [PromjenaPuska(130, 22, 1)], # level 1
    [PromjenaPuska(168, 40, 2)], # level 2
    [] # level 3
]
lava = [ # tile lave
    59
]
spikes = [ # tileovi spikeova
    231, 247
]

# sljedece varijable NE MIJENJATI:
LEVEL_HEIGHT = 17

def ZapocniLevel(level): # poziva se u menu.py kada se odabere opcija da se uđe u level
    tile_size = 8
    starting_pos = player_starting_positions[level]
    player.x = starting_pos[0]*tile_size
    player.y = (starting_pos[1] - LEVEL_HEIGHT*level)*tile_size
    pogled.x = max(0, player.x - (pogled.w - player.width)/2)
    player.hsp = 0
    player.vsp = 0
    if level == 0:
       music(1, 0, -1)
    elif level == 1:
        music(0, 0, -1)

def IgrajLevel():
    cls(0)
    map(0, level*LEVEL_HEIGHT, 240, 18, -int(pogled.x), -int(pogled.y), 0)
    HUD()
    tile_size = 8
    levelEnemies = enemies[level]
    for enemy in levelEnemies:
        while (enemy.y > LEVEL_HEIGHT*tile_size):
            enemy.y -= LEVEL_HEIGHT*tile_size
    collidables = DefinirajKolizije([player, levelEnemies, metci, projectiles], level, LEVEL_HEIGHT)
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
    ProvjeravajJeLiIgracULavi()
    ProvjeravajJeLiIgracNaSiljku()

def ProvjeravajJeLiIgracKodVrata():
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

        # locked door?
        if tile in level_locked_tile_indexes:
            print("[!] Vrata su zaključana", 10, 10, 12)
            return

        # finish door?
        if tile in level_finish_tile_indexes:
            sfx(16, "C-4", 15, 0, 2, 1)
            ZavrsiLevel()
            return
    
def ProvjeravajJeLiIgracULavi():
    tile_size = 8
    kojiTile = mget(round(player.x/tile_size), round(player.y/tile_size) + level*LEVEL_HEIGHT)
    if kojiTile in lava:
        sfx(8, "C-4", 15, 0, 2, 1)
        player.Pogoden(player, 1)
    
def ProvjeravajJeLiIgracNaSiljku():
    tile_size = 8
    kojiTile = mget(round(player.x/tile_size), round(player.y/tile_size) + 1 + level*LEVEL_HEIGHT)
    if kojiTile in spikes:
        sfx(8, "C-4", 15, 0, 2, 1)
        player.Pogoden(player, 1)

def ZavrsiLevel():
    global level
    level = level + 1
    if level <=3:
        ZapocniLevel(level)
    else:
        global state
        state = 'win'

def HUD():
    rect(0, 0, 240, 8, 0)
    print("Level:" + str(level), 1, 1, 12, True, 1, False)
    # Prikaz zivota
    spr(364, 50, 0, 6, 1, 0, 0, 1, 1)
    rect(60, 1, player.health*10, 5, 6)
    if player.health > 0:
        rect(60+player.health*10, 1, 50-player.health*10, 5, 3)
        print(str(player.health) + "HP", 120, 1, 12, True, 1, False)
    else: 
        print("0HP", 120, 1, 12, True, 1, False)
    # Prikaz puske i metaka
    spr(Puska.svespr[Puska.p[Puska.tp]], 150, 0, 6, 1, 0, 0, 1, 1)

# <TILES>
# 000:7777777777777777777777777777777777777777777777777777777777777777
# 001:8888888888888888888888888888888888888088888888888888888888888888
# 002:9999999999999999999999999999999999999999999999999999999999999999
# 003:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
# 004:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 005:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
# 006:77dddddd7deeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee7deeeeee77dfffff
# 007:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 008:dddddf77eeeeeef7eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeef7ffffff77
# 009:dddddddfdeeeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdfffffff
# 010:dddddddfdeeeeeefdedeefefdeeeeeefdeeeeeefdedeefefdeeeeeefdfffffff
# 011:dddddddddd9eafa8d9eafad8deafad98dafad9e8dfad9ea8dad9eaf8d8888888
# 012:77dddddd7deeeeeedeedeeeedeeeeeeedeeeeeeedeedeeee7deeeeee77dfffff
# 013:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 014:dddddf77eeeeeef7eeeefeefeeeeeeefeeeeeeefeeeefeefeeeeeef7ffffff77
# 015:dddddddd7777777777777777ffffffff77777777777777777777777777777777
# 016:dddddddddeeeeeeededdeeeededdeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 017:ddddddddeeeeeeefeeeeffefeeeeffefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 018:ffffffffffeeeeeefefeeeeefeefeeeefeeefeeefeeeeffffeeeeff2feeeef2f
# 019:ffffffffeeeeeeffeeeeefefeeeefeefeeefeeeffffeeeef2ffeeeeff2feeeef
# 020:777ddddd77deeeef7deeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdfffffff
# 021:ddddf777feeeef77feeeeef7feeeeeeffeeeeeeffeeeeeeffeeeeeefffffffff
# 022:777ddddd77deeeee7deeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 023:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 024:ddddf777eeeeef77eeeeeef7eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 025:777ddddd77deeeee7deeddeedeeeddeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 026:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 027:ddddf777eeeeef77eeffeef7eeffeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 028:3333333333444444343444443443444434443444344443443444443434444443
# 029:3333333344444433444443434444344344434443443444434344444334444443
# 030:8888888888bbbb888b8bb8b88bb88bb88bb88bb88b8bb8b888bbbb8888888888
# 031:ddddddddd77777770f77777700ffffff00000000000000000000000000000000
# 032:deeeeeeedeeeeeeedeeeeeeedeeeeeeededdeeeededdeeeedeeeeeeeffffffff
# 033:eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeffefeeeeffefeeeeeeefffffffff
# 034:feeeef2ffeeeeff2feeeeffffeeefeeefeefeeeefefeeeeeffeeeeeeffffffff
# 035:f2feeeef2ffeeeeffffeeeefeeefeeefeeeefeefeeeeefefeeeeeeffffffffff
# 036:dfffffffdeeeeeefdeeeeeefdeeeeeefdeeeeeef7deeeeef77deeeef777fffff
# 037:fffffffffeeeeeeffeeeeeeffeeeeeeffeeeeeeffeeeeef7feeeef77fffff777
# 038:deeeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee7deeeeee77deeeee777fffff
# 039:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 040:eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeef7eeeeef77fffff777
# 041:deeeeeeedeeeeeeedeeeeeeedeeeddeedeeeddee7deeeeee77deeeee777fffff
# 042:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 043:eeeeeeefeeeeeeefeeeeeeefeeffeeefeeffeeefeeeeeef7eeeeef77fffff777
# 044:3444444334444434344443443444344434434444343444443344444433333333
# 045:3444444343444443443444434443444344443443444443434444443333333333
# 046:3333333333444433343443433443344334433443343443433344443333333333
# 047:dddddddd7777777d777777f0ffffff0000000000000000000000000000000000
# 048:dddddddddd777777dddddddddd777777dddddddedd777777dddddeeedd777777
# 049:dddeeeee777777eedeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777ee
# 050:dddddddddeeeeeeedeeeeeeedeeeeeeedeeeffffffefddedffefdedddeefedde
# 051:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeffffffffdeeddddeeeddddededdddedd
# 052:dddddddfeeeeeeefeeeeeeefeeeeeeefffffeeefddddfeffdddefeffddeefeef
# 053:77aaaaaa7aaaaaaaa8888888a8aa8aa8a8aa8aa8a88888887a88888877aaaaaa
# 054:aaaaaaaaaaaaaaaa88888888aa8aa8aaaa8aa8aa8888888888888888aaaaaaaa
# 055:aaaaaa77aaaaaaa78888888a8aa8aa8a8aa8aa8a8888888a888888a7aaaaaa77
# 056:7777777877777784777778447777844477784444778444487888888784884877
# 057:8888877783384877833844878888444887784448777788887777788877777778
# 058:777777777777777777777777877777778777777788888877eeeee887e8888e88
# 059:2222222222222222222222222222222222222222222222222222222222222222
# 060:3333333333333333333333333333333333333333333333333333333333333333
# 061:4444444444444444444444444444444444444444444444444444444444444444
# 062:1111111111111111111111111111111111111111111111111111111111111111
# 063:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 064:dddeeeeedd777777ddeeeeeede777777deeeeeeede777777deeeeeeede777777
# 065:eeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777ee
# 066:deefddeedeefdeeddeeeffffdeeeeeeedeeeeeeedeeddddddeedeeeedeedeeee
# 067:ddddeddddddeddddffffffffeeeeeeeeeeeeeeeeddddddddeeeeeeeeeeeeeeee
# 068:deedfeefeeddfeefffffeeefeeeeeeefeeeeeeefddddfeefeeeefeefeeeefeef
# 069:ddddddddd77777777f77777777ffffff7777f7777777f7777777f7777777f777
# 070:dddddddd7777777777777777ffffffff77777777777777777777777777777777
# 071:dddddddd7777777f777777f7ffffff777777f7777777f7777777f7777777f777
# 072:8888887784884877888888877844444877844444777844447778444477888888
# 073:7777777877777778777777787777777887777777877777778777777788777777
# 074:e87778e8e8777787e8777777ee8777778ee87777788777777777777777777777
# 075:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# 076:7777777777777777777777777777777777777777777777777777777777777777
# 077:6666666666666666666666666666666666666666666666666666666666666666
# 078:5555555555555555555555555555555555555555555555555555555555555555
# 079:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 080:eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777
# 081:eeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777ee
# 082:deedeeeeffedeeeeffedeeeedeedeeeedeedffffdeeeeeeedeeeeeeedfffffff
# 083:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffffeeeeeeeeeeeeeeeeffffffff
# 084:eeeefeefeeeefeffeeeefeffeeeefeeffffffeefeeeeeeefeeeeeeefffffffff
# 085:ddddddddd33383337f33383377ffffff7773f7777773f7777773f7777773f777
# 086:dddddd8d8333383333333833ffffffff77777777777777777777777777777777
# 087:dddddddf3333333f333833f7ffffff777773f7777773f7777773f7777773f777
# 088:77888888ddeeeeefddeeeeeeddeeeeeeddeeeeeeddeeeeeeddeeeeeeddeeeeee
# 089:88777777ffff7777ffff7777ffff7777ffff7777ffff7777ffff7777ffff7777
# 090:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 091:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 092:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 093:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 094:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 095:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 096:eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777
# 097:eeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777eeeeeeeeee777777ee
# 098:ddf77777deef7777deeedddddeeeeeeedeeeeeeedeeeffffdeef7777dff77777
# 099:7777777777777777ddddddddeeeeeeeeeeeeeeeeffffffff7777777777777777
# 100:7777777777777777ddddddddeeeeeeeeeeeeeeeeffffffff7777777777777777
# 101:77777ddf7777deefddddeeefeeeeeeefeeeeeeefffffeeef7777deef77777dff
# 102:7777774877777848777788477774447777788777777887777784487778888887
# 103:8777777788bb777788bbb777bbbbb7777bbbb777777777777777777777777777
# 104:ddddddd8dbbbbbb8d9999998dbbbbbb8d9999998dbbbbbb8d9999998d8888888
# 105:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 106:cccccccccc6666ccc66cc66cc6cccc6c66666666666666666666666666666666
# 107:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 108:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 109:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 110:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 111:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 112:888888888fffffff8fff22228222ff3382ff333f8f3333ff83322fff8fff2222
# 113:88888888ffffff33223333ff33ff2222fffff3fff3333fff3ffffff222f22f2f
# 114:8888888833333338fff3fff8233f33f822222228fffff33822fffff8ff2ffff8
# 115:ffffffffffeeeeeefefeeeeefeefeeeefeeefeeefeeeeffffeeeeff5feeeef5f
# 116:ffffffffeeeeeeffeeeeefefeeeefeefeeefeeeffffeeeef5ffeeeeff5feeeef
# 118:ddddddddd44444447f44444477ffffff7774f7777774f7777774f7777774f777
# 119:dddddddd4444444444444444ffffffff77777777777777777777777777777777
# 120:dddddddd4444444f444444f7ffffff777774f7777774f7777774f7777774f777
# 121:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 122:eaeeeeeeeaaeeeaeeeeaeeaeeaeaeaaeeaaaaaeeeeeaaeeeeaaaaaaaeeeaeeee
# 123:eeeeeebbeeeeeeebeeeeeeeeeeeeebbeeebeeebeebbebebbbbbebebbbbeebeeb
# 124:bbbbbbbbbbbbbbbbbbbbbbbbebbeebbbeeeeebbeeeeeeeeeeeeeeeeeeeeeeeee
# 125:bbbbbbeeeeebbeeebeeeeeeebbbbeeeebbbbeeeebbbbbeeebbbbeeeebeeeeeee
# 126:eeeeebbbeeeebbbbeeeeebbbeeeeeebbebeebbbbebbeebbbbbbeeebbbbbbeeeb
# 127:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 128:82fff3ff832333ff8ff2fff28fff222f8f33333f83fffff38fffffff88888888
# 129:ff2ff2ffffffffff2ffffff32f22233ff2ff22fffff3322f3333ff2288888888
# 130:fff22ff8fffff2f833fffff8ff33f228ffff2ff8fff2f3f8ff2fff3888888888
# 131:feeeef5ffeeeeff5feeeeffffeeefeeefeefeeeefefeeeeeffeeeeeeffffffff
# 132:f5feeeef5ffeeeeffffeeeefeeefeeefeeeefeefeeeeefefeeeeeeffffffffff
# 133:777777777777777777777777777777727777cccc7777c33c7777333377773333
# 134:77777777777777777777777727777777cccc7777c33c77773333777733337777
# 135:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 136:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 137:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 138:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 139:0000000000000000000000000000000000000000000000060000006600000666
# 140:0000000000000000000000000000000000000000666666666666666666666666
# 141:0000000000000000000000000000000000000000666666666666666666666666
# 142:0000000000000000000000000000000000000000600000006600000066600000
# 143:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 144:ddddddddd34444440ff43434000fffff00000000000000000000000000000000
# 145:dddddddd4444444434343434ffffffff00000000000000000000000000000000
# 146:dddddddd4444443d34343ff0fffff00000000000000000000000000000000000
# 147:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 148:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 149:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 150:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 151:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 152:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 153:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 154:beeebeebbbeebbbeebeebbeeeebbbbeeeeebbbbeeebbbeebebebbbeebeebeebe
# 155:0000066600000666000006660000066600000666000006660000066600000666
# 156:666666666666666666ccc6666cccc6666cc66666ccccc666ccccc6666cc6666c
# 157:6666666666666666666666cc666666cc66666666666666cccc6666ccccc666cc
# 158:6660000066600000666000006660000066600000666000006660000066600000
# 159:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 160:0000000088888888888888888888888888888888888880888888888888888888
# 161:eeeeeeeee6666666e6000000e6000000e6002222e6002222e6002222e6002222
# 162:eeeddeee666dd666000dd000000dd000200dd002200dd002200dd002200dd002
# 163:eeeeeeee6666666e0000006e0000006e2222006e2222006e2222006e2222006e
# 164:4444444444444440444444004444400044440000444000004400000040000000
# 165:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 166:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 167:4444444404444444004444440004444400004444000004440000004400000004
# 169:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 170:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 171:0000066600000666000006660000066600000666000006660000066600000666
# 172:6cc666cc6cc666cc6cc6666c6cc666666cc66666666666666666666666666666
# 173:66cc66cc66cc66ccccc666cccc6666cc666666cc666666666666666666666666
# 174:6660000066600000666000006660000066600000666000006660000066600000
# 175:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 176:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 177:e6000000e6000000e6000000e6000000e6000000e6000000e6000000e6000000
# 178:000dd000000dd000000dd000044dd440044dd440000dd000000dd000000dd000
# 179:0000006e0000006e0000006e0000006e0000006e0000006e0000006e0000006e
# 180:4444444404444444004444440004444400004444000004440000004400000004
# 181:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 182:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 183:4444444444444440444444004444400044440000444000004400000040000000
# 184:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 185:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 186:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 187:0000066600000066000000060000000000000000000000000000000000000000
# 188:6666666666666666666666660000000000000000000000000000000000000000
# 189:6666666666666666666666660000000000000000000000000000000000000000
# 190:6660000066000000600000000000000000000000000000000000000000000000
# 191:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 192:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 193:e6000000e6000000e6000000e6000000e6000000e6000000e6666666eeeeeeee
# 194:000dd000000dd000000dd000000dd000000dd000000dd000666dd666eeeddeee
# 195:0000006e0000006e0000006e0000006e0000006e0000006e6666666eeeeeeeee
# 196:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 197:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 198:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 200:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 201:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 202:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 203:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 204:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 205:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 206:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 207:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 208:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 209:3333333343333333443333334443333344443333444443334444443344444443
# 210:3333333333333334333333443333344433334444333444443344444434444444
# 211:eeeeeeeeefffffffef000000ef000000ef002222ef002222ef002222ef002222
# 212:eeeddeeefffddfff000dd000000dd000200dd002200dd002200dd002200dd002
# 213:eeeeeeeefffffffe000000fe000000fe222200fe222200fe222200fe222200fe
# 214:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 215:2222222232222222332222223332222233332222333332223333332233333332
# 216:2222222222222223222222332222233322223333222333332233333323333333
# 217:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 218:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 219:e0000000e0000000e0000000e0000000e0000000e0000000e0000000e0000000
# 220:0000000e0000000e0000000e0000000e0000000e0000000e0000000e0000000e
# 221:e00ddddde00ddddde0000000e0000000e0000000e0000000e0000000e0000000
# 222:d00ee00dd00ee00d000ee000000ee000000ee000000ee000000ee000000ee000
# 223:ddddd00eddddd00e0000000e0000000e0000000e0000000e0000000e0000000e
# 224:667ee77c76676777777776676766776e77676777ee7666677ee77ede677e777c
# 225:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 226:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 227:ef000000ef000000ef000000ef000000ef000000ef000000ef000000ef000000
# 228:000dd000000dd000000dd000044dd440044dd440000dd000000dd000000dd000
# 229:000000fe000000fe000000fe000000fe000000fe000000fe000000fe000000fe
# 230:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 231:777ee777777ee77777edce7777edce777edddce77edddce7eedddceeedddddce
# 232:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 233:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 234:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 235:e0000000e0000000e0000000e0000000e0000000e0000000e0000000e0000000
# 236:0000000e0000000e0000000e0000000e0000000e0000000e0000000e0000000e
# 237:e0000000e0000000e0000000e0000000e0000000e0000000e0000000e00fffff
# 238:000ee000000ee000000ee000000ee000000ee000000ee000000ee000f00ee00f
# 239:0000000e0000000e0000000e0000000e0000000e0000000e0000000efffff00e
# 240:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 241:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 242:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 243:ef000000ef000000ef000000ef000000ef000000ef000000efffffffeeeeeeee
# 244:000dd000000dd000000dd000000dd000000dd000000dd000fffddfffeeeddeee
# 245:000000fe000000fe000000fe000000fe000000fe000000fefffffffeeeeeeeee
# 246:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 247:eddddddeeddddddeeddddddeeddddddeeddddddeeddddddeeddddddeeeeeeeee
# 248:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 249:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 250:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 251:e0000000e0000000e0000000e0000000e0000000e0000000e0000000e0000000
# 252:0000000e0000000e0000000e0000000e0000000e0000000e0000000e0000000e
# 253:e0000000e00fffffe0000000e00fffffe0000000e0000000eeeeeeeeeeeeeeee
# 254:000ee000f00ee00f000ee000f00ee00f000ee000000ee000eeeeeeeeeeeeeeee
# 255:0000000efffff00e0000000efffff00e0000000e0000000eeeeeeeeeeeeeeeee
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
# 066:666666fe66666fee6666feee6666ffee66666ffe666666ff66666ee066666e03
# 067:d6666666ed66666622d66666eed66666ed666666e66666660e66666640666666
# 068:666666fe66666fee6666feee6666ffee66666ffe666666ff66666ee066666e03
# 069:d6666666ed66666622d66666eed66666ed666666e66666660f66666630fefeff
# 070:fff00000ff00ddddfb0ddd00fb0dd006ff0dd060fb0ed060ffa0ee06ff000eee
# 071:0fffffff00ffffffe00fffff6e0fffff2e0fffff4e0fffff600fffff00ffffff
# 072:fffbff00fffff0ddffbf0dddffbb0dd0fffb0dd0ffba0ed0fffaa0eeffff000e
# 073:000fffffddd0fbff000d0fff06600bff60260bff60460fff06600fffee00ffff
# 074:ffffff00fffff00dffff00ddffff0eddffff0eddffff0eedffff00eefffff000
# 075:000fffffddd0ffffdddd0fffd0660fffd0620fffd0660fffee000fffeee0ffff
# 076:a6666888aaa68999a9989999a99999ff6a999fdd66a9fddd6699fd226699fd22
# 077:886666f69986fff6999888f6f99988f6df998f66ddf986662df9f6662df9f666
# 080:fffff0ddfffff0edffffff0dfffffff0ffffff0dffffff07ffffff0bffffff0b
# 081:ded0ffffdee0ffffeee0ffffdee0ffffe770ffff7770ffff7bb0ffffb0bb0fff
# 082:6666eee06666eeee6666efee66666ffe66666fee6666fee66666fe6666666ff6
# 083:0e666666e0666666ee666666ed666666fe666666ffe66666fee66666ff666666
# 084:6666eee06666eeee6666efee66666ffe66666fee6666fee66666fe6666666ff6
# 085:0effeff6eff6f666ee66f666ed666666fe666666ffe66666fee66666ff666666
# 086:f0dd0000f0d00ddd0ee00ee00e000000f00dd000ff0e0ff0f000fff0f000fff0
# 087:0e0fffff000ffffff0e0fffff000ffff0fffffffefffffffe0ffffff00ffffff
# 088:fff0dd00fff0d00dfff0e00efff0ee00ffff00d0fffff0e0ffff000fffff000f
# 089:00000fffddd00fffee00d0ff00f000ff000ffffff0effffff0e0fffff000ffff
# 090:ffff0de0ffff0d00ffff0ee0ffff0ee0fffff00effffff00fffff00ffffff000
# 091:000fffffee0fffffe000ffff0000ffff000ffffff00ffffff0e0fffff000ffff
# 092:66a99fd266a999ff6a9a9999a9999888a9999986999999869999998669988866
# 093:df99f666f998f66699898f66889998f6899998f6899999f6899999f66888ff66
# 096:a6666a99aaa6a999aa9a9999aa9999ff6aa99fdd66a9fddd6699f2226699f222
# 097:886666f69986fff6999888f6f99998f6df998f66ddf98666ddf9f666ddf9f666
# 098:a6666a99aaa6a999aa9a9999aa9999ff6aa99fdd66a9fddd6699f2226699f222
# 099:886666f69986fff6999888f6f99998f6df998f66ddf98666ddf9f666ddf9f666
# 100:a6666888aaa68999a9989999a99999886a99982266a982236698223366982334
# 101:886666f69986fff6999888f6899988f628998f66228986663228f6663328f666
# 102:a6666888aaa68999a9989999a99999886a99982266a982336698233466982344
# 103:886666f69986fff6999888f6899988f628998f66328986663328f6664328f666
# 104:0000000000500000555555550575000005500000050000000000000000000000
# 105:0000000000aaa000a00a0000baabaaaaaa0a0a000aa00a000a00000000000000
# 106:0000000000000000bbbbb0bb00bbbb000b0000bbbbbb0bb00000000000000000
# 107:0000000000000000002222200000000000222220000000000000000000000000
# 108:000000000cc00cc0c6cccc6cc66cc66cc666666ccc6666cc0cc66cc000cccc00
# 112:66a99f2d66a999ff6aaa9999aa999999a9999996999999866999886666666666
# 113:df99f666f999f66699998f66899998f6899998f6899999f6899999f66888ff66
# 114:66a99f2d66a999ff6aaa9999aa999999a9999986a99999869999998669998866
# 115:df99f666f999f66699998f66899998f6899999f6899999f66888ff6666666666
# 116:66a8223366a982236a9a8222a9999888a9999986999999869999998669988866
# 117:3228f6662289f66622898f66889998f6899998f6899999f6899999f66888ff66
# 118:66a8233466a982336a9a8222a9999888a9999986999999869999998669988866
# 119:3328f6663289f66622898f66889998f6899998f6899999f6899999f66888ff66
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
# 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 001:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 002:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 003:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 004:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 005:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a2a3a000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 006:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001b2b3b000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 007:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003130000000000000000000000000000000000000000000000000000000000001c2c3c000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 008:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000414000000000000000000000000000000000000000000000000000000004040404040404003134040400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 009:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000515374737473747374700000000000000000000000000000000000000000000000000000004140000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 010:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000616384838483848384800000000000000000000000000000000000000000000000000000005150000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 011:000000000000000000000000000000000000000000000000011100000000000000000000000000000000000000000616374737473747374700000000000000000000000000000000000000000000000000000006160000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 012:0000000000000000000000000000000000415100000000000212000000000000000000000000000000000000000006163848384838483848000000000000000000003d4d5d000000000000000000000000000003130000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 013:00000000000000000000000000000000a090907e7e7e7e91a1b1000000000000000000000000000000000000000006163747374737473747000000000000f10000003e4e5e000000000000000000000000000004140000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 014:404040404040404040404000000000a0a090a07f7f7f7f92a2b2000000007e7e7e7e7e7e7e7e0000000000000000061638483848384838480000000000007f0000003f4f5f000000000000000000000000000005150000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 015:4040404040404040404040404040404040404040404040404040404040407f7f7f7f7f7f7f7f00000000000000000515374737473747374700000000006171717171717171718100000000000000000000000006160000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 016:404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040384838483848384840404040406272727272727272728240404040404040404040404040404040400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 017:000000000000900000000000000000000000000000000000000000000000001d001d00001d00000000001d00000000000000000000900b0b0b90000000000000000000000000000000000000000000000000000000000000000000000090900000000090900000009090000000000000000000000000000000000000000000000000000000001d0000001d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a9a900a900000000a9a9a90000000000a900a9000000000000000000000000000000000000
# 018:000000000000900000000000000000000000000000000000000000000000001d001d00001d00000000001d00000000000000000000900b0b0b900000000000000000000000000000000000000000000000000000000000000000000000909000000000a0a00000009090000000000000000000000000000000000000000000000000000000001d0000001d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a900a900000000a9a9a90000000000a900a9000000000000000000000000000000000000
# 019:000000000000900000000000000000000000000000000000000000000000001d001d00001d00000000001d00000000000000000000900b0b0b90000000000000000000000000000000000000000000000000000000000000000000000090900000000000000000009090000000000000000000000000000000000000000000000000000000001d0000001d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a900a9000000a9a900a90000000000a900a9a90000000000000000000000000000000000
# 020:000000000000900000000000000000000000000000000000000000000000001d001d00001d00000000001d0000000000000000000062720b7282000000000000000000000000000000000000000000000000000000000000000000000090900000000000000000009090909090000000000000000000000000000000000000000000000000001d0000001d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a900a90000000000a900a9000000000000000000000000000000000000
# 021:000000004190909051000000000000000000000000000000000000000000001d001d0000607070707070800000000000000000000000900b9000000000000000000000000000000000000000000000000000000000031300000000000090900000000000000000009090000000000000000000000000000000000000000000000000000000607070707070800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a900000000000000000000000000000000000000000000003d4d5d0000
# 022:000000009000000090000000000000000000000000000000000000000000001d001d0000000000000000000000000000000000000000901b90000000000000000000000000000000000000000000000000000000000414000000000000909000000000000000000090900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000031300000060707070800000000000000000000000000000000000000313000000000000003e4e5e0000
# 023:000000004200000052000000000000000000000000000000000000000000001d001d0000000000000000000000000000000000000000900b90000000000000000000000000000000000000000000000000000000000515a0a000000000909000000000a0a0000000909000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000414000000001d001d00000000000000000000006070707080000000041400007e7e0000003f4f5f0000
# 024:0000000000000000000000000000000000000000000000000000000000000060708000000000000000000000000000000000000000900b0b1b90000000000000000000000000000000000000000000000000000000061690900000000090900000000090900000009090000000000000000000000000000000000000000090900e000e000e000e000e0e000e0e0e0e000e90909090000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009090900515000000001d001d0000000000a9a900000000001d001d000000000515909090909090909090909090
# 025:00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000901b0b901b0b9000000000000000000000000000000090909090000000000000000616909000000000a0a0909000009090000000a0a0000000000000000000000000607070800000000090900d0e00000e0e0000000e0e0e0d0d0e0e0090909090000000000000000000000000000000000000000000000000000000000000000000000000000000000000009090909090900616000000001d001d0000006070707080000000001d001d000000000616909090909090909090909090
# 026:000000000000000000000000000000000000000000000000a9a9a900000000000000000000000000000000000000000000000000901b1b901b1b900000000000000000000000000000909090011100000000000000061690900000000000000000000090900000000000000000000000000000000000001d1d000000000090900d0d0e000d0e000e000e0d0d0e0e0d0e0e90909090000000000000000000000000000000000000009090000000000000000000000000000000000000000000009086869090900515000000001d001d000000001d001d00000000001d001d000000000515909090909090909090909090
# 027:00000000000000000000000000000000000000000090909090909000000000000000000000000000000000000000000000000000900000900000900000000000000000000000000090909090021200000000000000061690900000000000000000000090900000000000000000000000000000000000001d1d000000000090900d0e0d0e0d0d0e0e000e0e0e0d0e0d0d0e90909090000000000000000000000090900000000000009090e2e200000000000000000000000000000000009090909086869090900616000000001d001d000000001d001d00000000001d001d000000000616909090909090909090909090
# 028:000000000000000000000000002131000000000000000000000000000000000000008393a300000000000000000000000000000090000090000090000000000000000000000000909021313747e100000000000000061690900000000000000000000090900000000000000000006070708000000000001d1d000000000090900e0d0e0d0e0e0e0d0e0d0d0e0e0e0e0d0e90909090000000000000000000009090909090900000909090e2e2e2000000000000000000000000000000009086869086869090900515000000001d001d000000001d001d00000000001d001d000000000515909090909090909090909090
# 029:0000000000000000000000000022320000000000cdddedfdddedfdbd0000000000008494a400000000000000000000000000000000000000000000000000000000000000009090909022323848e10000000000000006169090000000000000000090909090000000000000000000001d1d0000000000001d1d00000000009090909090909090909090909090909090909090909090000000000000000090909090909090900000909090e2e2e2e20000000000000000000000009090909086869086869090900616000000001d001d000000001d001d00000000001d001d000000000616909090909090909090909090
# 030:00a9a9a90000000000a700003747374700000000cedeeefedeeefebe0000000000008595b000000000000058680000000000000000000000000000000000000000000090909090902131374701110000000000000006169090000000000000009090909090000000000000000000001d1d0000000000001d1d00000000009090909090909090909090909090909090909090909090000000000000009090909090909090907e7e909090e2e2e2e2e2e2e20000000000000000009086869086869086869090900515000000001d001d000000001d001d00000000001d001d000000000515909090909090909090909090
# 031:00a9a9a99090909090a7a7a93848384800000000cfdfefffdfefffbf000000000055656575000000005464646464740000000000000000000000000000000000009090909090909022323848021200000000000000061690907e7e00000000909090909090000000000000000000001d1d7e7e7e7e7e7e1d1d7e7e7e7e7e90909090909090909090909090909090909090909090907e7e7e7e7e7e7e9090909090909090907f7f909090e2e2e2e2e2e2e2e200000000000000009086869086869086869090900616000000001d001d7e7e7e7e1d001d7e7e7e7e7e1d001d7e7e7e7e0616909090909090909090909090
# 032:9090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090a0a09090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090
# 033:909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090
# 034:000000000000000000007b8b7b8b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 035:404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040
# 036:400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040404040
# 037:400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001110111011101110111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000263646562636465626364656263646560000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003130000000000000000000000000040404040
# 038:400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002120212021202120212000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004140000000000000000000000000040404040
# 039:400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005154171510000000000000000000040404040
# 040:400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006164272520000000000000000000040404040
# 041:4000000000000000000000000000000000000000000000000000c0d0e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0d0e000000000c0d0e00000000000000000000000000000000000000000000000000000000000000000000000000000031300000000000000c0d0e000000000c0d0e000000000000000000000000000000000000000000000000000000000c0d0e0000000000000c0d0e0000000000313000000000000000000000000000000000000000000000000000000000000000000000005150000000000000000000000000040404040
# 042:400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000414000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000414000000000000000000000000000000000000000000000000000000000000000000000006160000000000000000000000000040404040
# 043:40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006070708000000000000000000000000000000000041440909090909090000000000000909090909090000000000000909090909040051500000000000000000000000000000000000000000000000000000000000000000000000000000000c0d0e00000000000000000000000000000000000000515909090909090909000000000000000909090909090909000000000000090909090909005150000000000000000000000000040404040
# 044:40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000051540b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b340061600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000061640b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34006160000000000000000000000000040404040
# 045:4000000000000000000000400000000000000000000000000000000000000000006070800000607080000000000000000000000000000000000000000000000000008393a300000000000000000000000000000000000000061640b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34006160000000000000000008393a300000000000000000000000000000000000000000000000000000000000000008393a30000000000000000000000000000051540b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34005150000000000000000233343000040404040
# 046:4000000058680000004040400000000000000040404000000000667686000000000000000000000000000000000000011100000000000000000000004151000000008494a4b0b0b000000000000000000000000000000000051540b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34005150000000000000000008494a400000000000000000000000000404040000000000000004040400000000000008494a4e100000000000000000000000000061640b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34006160000000000000000243444000040404040
# 047:400000005565750040404040b3b3b3b3b3b3b340404040000000677787000000000000000000000000000000000000021200000000000000000000004252000000008595a567778700000000000000000000000000000000061640b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34006160000000000000000008595a500000000000000000000000040400000000000000000000000404000000000008595546474000000000000000000000000061640b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34006167e7e7e7e7e7e0000253545000040404040
# 048:404040404040404040404040b3b3b3b3b3b3b3404040404040404040404040400000000000000000000040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34040404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34040404040404040404040404040404040404040
# 049:404040404040404040404040b3b3b3b3b3b3b340404040404040404040404040b3b3b3b3b3b3b3b3b3b340404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34040404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34040404040404040404040404040404040404040
# 050:404040404040404040404040b3b3b3b3b3b3b340404040404040404040404040b3b3b3b3b3b3b3b3b3b340404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b34040404040404040404040404040404040404040404040404040404040b3b3b3b3b3b3b3b3b3b3b34040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040
# 051:30302020201010102020203030c78233330000000000000000000000000000000000000000000000000000007ad3d3d3d31dc3c37db3b3b3b3b3b3b3b3b3b3b3b38dc3c32dd3d3d3d3d34aa0a00000a0a0000000a0a000000040120000404000000000000000000000000000000000000000000000000000000000000030303026364656263646562636465626364656263646562636465626364656263646562636465626364656263646562636465626364656101010101020202020202020202020101010101010101010202020202020202020202020101010101010101010101010101010203030303030303030
# 052:303030202020101010203030c782003434000000000000000000000000000000000000000000000000000000007ad3d3d3d3c3c3c3c37db3b3b3b3b3b3b3b38dc3c32dd3d3d3d3d3d34a00a0a00000a0a0000000a0a0000000401200004040000000000000000000000000000000000000000000000000000000000000403030000000000000000000000000000000000000000000000000000000000000000000f1f0f0f0f200000000000000000000000000001010101020202030c7c7c7c7c7302020101010101010101020303030303030303020202020101020202020101010102020202020c7c7c7c7c7c73030
# 053:30303030202020202030c7c782000033330000000000000000000000000000000000000000000000000000000000007ad3d31dc3c3c3c3c3c3c3c3c3c3c3c3c3c32dd3d3d3d3d34a000000a0a00000a0a000000040a000000012120000404000000000000000000000000000000000000000000000000000000000000040e730a300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020101010203030304040404040c730202020101010102030303030c740c7c7c7303030302020202030302020201020202030c74082e262404040c7c7
# 054:c7c730303030303030c7404000e1003434000000000000000000000000000021213131a30000000000000000000000007ad3d3d31dc3c3c3c3c3c3c3c3c3c3c32dd3d3d3d34a0000000000a040000040a0000000a0a0000000404000004090000000000000000000000000000000000000000000000000000000000919403030a40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f1f0f0f0202020202030404040b20040a940c73030202020202030303030c74040404040c7c7c7c7303030c7c73030302020202030c74082000919624040a940
# 055:4040c7c7c7c7c7c7c74040820009196282000000000000000000000000000022223232a400000000000000000000000000007ad3d3d31dc3c3c3c3c3c32dd3d3d3d3d34a00000000000000a04000004040000000a04000000062820000409000000000000061404040404019191919191919191919404040a300000000404030000000000000000000000000000000000000000000000000000000f1f0f0f0f0f200000000f1f0f200000000000000000000000030202020203040b200000092404040c7303030303030c7c7404040409240404040404040c7c7c74040c7c73030303030c74082000000000000624040
# 056:40a9404040404040404082e10000000000000000000000000000000000000010213110000000000000000000000000000000007ad3d3d31dc3c3c3c32dd3d3d3d3d34a0000000000000000a0a000006282000000404000000000000000409000000000614090909090404000000000000000000000404040a40000000040403000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c730302020304000e10000009240404040c7303030c7404040a940400092400092a9404040404040404040c7303030c7408200e20000000000006240
# 057:40404040820000624082192900000000000000000000000000000000000000102232000000000000000000000000000000000000007ad3d3d3d3d3d3d3d3d34a000000000000000000000040a00000000000000040400000000000000090900000000040409023334390400000000000000000000040404000000000004040400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f1f0f0f0f0f20000403030303040b2646400000000009240404040c7c74040404040404000000000006240820000000062404040c7c7c740401919290000000000000062
# 058:0000000000000000000000000000000000000000000000000000000000001010213100000000000000000000000000000000000000007ad3d3d3d3d3d3d34a0000000000000000000000006282000000000000004040000000000000009040192900004040902434449040000000000000000000004040401929000000404040000000000000000000004040400000000000000000f1f0f0f0f0f20000000000000000000000000000000000000000000000000040c73040404000000000000000000092404040404040404040404082e20000000000000000000000e262404040404040820000000000000000000000
# 059:0000000000000000000000008393a30000008393a300000000000000001010102232000000000000008393a30000000000000000000000007ad3d3d34a00000000000000000000000000000000000000000000006282000000000000009090000000004040902535459040000000000000000000e2404040a3000000004040400000000000000000004040a9400000000000000000000000000000000000000000000000000000000000000000000000000000004040404040b200000000000000000000924037474040a940404082646400000000000000000000006464646240a94082000000000000000000000000
# 060:0000000000000000000000008494a40000008494a400000000000000002690909090905600000000008494a4000000000000000000000000007ad34a0000000000000000000000000000000000000000000000000000000000000000006282000000004040903030909040e20000000000000000b3404040a40000000040a9a9000000000000004040404040300000f1f0f0f200000000000000000000000000000000000000f1f0f0f0f2000000000000000000404040404000000000000000000000e10040384840404040408200000000000000000000000000000000000062408200000000000000000000000000
# 061:000000000000000000000000409090909090905050564646464646269090909090909090564626404040404040a940000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004040303020309040b3000000000000e2b3b3404040000000091940404000000000000040404040303030000000000000000000000000f1f0f0f2000000000000000000000000000000000000000000000040a94040b2e1000000000000000000646492404040404082000000000000000000000000000000000000000000000000000000000000000000000000
# 062:00000000000000404040404040409090909050505050505050505050505090909090909040404040404040404040404000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000091940a9302020303040b3b3e2000000b3b3b3b3404040000000000040404000000000004040404030303030a3000000000000000000000000000000000000000000000000000000000000000000000000000040404040646400000000000000000000000040a940408200000000000000000000000000000000000000000000000000000000000023334300000000
# 063:000000000000404090909040409030b73090909090905050374750909090303030303090909040303090233343909090a9000000000000000000000000000000000000000000000000000040000000000000000000004040000000000000000000000040a9302020203040e3b3b3b3b3b3b3b3b3e34040400000000000404000000000004040a9403030303030a40000000000000000000000000000000000f1f0f0f0f0f0f0f0f2000000000000000000000000404040b20000000000000000000000000000624040820000000000000000000000000000000000000000000000000000000000000024344400000000
# 064:00000000004040902333439090b73020303090909090909038489090909030302020303030909030304024344440409026464646464646464646464646464646464646464646464656404040304040304040263646564030404000000000000000000040903020202030a9e3e3b3b3e3e3e3b3b3e340303019290000000000000000004040404040303020202000000000000000f1f0f0f0f2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000025354500000000
# 065:009090909090303024344490303020202030303030903030b7303030303030202010102030303030203030303090404000000000000000000000000000000000000000000000000000909030304030203040404040404020309040404040264646465640302020102030a9e3e3e3e3e3e3e3e3e3e340303000000000000000000000404040403030302020202000f1f0f0f20000000000000000000000000000000000000000000000f1f0f0f0f0f20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000374721313747000000
# 066:404040404030202030354530302020101020203030303020202020202020202010102020202020202020202030909090a300000000000000000000000000000000000000000000000090402020202020203030309090902020203030404040404040403020201010202030e3e3e3e3e3e3e3e3e3e3403020300000000000000000404040303030302020101010a3000000000000000000000000f1f0f0f0f0f0f2000000000000000000000000000000000000000000000000e1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000384822323848000000
# 067:403030303030202020202020202010101020202020202020101010101020101010102010101010101020202030303030a400000000000000000000000000000000000000000000009090302010101010202020303040402010103030303040404040303020201010102030e3e3e3e3e3e3e3e3e3e33020202030404040404040404040303030302020201010107e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7ef1f0f0404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040
# 124:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 125:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 126:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 127:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 128:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 129:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 130:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 131:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 132:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 133:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 134:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 135:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </MAP>

# <WAVES>
# 000:00000000ffffffff00000000ffffffff
# 001:0123456789abcdeffedcba9876543210
# 002:0123456789abcdef0123456789abcdef
# 003:89abcdeeeeedcba98765432111112345
# 005:00000000ffffffff00000000ffffffff
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
# 010:0ef01ec02eb03ea04e905e806e707e608e409e30ae30be20ce20de10de10ee10fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00fe00304000000500
# 011:07168730076d1777470e8708e700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700f700370000000406
# 012:5596859695d5a5b4b593c592c59fd59ed58de58de57ce56cf55cf53bf53bf52af51af519f518f518f508f508f508f508f508f508f508f508f508f508300000000400
# 013:11f721d631c441a35191518f617c716981589150a140a140b130c130d120e120f120f120f120f120f120f120f120f120f120f120f120f120f120f120307000000009
# 014:0c070c160c250c340c430c520c610c7f0c8e2c9d4cac6cbb8ccaacd9cce8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8fcf8d80000000000
# 015:3708570837f157ffa7f7c7f7d7f7d7f7e7f7e7f7f7f7770887089708b708c708c708e708e708e708e708e708f708f708f708f708f708f708f708f708900000000000
# 016:c6077604060416013600460f560e760d860ca60bb60ac609c609d600d600d600e600e600e600f600f600f600f600f600f600f600f600f600f600f600b6000000000d
# </SFX>

# <PATTERNS>
# 000:405400455102400000066100723204777100000000000000000000000000000000000000000000100000100000100000100000000000000000000000000000000000100000000000723204777100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 001:b33116000010a11716100050100210100210e00214b01716a80716000010100010000010000000000000000000000000b10614b00018a11716000000e00014b00016002410a00018000000000000100010000010000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 002:433638000000000000000000000040000040000040000000000030000000000000000000933636000000000000000000000040000040000000000000000030000000000000000000c33636000000000000000030000030000000000000000030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 003:40004600004000000000000090004e00004000000000000000004000004000004000000000004000004000000000000040004600004000000000000002325040005e10005000000000004000004000005040004e40004e40004e40004e100040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 004:100050400056100050100050100050100050100050100050100050400054100050100050100050400058100050100050100050100050100050100050100050100050100050000050000050404756100050400054100050400054100050100050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 005:400062100060400062100060500062100060400062100060400062100060400062100060500062100060400062100060400062100060400062100060500062100060400062100060700062100060500062100060400062100060400062100060100060100060900066100060c00066100060b00066100060100060100060900066100060c00066100060b00066100060100060100060900066100060c00066100060b00066100060900066100060700066100060600066100060400066100060
# 006:800062100060800062100060900062100060800062100060800062100060800062100060900062100060800062100060800062100060800062100060900062100060800062100060b00062100060900062100060900062100060900062100060100060100060d00064100060500066100060f00064100060100060100060d00064100060500066100060f00064100060100060100060d00064100060500066100060f00064100060d00064100060b00064100060a00064100060800064100060
# 007:400066100060400066100060500066100060400066100060400066100060400066100060500066100060400066100060400066100060400066100060500066100060400066100060700066100060500066100060400066100060400066100060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060000060
# 008:400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000400060100060000000000000000000000000400060000000100060000000000000000000000000000000400060000000100060000000000000000000000000000000400060000000100060000000000000000000000000000000000000000000000000000000000000000000
# </PATTERNS>

# <TRACKS>
# 000:0003000003000003000003000803000803000803000803001803000803001803000803001803411803411003410803417e0200
# 001:6c1842000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000bf0010
# </TRACKS>

# <FLAGS>
# 000:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </FLAGS>

# <PALETTE>
# 000:1a1c2cff008cffff37ba794c9d4c288913e8f548371a1a4d182489ffc6951824ca61daf7f4f4f49daeca5d6d9138b764
# 001:040400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </PALETTE>

