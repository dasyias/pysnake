import pyglet
import random
import player
import sys
import shelve
from pyglet.gl import *

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

key = pyglet.window.key


class main(pyglet.window.Window):
    def __init__(self):
        self.render_size = 640, 480
        self.window_size = 1280, 960
        super().__init__(self.window_size[0], self.window_size[1],\
                caption="PySnake")
        glScalef(self.window_size[0] / self.render_size[0],\
                self.window_size[1] / self.render_size[1], 0)
        # self.set_size(self.window_size[0], self.window_size[1])

        self.set_icon(pyglet.resource.image("icon.png"))

        self.thicc = 20

        self.blink_counter = 0

        self.scfile = shelve.open("score")
        self.highscores = [0, 0, 0, 0]
        self.get_highscores()

        pyglet.font.add_file("resources/8bitOperatorPlus-Regular.ttf")
        self.font = pyglet.font.load("8-bit Operator+", 18)

        self.player_image = pyglet.resource.image('sblock.png')
        self.food_image = pyglet.resource.image('fblock.png')
        self.grid_image = pyglet.resource.image('gblock.png')
        self.wall_image = pyglet.resource.image('wblock.png')
        self.pausecover = pyglet.resource.image("pausecover.png")

        self.pausecover.width = self.render_size[0]
        self.pausecover.height = self.render_size[1]

        self.center_image(self.player_image)
        self.center_image(self.food_image)
        self.center_image(self.grid_image)
        self.center_image(self.wall_image)
        self.center_image(self.pausecover)

        # START GRID BATCH #
        self.grid_batch = pyglet.graphics.Batch()
        self.grid = []

        for x in range(1, self.render_size[0] // self.thicc):
            for y in range(1, self.render_size[1] // self.thicc):
                self.grid.append(pyglet.sprite.Sprite(self.grid_image, x*self.thicc, y*self.thicc,
                                                      batch=self.grid_batch))
        # END GRID BATCH #

        # START WALL BATCH #
        self.wall_batch = pyglet.graphics.Batch()
        self.wall = []

        for x in range(0, self.render_size[0] // self.thicc + 1):
            for y in range(0, self.render_size[1] // self.thicc + 1):
                if x == 0 or y == 0 or x == self.render_size[0] // self.thicc or y == self.render_size[1] // self.thicc:
                    self.wall.append(pyglet.sprite.Sprite(self.wall_image, x*self.thicc, y*self.thicc,
                                                          batch=self.wall_batch))

        # START MAIN BATCH #
        self.main_batch = pyglet.graphics.Batch()

        self.player = player.Player(self.player_image, self.render_size[0]//2, self.render_size[1]//2,
                                    self.main_batch, self.thicc, self.render_size)

        self.food = None
        self.reset_food(self.food_image, self.render_size, self.main_batch)
        # END MAIN BATCH #

        # START SCORE BATCH #
        self.score_batch = pyglet.graphics.Batch()
        self.score_label = pyglet.text.Label(text="SCORE: 0", x=self.thicc, y=self.thicc, batch=self.score_batch,
                                             font_name="8-bit Operator+", font_size=18)
        # END SCORE BATCH #

        # START MENU BATCH #
        self.start_batch = pyglet.graphics.Batch()
        self.title_label = pyglet.text.Label(text="PYSNAKE", x=self.render_size[0]/2, y=self.render_size[1]/2+100,
                                             anchor_x="center", anchor_y="center", font_name="8-bit Operator+",
                                             font_size=48, batch=self.start_batch)
        self.startinst_label = pyglet.text.Label(text="PRESS SPACE", x=self.render_size[0]/2,
                                                 y=self.render_size[1]/2-100, anchor_x="center", anchor_y="center",
                                                 font_name="8-bit Operator+", font_size=28)
        # END MENU BATCH #

        # START DIFFSELECT BATCH #
        self.diffselect_batch = pyglet.graphics.Batch()
        self.diffselect_label = pyglet.text.Label(text="DIFFICULTY", x=self.render_size[0]/2,
                                                  y=self.render_size[1]/2+150, anchor_x="center", anchor_y="center",
                                                  font_name="8-bit Operator+", font_size=36,
                                                  batch=self.diffselect_batch)
        self.easy_label = pyglet.text.Label(text="EASY", x=self.render_size[0]/2, y=self.render_size[1]/2+50,
                                            anchor_x="center", anchor_y="center", font_name="8-bit Operator+",
                                            font_size=28, batch=self.diffselect_batch)
        self.med_label = pyglet.text.Label(text=">MEDIUM<", x=self.render_size[0]/2, y=self.render_size[1]/2,
                                           anchor_x="center", anchor_y="center", font_name="8-bit Operator+",
                                           font_size=28, batch=self.diffselect_batch)
        self.hard_label = pyglet.text.Label(text="HARD", x=self.render_size[0]/2, y=self.render_size[1]/2-50,
                                            anchor_x="center", anchor_y="center", font_name="8-bit Operator+",
                                            font_size=28, batch=self.diffselect_batch)
        self.expert_label = pyglet.text.Label(text="EXPERT", x=self.render_size[0]/2, y=self.render_size[1]/2-100,
                                              anchor_x="center", anchor_y="center", font_name="8-bit Operator+",
                                              font_size=28, batch=self.diffselect_batch)
        self.dfhs_label = pyglet.text.Label(text="HIGHSCORE: 0", x=self.render_size[0]/2,
                                            y=self.render_size[1]/2-150, anchor_x="center", anchor_y="center",
                                            font_name="8-bit Operator+", font_size=24, batch=self.diffselect_batch)
        self.diffselect = 1
        # END DIFFSELECT BATCH #

        # START PAUSED BATCH #
        self.paused_batch = pyglet.graphics.Batch()
        self.pause_cover = pyglet.sprite.Sprite(self.pausecover, self.render_size[0]/2, self.render_size[1]/2)
        self.paused_label = pyglet.text.Label(text="PAUSED", x=self.render_size[0]/2, y=self.render_size[1]/2+75,
                                              font_name="8-bit Operator+", font_size=48, batch=self.paused_batch,
                                              anchor_x="center", anchor_y="center")
        self.pausedinst_label = pyglet.text.Label(text="PRESS SPACE TO RESUME", x=self.render_size[0]/2,
                                                  y=self.render_size[1]/2, font_name="8-bit Operator+",
                                                  font_size=28, batch=self.paused_batch, anchor_x="center",
                                                  anchor_y="center")
        # END PAUSED BATCH #

        # START GAME OVER BATCH #
        self.gameover_batch = pyglet.graphics.Batch()
        self.gameover_label = pyglet.text.Label(text="GAME OVER", x=self.render_size[0]/2, y=self.render_size[1]/2+75,
                                                font_name="8-bit Operator+", font_size=48, batch=self.gameover_batch,
                                                anchor_x="center", anchor_y="center")
        self.gohs_label = pyglet.text.Label(text="HIGHSCORE: " + str(self.highscores[self.diffselect]),
                                            x=self.render_size[0]/2, y=self.render_size[1]/2,
                                            font_name="8-bit Operator+", font_size=34,
                                            batch=self.gameover_batch, anchor_x="center", anchor_y="center")
        self.gonhs_label = pyglet.text.Label(text="", x=self.render_size[0]/2, y=self.render_size[1]/2-50,
                                             anchor_x="center", anchor_y="center", batch=self.gameover_batch,
                                             font_name="8-bit Operator+", font_size=18)
        self.goinst_label = pyglet.text.Label(text="PRESS SPACE", x=self.render_size[0]/2,
                                              y=self.render_size[1]/2-100, anchor_x="center", anchor_y="center",
                                              font_name="8-bit Operator+", font_size=28)
        # END GAME OVER BATCH #

        self.state = 'start'

        self.difficulties = [6, 4, 3, 2]
        self.difficulty = self.difficulties[1]
        self.framecount = 0

        pyglet.clock.schedule_interval(self.update, 1/60.0)

    @staticmethod
    def center_image(image):
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    def reset_food(self, image, size, batch=None):
        self.food = pyglet.sprite.Sprite(img=image, x=random.randrange(1, size[0]//self.thicc)*self.thicc,
                                    y=random.randrange(1, size[1]//self.thicc)*self.thicc, batch=batch)
        while self.player.is_inside(self.food) or self.food.x % self.thicc or self.food.y % self.thicc:
            self.food = pyglet.sprite.Sprite(img=image, x=random.randrange(1, size[0] // 10) * 10,
                                        y=random.randrange(1, size[1] // 10) * 10, batch=batch)

    def set_highscore(self, score):
        try:
            self.scfile['highscore' + str(self.diffselect)] = score
        except Exception:
            print("failed to save score")

    def get_highscores(self):
        for i in range(4):
            try:
                self.highscores[i] = self.scfile['highscore' + str(i)]
            except Exception:
                self.highscores[i] = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.scfile.close()
            sys.exit()
        if symbol == key._1:
            self.window_size = 640, 480
            self.set_size(self.window_size[0], self.window_size[1])
            glScalef(.5, .5, 0)
        if symbol == key._2:
            self.window_size = 1280, 960
            self.set_size(self.window_size[0], self.window_size[1])
            glScalef(self.window_size[0] / self.render_size[0], self.window_size[1] / self.render_size[1], 0)
        # glScalef(self.window_size[0] / self.render_size[0], self.window_size[1] / self.render_size[1], 0)
        if self.state == 'start':
            if symbol == key.SPACE or symbol == key.ENTER:
                self.state = 'diffselect'
        elif self.state == 'diffselect':
            if symbol == key.UP:
                self.diffselect -= 1
            if symbol == key.DOWN:
                self.diffselect += 1
            if symbol == key.SPACE or symbol == key.ENTER:
                self.state = 'running'
                self.difficulty = self.difficulties[self.diffselect]
                self.reset_food(self.food_image, self.render_size, self.main_batch)
                self.player = player.Player(self.player_image, self.render_size[0]//2, self.render_size[1]//2,
                                            self.main_batch, self.thicc, self.render_size)
                self.framecount = 0
            if symbol == key.BACKSPACE:
                self.state = 'start'
        elif self.state == 'running':
            if symbol == key.UP or symbol == key.W:
                self.player.set_direction((0, 1))
            if symbol == key.DOWN or symbol == key.S:
                self.player.set_direction((0, -1))
            if symbol == key.LEFT or symbol == key.A:
                self.player.set_direction((-1, 0))
            if symbol == key.RIGHT or symbol == key.D:
                self.player.set_direction((1, 0))
            if symbol == key.SPACE:
                self.state = 'paused'
        elif self.state == 'paused':
            if symbol == key.SPACE:
                self.state = 'running'
                self.framecount = 0
        elif self.state == 'gameover':
            if symbol == key.SPACE:
                self.state = 'start'
                self.get_highscores()
                self.dfhs_label.text = "HIGHSCORE: " + str(self.highscores[self.diffselect])

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.grid_batch.draw()
        if self.state == 'start':
            self.wall_batch.draw()
            self.pause_cover.draw()
            self.start_batch.draw()
            if self.blink_counter < 10:
                self.startinst_label.draw()
        if self.state == 'diffselect':
            self.wall_batch.draw()
            self.pause_cover.draw()
            self.diffselect_batch.draw()
        if self.state == 'running':
            self.main_batch.draw()
            self.score_batch.draw()
            self.wall_batch.draw()
        if self.state == 'paused':
            self.main_batch.draw()
            self.score_batch.draw()
            self.wall_batch.draw()
            self.pause_cover.draw()
            self.paused_batch.draw()
        if self.state == 'gameover':
            self.main_batch.draw()
            self.score_batch.draw()
            self.wall_batch.draw()
            self.pause_cover.draw()
            self.gameover_batch.draw()
            if self.blink_counter < 10:
                self.goinst_label.draw()

    def update(self, dt):
        if self.framecount == self.difficulty:
            if self.state == 'running':
                pupdate = self.player.update(self.food)
                self.score_label.text = "SCORE: " + str(self.player.get_score())
                if pupdate == "eat":
                    self.reset_food(self.food_image, self.render_size, self.main_batch)
                elif pupdate == "gameover":
                    self.get_highscores()
                    if self.player.get_score() > self.highscores[self.diffselect]:
                        self.set_highscore(self.player.get_score())
                        self.gonhs_label.text = "NEW HIGHSCORE!"
                    else:
                        self.gonhs_label.text = ""
                    self.get_highscores()
                    self.gohs_label.text = "HIGHSCORE: " + str(self.highscores[self.diffselect])
                    self.difficulty = self.difficulties[1]
                    self.state = 'gameover'
            if self.state == 'gameover' or self.state == 'start':
                self.blink_counter += 1
                if self.blink_counter == 20:
                    self.blink_counter = 0
            if self.state == 'diffselect':
                if self.diffselect < 0:
                    self.diffselect = 3
                if self.diffselect > 3:
                    self.diffselect = 0
                if self.diffselect == 0:
                    self.easy_label.text = ">EASY<"
                    self.med_label.text = "MEDIUM"
                    self.hard_label.text = "HARD"
                    self.expert_label.text = "EXPERT"
                elif self.diffselect == 1:
                    self.easy_label.text = "EASY"
                    self.med_label.text = ">MEDIUM<"
                    self.hard_label.text = "HARD"
                    self.expert_label.text = "EXPERT"
                elif self.diffselect == 2:
                    self.easy_label.text = "EASY"
                    self.med_label.text = "MEDIUM"
                    self.hard_label.text = ">HARD<"
                    self.expert_label.text = "EXPERT"
                elif self.diffselect == 3:
                    self.easy_label.text = "EASY"
                    self.med_label.text = "MEDIUM"
                    self.hard_label.text = "HARD"
                    self.expert_label.text = ">EXPERT<"
                self.dfhs_label.text = "HIGHSCORE: " + str(self.highscores[self.diffselect])
            self.framecount = 0
        self.framecount += 1


if __name__ == '__main__':
    m = main()
    pyglet.app.run()

