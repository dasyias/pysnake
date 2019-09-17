import pyglet
import random


class Player():
    def __init__(self, img, x, y, batch, thicc, scrsize):
        self.image = img
        self.thicc = thicc
        self.batch = batch
        self.scrsize = scrsize
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.blocks = [pyglet.sprite.Sprite(img=self.image, x=x, y=y, batch=self.batch)]
        self.score = 0

    def is_inside_head(self, obj):
        return self.blocks[0].x == obj.x and self.blocks[0].y == obj.y

    def is_inside_body(self, obj):
        for block in self.blocks[1:]:
            if block.x == obj.x and block.y == obj.y:
                return True
        return False

    def is_inside(self, obj):
        for block in self.blocks:
            if block.x == obj.x and block.y == obj.y:
                return True
        return False

    def set_direction(self, dir):
        if not self.is_inside(pyglet.sprite.Sprite(img=self.image,
                                                   x=self.blocks[0].x + dir[0] * self.thicc,
                                                   y=self.blocks[0].y + dir[1] * self.thicc)):
            self.direction = dir

    def get_score(self):
        return self.score

    def update(self, food):
        self.blocks.insert(0, pyglet.sprite.Sprite(img=self.image,
                                                   x=self.blocks[0].x + self.direction[0] * self.thicc,
                                                   y=self.blocks[0].y + self.direction[1] * self.thicc,
                                                   batch=self.batch))
        if self.is_inside_head(food):
            self.score += 1
            return "eat"
        del self.blocks[-1]
        if self.blocks[0].x > self.scrsize[0] - self.thicc // 2 or\
                self.blocks[0].x < self.thicc // 2 or\
                self.blocks[0].y > self.scrsize[1] - self.thicc // 2 or\
                self.blocks[0].y < self.thicc // 2 or\
                self.is_inside_body(self.blocks[0]):
            return "gameover"
        return

