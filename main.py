import random

import arcade

# game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Game"
# player
GRAVITY = 1.2
PLAYER_JUMP_SPEED = 20
PLAYER_JUMP_POWER = 20
PLAYER_MOVEMENT_SPEED = 7
# obstacles
BOULDER_MOVEMENT_SPEED = 12


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game1 = False
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.physics_engine_2 = None
        self.physics_engine_3 = None
        self.camera = None
        self.wall = None
        self.lava = None
        self.lava_wall = None
        self.score = 0
        self.gui_camera = None
        self.timer_start = 0
        self.start_lava_gen = 0
        self.end_lava_gen = 0
        self.start_power_gen = 0
        self.end_power_gen = 0
        self.score1 = 0
        self.boulder_timer = 0
        self.boulder = None
        self.boulder_target = 0
        self.boulder_slope = 0
        self.player_sprite_can_jump = 0
        self.power_up_active = False
        self.power_up = None
        self.power_up_timer = 0
        self.power_up_warning = False
        arcade.set_background_color(arcade.csscolor.WHITE)

    def game(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("player")
        self.scene.add_sprite_list("walls", use_spatial_hash=True)
        self.scene.add_sprite_list("lava", use_spatial_hash=True)
        self.scene.add_sprite_list("boulder")
        self.scene.add_sprite_list("lava_wall")
        self.scene.add_sprite_list("power_up", use_spatial_hash=True)
        self.start_lava_gen = 1400
        self.end_lava_gen = 1700
        for lava in range(0, 100):
            self.lava = arcade.Sprite(r":resources:images/tiles/lava.png", (random.randrange(8, 12, 1) / 10))
            self.start_lava_gen = self.start_lava_gen + 600
            self.end_lava_gen = self.end_lava_gen + 600
            if self.lava.scale == 0.8:
                self.lava.center_y = 45
            elif self.lava.scale == 0.9:
                self.lava.center_y = 39
            elif self.lava.scale == 1:
                self.lava.center_y = 33
            elif self.lava.scale == 1.1:
                self.lava.center_y = 28
            self.lava.center_x = random.randrange(self.start_lava_gen, self.end_lava_gen)
            self.scene.add_sprite("lava", self.lava)
        self.start_power_gen = 1400
        self.end_power_gen = 2150
        for power in range(0, 40):
            self.power_up = arcade.Sprite(":resources:images/items/gemBlue.png")
            self.power_up.center_y = 128
            self.start_power_gen = self.start_power_gen + 1500
            self.end_power_gen = self.end_power_gen + 1500
            power_up_center_x = random.randrange(self.start_power_gen, self.end_power_gen)
            self.power_up.center_x = power_up_center_x
            self.scene.add_sprite("power_up", self.power_up)
        self.timer_start = 0
        self.player_sprite = arcade.Sprite(
            r":resources:images/animated_characters/male_person/malePerson_idle.png")
        self.player_sprite.center_x = 1200
        self.player_sprite.center_y = 128
        self.scene.add_sprite("player", self.player_sprite)
        self.boulder = arcade.Sprite(":resources:images/tiles/rock.png", 3)
        for x in range(0, 60000, 120):
            self.wall = arcade.Sprite(":resources:images/tiles/stoneMid.png")
            self.wall.center_x = x
            self.wall.center_y = 32
            self.scene.add_sprite("walls", self.wall)
        for y in range(0, 300, 100):
            self.lava_wall = arcade.Sprite(r":resources:images/tiles/lava.png", 9)
            self.lava_wall.center_y = y
            self.scene.add_sprite("lava_wall", self.lava_wall)
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.player_sprite_can_jump = 0
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY,
                                                             walls=self.scene["walls"])
        self.physics_engine_2 = arcade.PhysicsEnginePlatformer(self.lava_wall, gravity_constant=0)
        self.physics_engine_3 = arcade.PhysicsEnginePlatformer(self.boulder, gravity_constant=0)

    def on_draw(self):
        if self.game1:
            self.clear()
            self.scene.draw()
            self.gui_camera.use()
            score_text = f"Score: {self.score}"
            arcade.draw_text(score_text, 840, 600, arcade.csscolor.WHITE, 18)
            if self.timer_start <= 90:
                arcade.draw_text("Use WASD or arrow keys to move", 200, 400, arcade.csscolor.WHITE, 30)
            if 90 < self.timer_start < 220:
                arcade.draw_text("Try to escape to the right to escape the wall of lava", 70, 400, arcade.csscolor.WHITE,
                                 28)
            if self.power_up_warning:
                arcade.draw_text("Power up ending", 250, 400, arcade.csscolor.WHITE, 30)
            self.camera.use()
        if not self.game1:
            arcade.start_render()
            self.gui_camera.use()
            if self.score1 > 0:
                arcade.draw_text("Your score was", 310, 530, arcade.csscolor.BLACK, 40)
            if 100 > self.score1 > 0:
                arcade.draw_text(self.score1, 480, 440, arcade.csscolor.BLACK, 40)
            if 100 < self.score1:
                arcade.draw_text(self.score1, 465, 440, arcade.csscolor.BLACK, 40)
            arcade.draw_text("Press enter to play", 280, 350, arcade.csscolor.BLACK, 40)

    def on_key_press(self, key, modifiers):
        if self.game1:
            if key == arcade.key.W or key == arcade.key.SPACE or key == arcade.key.UP:
                if self.player_sprite_can_jump >= 1:
                    self.player_sprite.change_y = PLAYER_JUMP_POWER
                    self.player_sprite_can_jump = self.player_sprite_can_jump - 1
            elif key == arcade.key.D or key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.A or key == arcade.key.LEFT:
                if self.player_sprite.center_x > 1200:
                    self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if not self.game1:
            if key == arcade.key.ENTER:
                self.game()
                self.game1 = True

    def on_key_release(self, key, modifiers):
        if self.game1:
            if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.SPACE or key == arcade.key.S:
                self.player_sprite.change_y = 0
            elif key == arcade.key.D or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.LEFT:
                self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        if self.game1:
            screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
            screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
            if screen_center_x < 0:
                screen_center_x = 0
            if screen_center_y < 0:
                screen_center_y = 0
            player_centered = screen_center_x, screen_center_y
            self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        if self.game1:
            self.physics_engine.update()
            if self.timer_start >= 60:
                self.physics_engine_2.update()
            self.physics_engine_3.update()
            self.center_camera_to_player()
            if self.player_sprite.change_y == 0 and self.power_up_active:
                if self.player_sprite_can_jump < 2:
                    self.player_sprite_can_jump = self.player_sprite_can_jump + 1
            if self.player_sprite.change_y == 0 and not self.power_up_active:
                if self.player_sprite_can_jump < 1:
                    self.player_sprite_can_jump = self.player_sprite_can_jump + 1
            if self.player_sprite.center_x - self.lava_wall.center_x > 1200:
                if self.timer_start > 60:
                    self.lava_wall.center_x = self.lava_wall.center_x + 100
            self.lava_wall.change_x = random.randrange(60, 70) / 10
            if self.power_up_active:
                self.power_up_timer = self.power_up_timer + 1
            if self.power_up_timer > 300:
                self.power_up_timer = 0
                self.power_up_active = False
                self.power_up_warning = False
            if self.power_up_timer > 240:
                self.power_up_warning = True
            power_up_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["power_up"])
            for power_up in power_up_hit_list:
                self.power_up_active = True
                self.power_up_timer = 0
                self.power_up_warning = False
                power_up.kill()
            lava_wall_power_hit_list = arcade.check_for_collision_with_list(self.lava_wall, self.scene["power_up"])
            for power_up in lava_wall_power_hit_list:
                power_up.kill()
            boulder_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["boulder"])
            for self.player_sprite in boulder_hit_list:
                self.game1 = False
                self.score1 = self.score
                self.power_up_active = False
                self.power_up_warning = False
            lava_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["lava"])
            for self.player in lava_hit_list:
                self.game1 = False
                self.score1 = self.score
                self.power_up_active = False
                self.power_up_warning = False
            if self.player_sprite.center_x <= self.lava_wall.center_x + 600:
                self.game1 = False
                self.score1 = self.score
                self.power_up_active = False
                self.power_up_warning = False
            self.score = round((self.player_sprite.center_x - 1200) / 30)
            if self.boulder_timer > 320 and self.timer_start > 150:
                self.boulder = arcade.Sprite(":resources:images/tiles/rock.png")
                self.boulder_timer = 0
                self.scene.add_sprite("boulder", self.boulder)
                self.boulder.center_x = self.lava_wall.center_x + 400
                self.boulder_target = self.player_sprite.center_x + 0.8*BOULDER_MOVEMENT_SPEED/PLAYER_MOVEMENT_SPEED*(
                        self.player_sprite.center_x - self.lava_wall.center_x - 400)
                boulder_change_in_x = self.boulder_target - self.lava_wall.center_x - 400
                self.boulder_slope = -410/boulder_change_in_x
                self.boulder.center_y = 700
                self.physics_engine_3 = arcade.PhysicsEnginePlatformer(self.boulder, gravity_constant=0)
            if self.timer_start > 150:
                self.boulder.change_y = BOULDER_MOVEMENT_SPEED*self.boulder_slope
                self.boulder.change_x = BOULDER_MOVEMENT_SPEED
            if self.score < 0:
                self.score = 0
            if self.boulder.collides_with_list(self.scene["walls"]):
                self.boulder.kill()
            self.timer_start = self.timer_start + 1
            self.boulder_timer = self.boulder_timer + 1
            arcade.set_background_color(arcade.csscolor.DARK_RED)
        if not self.game1:
            arcade.set_background_color(arcade.csscolor.WHITE)


def main():
    window = MyGame()
    window.game()
    arcade.run()


if __name__ == "__main__":
    main()
