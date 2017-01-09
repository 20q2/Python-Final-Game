import pygame

class TileCache:
    """Load the tilesets lazily into global cache"""

    def __init__(self,  width=32, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load it from disk if needed."""

        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""

        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), frames=None):
        super(Sprite, self).__init__()
        self.state = 0
        self.frames = frames
        self.animation = self.stand_animation(self.state)
        self.image = frames[0][0]
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.name = "default"
        self.expire = -1
        

    def stand_animation(self,state):
        while True:
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None

    def update(self, *args):
        self.animation.next()
        self.expire = self.expire -1
        if self.expire == 0:
            self.kill()
        
    def _get_pos(self):
        """Check the current position of the sprite on the map."""

        return (self.rect.midbottom[0]-12)/24, (self.rect.midbottom[1]-16)/16

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""

        self.rect.midbottom = pos[0]*24+12, pos[1]*16+16
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
