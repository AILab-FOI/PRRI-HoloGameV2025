#lista projektila
projectiles = []
class Enemy5:
    x = 90
    y = 90
    width = 16
    height = 16
    sprite = 1  
    dx = 0  # Ne menja se pozicija u horizontalnom pravcu
    vsp = 0
    gravitacija = 0.3
    skokJacina = 3
    minY = 120
    desno = False
    shotTimer = 0  # Timer za pucanje
    shotFreq = 1  # Koliko često puca
    coll = []
    health = 2
    dead = False
    detection_range = 70  
    vertical_range = 20

    def __init__(self, x, y):
        tile_size = 8
        self.x = x * tile_size
        self.y = y * tile_size

    def movement(self, coll):
      self.coll = coll
      self.dx = 0  # Horizontal movement speed (not used for movement, just for logic)
      self.vsp = 0  # Vertical speed (gravity is handled below)

         if not self.dead:
          if player.x < self.x:  
            self.desno = False 
          elif player.x > self.x:  
            self.desno = True 

         
          if self.desno:
              if not self.ProvjeriKolizije(1, 0):  
                  self.x += 1  
          else:
              if not self.ProvjeriKolizije(-1, 0): 
                  self.x -= 1 

      self.shotTimer += 1

    # Pucanje ako je igrač u dometu
      if abs(player.x - self.x) <= self.detection_range and self.shotTimer >= 60 * self.shotFreq and not self.dead:
          self.shootProjectile()  # Ispaljivanje projektila
          self.shotTimer = 0  # Reset timer za sledeće pucanje

    # Crtanje neprijatelja na ekranu
      if not self.dead and self.desno:
          spr(320, int(self.x) - int(pogled.x), int(self.y) - int(pogled.y), 6, 1, 0, 0, 2, 2)
      elif not self.dead:
          spr(320, int(self.x) - int(pogled.x), int(self.y) - int(pogled.y), 6, 1, 1, 0, 2, 2)

    def shootProjectile(self):
        projectile = Projectile(self.x + 5, int(self.y))  
        projectile.desno = self.desno  
        projectiles.append(projectile) 
        sfx(1, "D-2", 3, 0, 2, 3)  

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
