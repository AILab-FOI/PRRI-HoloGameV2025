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
                if tileHere != 0 and tileHere not in level_finish_tile_indexes and tileHere not in background_tile_indexes:
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
                if tileHere != 0 and tileHere not in level_finish_tile_indexes and tileHere not in background_tile_indexes:
                    pos_key = ("x", xx + px, "y", yy + py)
                    if pos_key not in collidables:
                        collidables[pos_key] = collidable((xx + px)*tile_size, (yy + py)*tile_size, tile_size, tile_size)

    return list(collidables.values())



