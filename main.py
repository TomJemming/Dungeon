import arcade
import math
import ctypes
import random
import os


x2 = 0
y2 = 0
x4 = 0
y4 = 0

if os.name == "nt":
    user32 = ctypes.windll.user32
    SCREEN_WIDTH = user32.GetSystemMetrics(0)
    SCREEN_HEIGHT = user32.GetSystemMetrics(1)
elif os.name == "posix":
    pass
else:
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 800

def screen_resolution_int(num):
    x = int((num/768) * SCREEN_HEIGHT)
    return x

def screen_resolution_float(num):
    x = (num/768) * SCREEN_HEIGHT
    return x

class MenuView(arcade.View):

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      arcade.load_texture(file_name="images/main_screen.png"))


    def on_mouse_press(self, x, y, button, modifiers):
        game = GameView()
        self.window.show_view(game)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.fireball_timer = 0
        self.fireball_cast_timer = 0.5
        self.bolt_timer = 5
        self.shoot_cd = False
        self.player_move = False
        self.onetime_health = True
        self.player_life = 5
        self.slime_spawn_timer = 10
        self.stage_timer = 10
        self.loading_screen_timer = 0
        self.animation_timer_2 = 1
        self.animation_clock_2 = 1
        self.animation_timer_3 = 1.5
        self.animation_clock_3 = 1
        self.stage = 1
        self.loading_screen_on = 0
        self.onetime_door = True
        self.spider_spawn_timer = 3
        self.rogue_spawn_timer = 5
        self.evasion_cooldown = 0
        self.evasion_cooldown2 = 0

#scales
        self.player_scale = screen_resolution_float(0.825)
        self.slime_scale = screen_resolution_float(0.8)
        self.spider_scale = screen_resolution_float(0.1)
        self.fireball_scale = screen_resolution_float(0.13)
        self.crosshair_scale = screen_resolution_float(0.75)

#background
        self.background = arcade.load_texture(file_name="images/background.png")

#sprite lists
        self.wall_up_list = arcade.SpriteList()
        self.wall_down_list = arcade.SpriteList()
        self.wall_right_list = arcade.SpriteList()
        self.wall_left_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.crosshair_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        self.bolt_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.slime_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.spider_list = arcade.SpriteList()
        self.rogue_list = arcade.SpriteList()


#player
        self.player = arcade.AnimatedWalkingSprite(scale=self.player_scale)

        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.player_scale))

        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.player_scale,mirrored=True))

        self.player.walk_right_textures = []

        self.player.walk_right_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.player_scale))
        self.player.walk_right_textures.append(arcade.load_texture("images/Mage_2.png",scale=self.player_scale))


        self.player.walk_left_textures = []

        self.player.walk_left_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.player_scale,mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/Mage_2.png",scale=self.player_scale,mirrored=True))


        self.player.texture_change_distance = 50

        self.player.center_x = SCREEN_WIDTH//2
        self.player.center_y = SCREEN_HEIGHT//2
        self.player.scale = self.player_scale
        self.player_list.append(self.player)

#walls
        self.wall = arcade.Sprite("images/wall.png")
        self.wall.center_x = SCREEN_WIDTH//2
        self.wall.center_y = screen_resolution_int(100)
        self.wall_down_list.append(self.wall)

        self.wall = arcade.Sprite("images/wall.png")
        self.wall.center_x = SCREEN_WIDTH//2
        self.wall.center_y = SCREEN_HEIGHT-screen_resolution_int(100)
        self.wall_up_list.append(self.wall)

        self.wall = arcade.Sprite("images/wall_y.png")
        self.wall.center_x = screen_resolution_int(100)
        self.wall.center_y = SCREEN_HEIGHT//2
        self.wall_left_list.append(self.wall)

        self.wall = arcade.Sprite("images/wall_y.png")
        self.wall.center_x = SCREEN_WIDTH-screen_resolution_int(100)
        self.wall.center_y = SCREEN_HEIGHT//2
        self.wall_right_list.append(self.wall)

#crosshair
        self.crosshair = arcade.Sprite("images/crosshair.png",scale=self.crosshair_scale)
        self.crosshair.center_x = SCREEN_WIDTH//2
        self.crosshair.center_y = SCREEN_HEIGHT//2
        self.crosshair_list.append(self.crosshair)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)
        arcade.draw_text("{0:1}".format(int(self.stage_timer)), SCREEN_WIDTH/2, SCREEN_HEIGHT - screen_resolution_int(75), arcade.color.WHITE, screen_resolution_int(35), align="center", anchor_x="center",anchor_y="center")
        arcade.draw_text("Stage: " + "{0:1}".format(int(self.stage)), SCREEN_WIDTH - screen_resolution_int(150), SCREEN_HEIGHT - screen_resolution_int(75), arcade.color.WHITE, screen_resolution_int(35), align="center", anchor_x="center",anchor_y="center")
        arcade.draw_text("x " + str(self.player_life), color=arcade.color.WHITE, start_x = screen_resolution_int(120), start_y= SCREEN_HEIGHT - screen_resolution_int(75), font_size= screen_resolution_int(45))
        #arcade.draw_text(str(self.animation_clock_2), color = arcade.color.WHITE, start_x = 120, start_y = SCREEN_HEIGHT - 150)
        self.slime_list.draw()
        self.spider_list.draw()
        self.rogue_list.draw()
        self.player_list.draw()
        self.crosshair_list.draw()
        self.fireball_list.draw()
        self.bolt_list.draw()
        self.health_list.draw()
        if self.loading_screen_on == 1:
            arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture(file_name="images/loading_screen.png"))
            arcade.draw_text("Stage " + "{0:1}".format(int(self.stage)), SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.WHITE, screen_resolution_int(60), align="center", anchor_x="center",anchor_y="center")



    def on_key_press(self, symbol, modifiers:int):
        if self.shoot_cd == False:
            if symbol == arcade.key.W:
                self.player.change_y = screen_resolution_int(5)
            if symbol == arcade.key.S:
                self.player.change_y = -screen_resolution_int(5)
            if symbol == arcade.key.D:
                self.player.change_x = screen_resolution_int(5)
            if symbol == arcade.key.A:
                self.player.change_x = -screen_resolution_int(5)
        if symbol == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)


    def on_key_release(self, symbol, modifiers:int):
        if symbol == arcade.key.W:
            self.player.change_y = 0
        if symbol == arcade.key.S:
            self.player.change_y = 0
        if symbol == arcade.key.D:
            self.player.change_x = 0
        if symbol == arcade.key.A:
            self.player.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.center_y = y
        self.crosshair.center_x = x
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.fireball_timer < 0.1:
            self.shoot_cd = True


    def animation(self, sprite, name, frames: 2, scale: 1,mirrored = False):
        if frames == 2:
            if self.animation_clock_2 == 1:
                sprite.textures.clear()
                sprite.textures.append(arcade.load_texture("images/"+name+"_"+str(frames-1)+".png",scale= scale,mirrored=mirrored))
                sprite.set_texture(0)
                sprite.textures.clear()
            if self.animation_clock_2 == 2:
                sprite.textures.clear()
                sprite.textures.append(arcade.load_texture("images/"+name+"_"+str(frames)+".png",scale= scale,mirrored=mirrored))
                sprite.set_texture(0)
                sprite.textures.clear()
        if frames == 3:
            if self.animation_clock_3 == 1:
                sprite.textures.clear()
                sprite.textures.append(arcade.load_texture("images/"+name+"_"+str(frames-2)+".png",scale= scale,mirrored=mirrored))
                sprite.set_texture(0)
                sprite.textures.clear()
            if self.animation_clock_3 == 2:
                sprite.textures.clear()
                sprite.textures.append(arcade.load_texture("images/"+name+"_"+str(frames-1)+".png",scale= scale,mirrored=mirrored))
                sprite.set_texture(0)
                sprite.textures.clear()
            if self.animation_clock_3 == 3:
                sprite.textures.clear()
                sprite.textures.append(arcade.load_texture("images/"+name+"_"+str(frames)+".png",scale= scale,mirrored=mirrored))
                sprite.set_texture(0)
                sprite.textures.clear()

    def player_health(self):
        if self.onetime_health == True:
            health = arcade.Sprite(filename="images/player_health.png", scale=screen_resolution_float(0.15), center_x= screen_resolution_int(60), center_y= SCREEN_HEIGHT - screen_resolution_int(50))
            self.health_list.append(health)
            self.onetime_health = False

    def door(self):
        door = arcade.Sprite(filename="images/light.png")
        door.center_x = SCREEN_WIDTH-screen_resolution_int(100)
        door.center_y = SCREEN_HEIGHT//2
        self.door_list.append(door)
        self.background = arcade.load_texture(file_name="images/background_f.png")


    def slime_enemy(self):
        slime = arcade.Sprite(filename="images/slime_1.png", scale=self.slime_scale)

        slime.center_y = random.randrange(screen_resolution_int(200), SCREEN_HEIGHT-screen_resolution_int(200))
        slime.center_x = random.randrange(screen_resolution_int(200), SCREEN_WIDTH-screen_resolution_int(100))
        slime_coords_spawn_x = False
        slime_coords_spawn_y = False

        while slime_coords_spawn_x == False:
            if slime.center_x < self.player.center_x + screen_resolution_int(100) and slime.center_x > self.player.center_x - screen_resolution_int(100):
                slime.center_x = random.randrange(screen_resolution_int(200), SCREEN_WIDTH)
            else:
                slime_coords_spawn_x = True


        while slime_coords_spawn_y == False:
            if slime.center_y < self.player.center_y + screen_resolution_int(100) and slime.center_y > self.player.center_y - screen_resolution_int(100):
                slime.center_y = random.randrange(screen_resolution_int(100), SCREEN_HEIGHT)
            else:
                slime_coords_spawn_y = True

        self.slime_list.append(slime)


    def spider_enemy(self):

        spider = arcade.Sprite(filename="images/spider_1.png",scale=self.spider_scale) #filename

        spider.center_y = random.randrange(screen_resolution_int(200), SCREEN_HEIGHT-screen_resolution_int(200))
        spider.center_x = random.randrange(screen_resolution_int(200), SCREEN_WIDTH-screen_resolution_int(100))
        spider_coords_spawn_x = False
        spider_coords_spawn_y = False

        while spider_coords_spawn_x == False:
            if spider.center_x < self.player.center_x + screen_resolution_int(100) and spider.center_x > self.player.center_x - screen_resolution_int(100):
                spider.center_x = random.randrange(screen_resolution_int(200), SCREEN_WIDTH)
            else:
                spider_coords_spawn_x = True


        while spider_coords_spawn_y == False:
            if spider.center_y < self.player.center_y + screen_resolution_int(100) and spider.center_y > self.player.center_y - screen_resolution_int(100):
                spider.center_y = random.randrange(screen_resolution_int(200), SCREEN_HEIGHT)
            else:
                spider_coords_spawn_y = True

        self.spider_list.append(spider)

    def rogue_enemy(self):

        rogue = arcade.Sprite(filename="images/rogue_1.png",scale=0.25) #filename

        rogue.center_y = random.randrange(200, SCREEN_HEIGHT-200)
        rogue.center_x = random.randrange(200, SCREEN_WIDTH-100)
        rogue_coords_spawn_x = False
        rogue_coords_spawn_y = False

        while rogue_coords_spawn_x == False:
            if rogue.center_x < self.player.center_x + 100 and rogue.center_x > self.player.center_x - 100:
                rogue.center_x = random.randrange(200, SCREEN_WIDTH)
            else:
                rogue_coords_spawn_x = True


        while rogue_coords_spawn_y == False:
            if rogue.center_y < self.player.center_y + 100 and rogue.center_y > self.player.center_y - 100:
               rogue.center_y = random.randrange(200, SCREEN_HEIGHT)
            else:
                rogue_coords_spawn_y = True


        self.rogue_list.append(rogue)



    def trajectory(self,x,y,a,b):

        diff_a = a-x
        diff_b = b-y

        v = math.atan2(diff_a, diff_b)
        return v


    def evasion_movement(self,x,y,w,a,b):
        v = self.trajectory(x,y,a,b)
        global x1
        global y1
        for spider in self.spider_list:
            if  w < v + 12.5 and w > v - 12.5:
                if w < v:
                    x1 = 1
                    y1 = 1
                else:
                    x1 = (-1)
                    y1 = (-1)
            else:
                x1 = 0
                y1 = 0


    def fireball(self):
        fireball = arcade.Sprite(filename= "images/fireball_1.png",scale=self.fireball_scale)

        start_x = self.player.center_x
        start_y = self.player.center_y + 50
        fireball.center_x = start_x
        fireball.center_y = start_y

        dest_x = self.mouse_x
        dest_y = self.mouse_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        fireball.angle = math.degrees(angle)

        fireball.change_x = math.cos(angle) * 5
        fireball.change_y = math.sin(angle) * 5

        self.fireball_list.append(fireball)

        self.fireball_timer = 1
        self.fireball_cast_timer = 0

        for spider in self.spider_list:
            self.evasion_movement(start_x,start_y,angle,spider.center_x,spider.center_y,1)
        for rogue in self.rogue_list:
            self.evasion_movement(start_x,start_y,angle,rogue.center_x,rogue.center_y,2)

    def bolt(self,x,y):
        bolt = arcade.Sprite(filename= "images/bolt_1.png",scale=0.1)

        start_x = x
        start_y = y + 50
        bolt.center_x = start_x
        bolt.center_y = start_y

        dest_x = self.player.center_x
        dest_y = self.player.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        bolt.angle = math.degrees(angle)

        bolt.change_x = math.cos(angle) * 3
        bolt.change_y = math.sin(angle) * 3

        self.bolt_list.append(bolt)

        self.bolt_timer = 3

    def trajectory(self,x,y,a,b):

        diff_a = a-x
        diff_b = b-y

        v = math.atan2(diff_a, diff_b)
        return v


    def evasion_movement(self,x,y,w,a,b,n):
        v = self.trajectory(x,y,a,b)
        global x2
        global y2
        global x4
        global y4
        if n == 1:
            if  w < v + 15 and w > v - 15:
                if w <= v:
                    x2 = 4
                    y2 = 4
                else:
                    x2 = (-4)
                    y2 = (-4)
                self.evasion_cooldown = 0
            else:
                x2 = 0
                y2 = 0
                self.evasion_cooldown = 0
        else :
            if  w < v + 15 and w > v - 15:
                if w <= v:
                    x4 = 2
                    y4 = 2
                else:
                    x4 = (-2)
                    y4 = (-2)
                    self.evasion_cooldown2 = 0
            else:
                x4 = 0
                y4 = 0
                self.evasion_cooldown2 = 0



    def update(self, delta_time):

        self.crosshair_list.update()
        self.health_list.update()
        self.player_health()
        self.slime_list.update()
        self.spider_list.update()
        self.rogue_list.update()
        self.door_list.update()

        self.fireball_list.update()
        self.fireball_list.update_animation()

        self.bolt_list.update()
        self.bolt_list.update_animation()

        self.player_list.update()
        self.player_list.update_animation()

        self.slime_spawn_timer += delta_time
        self.spider_spawn_timer += delta_time
        self.rogue_spawn_timer += delta_time

        if self.fireball_timer > 0:
            self.fireball_timer -= delta_time

        if self.bolt_timer > 0:
            self.bolt_timer -= delta_time

        if self.stage_timer > 0:
            self.stage_timer -= delta_time

        if self.loading_screen_timer > 0:
            self.loading_screen_timer -= delta_time

#animation_clocks
        self.animation_timer_2 -= delta_time
        if self.animation_timer_2 < 0.75 and self.animation_timer_2 > 0.5:
            self.animation_clock_2 = 1
            self.animation_timer_2 = 1.5
        if self.animation_timer_2 < 1.25 and self.animation_timer_2 > 1:
            self.animation_clock_2 = 2
            self.animation_timer_2 = 1

        self.animation_timer_3 -= delta_time
        if self.animation_timer_3 < 0.75 and self.animation_timer_3 > 0.5:
            self.animation_clock_3 = 1
            self.animation_timer_3 = 1.5
        if self.animation_timer_3 < 1.25 and self.animation_timer_3 > 1:
            self.animation_clock_3 = 2
            self.animation_timer_3 = 2
        if self.animation_timer_3 < 1.75 and self.animation_timer_3 > 1.5:
            self.animation_clock_3 = 3
            self.animation_timer_3 = 1

#fireball_cast_animation
        if self.fireball_cast_timer > 0:
            self.fireball_cast_timer -= delta_time
        if self.fireball_cast_timer < 0.1 and self.player_move == False and self.shoot_cd == True:
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_3.png",scale = self.player_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_3.png",scale = self.player_scale,mirrored=True))
            self.fireball_cast_timer = 1
        if self.fireball_cast_timer < 0.87 and self.fireball_cast_timer > 0.5 and self.player_move == False and self.shoot_cd == True:
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_4.png",scale = self.player_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_4.png",scale=self.player_scale,mirrored=True))
            self.fireball_cast_timer = 1.5
        if self.fireball_cast_timer < 1.37 and self.fireball_cast_timer > 1 and self.player_move == False and self.shoot_cd == True:
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_5.png",scale = self.player_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_5.png",scale=self.player_scale,mirrored=True))
            self.fireball_cast_timer = 2
        if self.fireball_cast_timer < 1.87 and self.fireball_cast_timer > 1.5 and self.player_move == False and self.shoot_cd == True:
            self.fireball()
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_1.png",scale = self.player_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.player_scale,mirrored=True))
            self.fireball_cast_timer = 0
            self.shoot_cd = False

#animations
        for slime in self.slime_list:
            self.animation(slime, "slime",2, self.slime_scale)
        for fireball in self.fireball_list:
            self.animation(fireball, "fireball", 3, self.fireball_scale)
        for spider in self.spider_list:
            if spider.center_x > self.player.center_x:
                self.animation(spider, "spider", 3, self.spider_scale, True)
            else:
                self.animation(spider, "spider", 3, self.spider_scale, False)


#slime_movement + spawn

        if self.slime_spawn_timer > 2:
            self.slime_enemy()
            self.slime_spawn_timer = 0
        for slime in self.slime_list:
            if self.player.center_x > slime.center_x:
                slime.change_x = 1
            else:
                slime.change_x = -1
            if self.player.center_y > slime.center_y:
                slime.change_y = 1
            else:
                slime.change_y = -1


#spider movement & spawn

        if self.spider_spawn_timer > 5:
            self.spider_enemy()
            self.spider_spawn_timer = 0

        try:
            ab = abs(x2) / x2
        except ZeroDivisionError:
            ab = 0
        x1 = x2 - self.evasion_cooldown * ab
        y1 = y2 - self.evasion_cooldown * ab

        for spider in self.spider_list:
            d1 = self.player.center_x - spider.center_x
            d2 = self.player.center_y - spider.center_y
            if d1 > 0:
                spider.change_x = 2 + x1
            elif d1 == 0:
                spider.change_x = 2  + x1
            else:
                spider.change_x = -2 + x1
            if d2 > 0:
                spider.change_y = 2 + y1
            elif d2 == 0:
                spider.change_y = 2 + y1
            else:
                spider.change_y = -2 + y1

        if x2 == 0:
            self.evasion_cooldown = 0
        else:
            self.evasion_cooldown += 2 * delta_time
            if self.evasion_cooldown >= 4:
                self.evasion_cooldown = 4


        if self.rogue_spawn_timer > 8:
            self.rogue_enemy()
            self.rogue_spawn_timer = 0
        try:
            ab = abs(x4) / x4
        except ZeroDivisionError:
            ab = 0
        x3 = x4 - self.evasion_cooldown2 * ab
        y3 = y4 - self.evasion_cooldown2 * ab

        for rogue in self.rogue_list:
            if self.bolt_timer <= 0:
                self.bolt(rogue.center_x,rogue.center_y)
            d1 = self.player.center_x - rogue.center_x
            d2 = self.player.center_y - rogue.center_y
            d3 = (d1**2 + d2**2)**(1/2)
            f = 0

            if d3 > 400:
                f = 0
            if d3 > 350 and f == 0:
                if d1 > 0:
                    rogue.change_x = 1 + x3
                elif d1 == 0:
                    rogue.change_x = 1 + x3
                else:
                    rogue.change_x = -1 + x3
                if d2 > 0:
                    rogue.change_y = 1 + y3
                elif d2 == 0:
                    rogue.change_y = 1 + y3
                else:
                    rogue.change_y = -1 + y3
            else:
                f = 1
                xc = self.player.center_x
                yc = self.player.center_y
                xr = rogue.center_x
                yr = rogue.center_y
                ac = math.atan2(yc-yr, xc-xr)

                rogue.change_x = math.sin(ac) * (-2)  * (1+ x3)
                rogue.change_y = math.cos(ac) * 2 * (1 + y3)



        if x4 == 0:
            self.evasion_cooldown2 = 0
        else:
            self.evasion_cooldown2 += 2 * delta_time
            if self.evasion_cooldown2 >= 2:
                self.evasion_cooldown2 = 2




#door
        if self.stage_timer < 0.01:
            if self.onetime_door == True:
                self.door()
                self.onetime_door = False
        door_hit_with_player = arcade.check_for_collision_with_list(self.player, self.door_list)
        for door in door_hit_with_player:
            self.stage += 1
            self.player.center_x = screen_resolution_int(200)
            self.player.center_y = SCREEN_HEIGHT//2
            door.kill()
            self.stage_timer = 13
            self.onetime_door = True
            self.slime_list = arcade.SpriteList()
            self.fireball_list = arcade.SpriteList()
            self.spider_list = arcade.SpriteList()
            self.loading_screen_on = 1
            self.loading_screen_timer = 3

        if self.loading_screen_timer > 2.8 and self.loading_screen_timer < 2.9:
            arcade.pause(2)
            self.loading_screen_on = 0
            self.background = arcade.load_texture(file_name="images/background.png")
            self.animation_timer_2 = 4
            self.animation_timer_3 = 4


#game_over
        if self.player_life < 1:
            arcade.close_window()
            print("Noob, you lost.")


#slime hitbox
        slime_hit_with_player = arcade.check_for_collision_with_list(self.player, self.slime_list)
        for slime in slime_hit_with_player:
            self.player_life -= 1
            slime.kill()

        for slime in self.slime_list:
            slime_hit_with_projectile = arcade.check_for_collision_with_list(slime, self.fireball_list)
            for slime_hit in slime_hit_with_projectile:
                slime.kill()

        for slime in self.slime_list:
            if slime.bottom > SCREEN_HEIGHT - screen_resolution_int(150) or slime.top < screen_resolution_int(150) or slime.right < screen_resolution_int(150) or slime.left > SCREEN_WIDTH - screen_resolution_int(150):
                slime.kill()


#spider hitbox
        spider_hit_with_player = arcade.check_for_collision_with_list(self.player, self.spider_list)
        for spider in spider_hit_with_player:
            self.player_life -= 1
            spider.kill()

        for spider in self.spider_list:
            spider_hit_with_projectile = arcade.check_for_collision_with_list(spider, self.fireball_list)
            for spider_hit in spider_hit_with_projectile:
                spider.kill()

        for spider in self.spider_list:
            if spider.bottom > SCREEN_HEIGHT - screen_resolution_int(150) or spider.top < screen_resolution_int(150) or spider.right < screen_resolution_int(150) or spider.left > SCREEN_WIDTH - screen_resolution_int(150):
                spider.kill()

#rogue hitbox

        rogue_hit_with_player = arcade.check_for_collision_with_list(self.player, self.rogue_list)
        for rogue in rogue_hit_with_player:
            self.player_life -= 1
            rogue.kill()

        for rogue in self.rogue_list:
            rogue_hit_with_projectile = arcade.check_for_collision_with_list(rogue, self.fireball_list)
            for rogue_hit in rogue_hit_with_projectile:
                rogue.kill()

        for rogue in self.rogue_list:
            if rogue.bottom > SCREEN_HEIGHT - 150 or rogue.top < 150 or rogue.right < 150 or rogue.left > SCREEN_WIDTH - 150:
                rogue.kill()

#wall_hitbox
        wall_down_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_down_list)
        for wall in wall_down_hit_list:
            self.player.center_y += screen_resolution_int(5)

        wall_up_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_up_list)
        for wall in wall_up_hit_list:
            self.player.center_y -= screen_resolution_int(5)

        wall_left_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_left_list)
        for wall in wall_left_hit_list:
            self.player.center_x += screen_resolution_int(5)

        wall_right_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_right_list)
        for wall in wall_right_hit_list:
            self.player.center_x -= screen_resolution_int(5)


#fireball_hitbox
        for fireball in self.fireball_list:
            if fireball.bottom > SCREEN_HEIGHT - screen_resolution_int(150) or fireball.top < screen_resolution_int(150) or fireball.right < screen_resolution_int(150) or fireball.left > SCREEN_WIDTH - screen_resolution_int(150):
                fireball.kill()

        for bolt in self.bolt_list:
            if bolt.bottom > SCREEN_HEIGHT - 200 or bolt.top < 200 or bolt.right < 200 or bolt.left > SCREEN_WIDTH - 200:
                bolt.kill()

#bolt_hitbox
        bolt_hit_with_player = arcade.check_for_collision_with_list(self.player, self.bolt_list)
        for bolt in bolt_hit_with_player:
            self.player_life -= 1
            bolt.kill()

        for bolt in self.bolt_list:
            bolt_hit_with_projectile = arcade.check_for_collision_with_list(bolt, self.fireball_list)
            for bolt_hit in bolt_hit_with_projectile:
                bolt.kill()

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view


    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      arcade.load_texture(file_name="images/pause_screen.png"))


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif symbol == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)


def main():
    if os.name == "posix":
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Instruction and Game Over Views Example", fullscreen=True, antialiasing=False)
    else:
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Instruction and Game Over Views Example",fullscreen=True)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
