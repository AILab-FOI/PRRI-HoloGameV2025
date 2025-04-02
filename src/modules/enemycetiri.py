#lista projektila
projectiles = []
class Enemy4:
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
    detection_range = 70  # Domet detekcije za pucanje
    vertical_range = 20  # Domet vertikalne detekcije (ne koristi se u ovom primeru, ali može se proširiti)

    def __init__(self, x, y):
        tile_size = 8
        self.x = x * tile_size
        self.y = y * tile_size

    def movement(self, coll):
        self.coll = coll
        self.dx = 0  # Pozicija ne menja
        self.vsp = 0  # Gravitacija je samo za vertikalno kretanje, ali ovde nije potrebna

        # Pomakni neprijatelja da prati poziciju igrača
        if not self.dead:
            if player.x < self.x:  # Ako je igrač levo od neprijatelja
                self.desno = False  # Neprijatelj se okrene levo
            elif player.x > self.x:  # Ako je igrač desno od neprijatelja
                self.desno = True  # Neprijatelj se okrene desno

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
        projectile = Projectile(self.x + 5, int(self.y))  # Kreiranje novog projektila na poziciji neprijatelja
        projectile.desno = self.desno  # Projektile idu u smeru u kojem neprijatelj "gleda"
        projectiles.append(projectile)  # Dodavanje projektila u listu
        sfx(1, "D-2", 3, 0, 2, 3)  # Zvuk prilikom pucanja

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
