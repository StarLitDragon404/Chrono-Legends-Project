import pygame as pg
from pytmx.util_pygame import load_pygame
from spritesheet_code import load_frame_from_spritesheet_with_tile_size, load_frame_from_spritesheet_with_tileset_size
import counter
import os


WIDTH = 1280
HEIGHT = 800
TILE_SIZE = 80
FPS = 240


pg.init()
pg.mixer.init()


screen = pg.display.set_mode((WIDTH, HEIGHT))
tmx_data = load_pygame("assets/maps/Icarus_Room.tmx")
tile_layer = tmx_data.get_layer_by_name('Ground')
object_layer = tmx_data.get_layer_by_name('Objects')
exits_layer = tmx_data.get_layer_by_name('Exits')
entrances_layer = tmx_data.get_layer_by_name('Entrances')
player_spritesheet = pg.image.load("assets/characters/icarus/Icarus.png").convert_alpha()
collision_layer = tmx_data.get_layer_by_name('Collision')
spawn_layer = tmx_data.get_layer_by_name('Spawn')
interaction_layer = tmx_data.get_layer_by_name('Interact')
room_borders = pg.Rect(0, 0, tmx_data.width * TILE_SIZE, tmx_data.height * TILE_SIZE)
black_overlay = 0
room_transition = False
room_trans_ph2 = False
trans_dest = None
trans_entr = None
bg_color = (0, 0, 0)






def change_room(room, entrance):
    global room_transition, trans_dest, trans_entr, room_trans_ph2, waiting_in_emily_room
    trans_entr = entrance
    trans_dest = room
    room_transition = True
    room_trans_ph2 = False
    if trans_dest == 'Emily_room.tmx':
        waiting_in_emily_room = 0
    
        





def door_show():
    for object in camera_group.sprites():
        if hasattr(object, 'door_vis'):
            object.door_vis = True
def door_hide():
    for object in camera_group.sprites():
        if hasattr(object, 'door_vis'):
            object.door_vis = False


class Tile(pg.sprite.Sprite):
    def __init__(self, tile):
        super().__init__()
        self.image = pg.transform.scale(tile[2], (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = tile[0] * TILE_SIZE
        self.rect.y = tile[1] * TILE_SIZE
        self.ysort = False
        self.visible = True

class Object(pg.sprite.Sprite):
    def __init__(self, object):
        super().__init__()
        self.image = pg.transform.scale_by(pg.transform.scale(object.image.convert_alpha(), (object.width, object.height)), (TILE_SIZE/32, TILE_SIZE/32))
        self.rect = self.image.get_rect()
        self.rect.x = object.x * (TILE_SIZE/32)
        self.rect.y = object.y * (TILE_SIZE/32)
        self.ysort = object.ysort
        self.visible = object.visible
        self.show_last = False
        if hasattr(object, 'show_last'):
            self.show_last = object.show_last
        
        if hasattr(object, 'door_vis'):
            self.door_vis = object.door_vis
        if hasattr(object, 'interact_dialogue'):
            self.interact_dialogue = object.interact_dialogue
    def update(self):
        pass

class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.camera_rect = pg.Rect(0, 0, WIDTH, HEIGHT)
        self.auto_center = True
        self.target_dest = None
        self.duration = None
        self.path = None
        self.path_progress = 0

    def center_target_camera(self, target):
        self.camera_rect.center = target.rect.center

    def box_target_camera(self, target):

        self.center_target_camera(target)
        
        self.fix_gaps()
    
    def lock_on(self, target, duration):
        self.auto_center = False
        self.target_dest = target.rect.center
        self.duration = duration
        counter_manager.add(counter.Counter(FPS*duration, self.post_glide))
        self.path_progress = 0
        self.path = []
        for i in range(FPS*duration):
            self.path.append((self.camera_rect.centerx+((target.rect.centerx-self.camera_rect.centerx)/(FPS*duration))*(i+1), self.camera_rect.centery+((target.rect.centery-self.camera_rect.centery)/(FPS*duration))*(i+1)))
        

    def post_glide(self):
        self.camera_rect.center = self.target_dest
        self.target_dest = None
        self.duration = None
        self.fix_gaps()


    def fix_gaps(self):
        if self.camera_rect.left < room_borders.left:
            self.camera_rect.left = room_borders.left
        if self.camera_rect.right > room_borders.right:
            self.camera_rect.right = room_borders.right
        if self.camera_rect.top < room_borders.top:
            self.camera_rect.top = room_borders.top
        if self.camera_rect.bottom > room_borders.bottom:
            self.camera_rect.bottom = room_borders.bottom

    def scroll_rect(self, rect):
        return rect.move(-self.camera_rect.left, -self.camera_rect.top)

    def get_npc(self, name):
        for sprite in self.sprites():
            if isinstance(sprite, NPC):
                if sprite.name == name:
                    return sprite
                
    def draw(self, screen):
        
        if self.auto_center:
            self.box_target_camera(player)
        else:
            if self.target_dest is not None:
                self.camera_rect.center = self.path[self.path_progress]
                self.path_progress += 1
                self.fix_gaps()
                if self.path_progress == len(self.path):
                    self.post_glide()
        for sprite in self.sprites():
            if (not sprite.ysort):
                screen.blit(sprite.image, sprite.rect.move(-self.camera_rect.left, -self.camera_rect.top))
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            if sprite.ysort:
                if hasattr(sprite, 'show_last'):
                    if not sprite.show_last:
                        rect = sprite.rect.move(-self.camera_rect.left, -self.camera_rect.top)
                    
                        if hasattr(sprite, 'door_vis'):
                            if sprite.door_vis:
                                
                                screen.blit(sprite.image, rect)
                        else:
                            screen.blit(sprite.image, rect)
                else:
                    rect = sprite.rect.move(-self.camera_rect.left, -self.camera_rect.top)
                    
                    if hasattr(sprite, 'door_vis'):
                        if sprite.door_vis:
                            
                            screen.blit(sprite.image, rect)
                    else:
                        screen.blit(sprite.image, rect)
        for sprite in self.sprites():
        
            if hasattr(sprite, 'show_last'):
                if sprite.show_last:
                    rect = sprite.rect.move(-self.camera_rect.left, -self.camera_rect.top)
                
                    if hasattr(sprite, 'door_vis'):
                        if sprite.door_vis:
                            
                            screen.blit(sprite.image, rect)
                    else:
                        screen.blit(sprite.image, rect)

alona_walk_outside_flag = False

def alona_walk_outside():
    global alona_walk_outside_flag
    if alona_walk_outside_flag:
<<<<<<< HEAD
        camera_group.get_npc('Alona').move_path([(800, 0, 3)])
=======
        camera_group.get_npc('Alona').move_path([(800, 0, 2)])
>>>>>>> d95fd2d (Added lots of changes (addes outdoors adding backdrop), also added trigger box functionallity)
        alona_walk_outside_flag = False



class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale_by(load_frame_from_spritesheet_with_tileset_size(player_spritesheet.copy(), 2, 2, 1, 1), 4)
        self.rect = self.image.get_rect()
        for s in spawn_layer:
            self.rect.center = s.x * (TILE_SIZE/32), s.y * (TILE_SIZE/32)
        self.speed = 1
        self.hitbox = self.rect.copy()
        self.hitbox.height /= 3
        self.hitbox.bottom = self.rect.bottom
        self.ysort = True
        self.locked = True
        self.vx = 0
        self.vy = 0
        self.visible = True
        self.direction = None
    def move(self,vx, vy):
        self.vx = vx
        self.vy = vy
    def change_frame(self, row, col):
        self.image = pg.transform.scale_by(load_frame_from_spritesheet_with_tileset_size(player_spritesheet.copy(), 2, 2, row, col), 4)
        self.rect = self.image.get_rect(center=self.rect.center)
    def update(self):
        
        self.hitbox = self.rect.copy()
        self.hitbox.height /= 3
        self.hitbox.bottom = self.rect.bottom
        keys = pg.key.get_pressed()
        self.rect.move_ip(self.vx, self.vy)
        if not room_transition and not self.locked:
            vx = 0
            vy = 0
            if keys[pg.K_LEFT]:
                vx -= self.speed
                self.direction = 'left'
            if keys[pg.K_RIGHT]:
                vx += self.speed
                self.direction = 'right'
            
            self.rect.move_ip(vx, 0)
            self.hitbox = self.rect.copy()
            self.hitbox.height /= 3
            self.hitbox.bottom = self.rect.bottom
            for collider in collision_layer:
                rect = pg.Rect(collider.x * (TILE_SIZE/32), collider.y * (TILE_SIZE/32), collider.width * (TILE_SIZE/32), collider.height * (TILE_SIZE/32))
                if camera_group.scroll_rect(self.hitbox).colliderect(camera_group.scroll_rect(rect)):
                    if not hasattr(collider, 'trigger_func'):
                        if vx > 0:
                            self.rect.right = rect.left
                        if vx < 0:
                            self.rect.left = rect.right
                    else:
                        exec(f'{collider.trigger_func}()')

            
            if keys[pg.K_UP]:
                vy -= self.speed
                self.direction = 'up'
            if keys[pg.K_DOWN]:
                vy += self.speed
                self.direction = 'down'
            self.rect.move_ip(0, vy)
            self.hitbox = self.rect.copy()
            self.hitbox.height /= 3
            self.hitbox.bottom = self.rect.bottom

            for collider in collision_layer:
                rect = pg.Rect(collider.x * (TILE_SIZE/32), collider.y * (TILE_SIZE/32), collider.width * (TILE_SIZE/32), collider.height * (TILE_SIZE/32))
                if camera_group.scroll_rect(self.hitbox).colliderect(camera_group.scroll_rect(rect)):
                    if not hasattr(collider, 'trigger_func'):
                        if vy > 0:
                            self.rect.bottom = rect.top
                        if vy < 0:
                            self.hitbox.top = rect.bottom
                            self.rect.bottom = self.hitbox.bottom
                    else:
                        exec(f'{collider.trigger_func}()')

                
            for exit in exits_layer:
                rect = pg.Rect(exit.x * (TILE_SIZE/32), exit.y * (TILE_SIZE/32), exit.width * (TILE_SIZE/32), exit.height * (TILE_SIZE/32))
                if self.rect.colliderect(rect):
                    dest_room = exit.dest_room
                    dest_entrance = exit.dest_entrance
                    change_room(dest_room, dest_entrance)

class NPC(pg.sprite.Sprite):
    def __init__(self, name, spawn):
        super().__init__()
        if name == 'Jessica':
            self.image = pg.transform.scale_by(pg.image.load('assets/characters/jessica/jessica.png'), 4)
        if name == 'Alona':
            self.image = pg.transform.scale_by(load_frame_from_spritesheet_with_tileset_size(pg.image.load('assets/characters/alona/alona.png'), 2, 2, 0, 0), 4)
        if name == 'Emily':
            self.image = pg.transform.scale_by(load_frame_from_spritesheet_with_tileset_size(pg.image.load('assets/characters/emily/emily.png'), 3, 3, 0, 0), 4)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.centerx = spawn[0] * (TILE_SIZE/32)
        self.rect.centery = spawn[1] * (TILE_SIZE/32)
        self.ysort = True
        self.visible = True
        self.vx = 0
        self.vy = 0
        self.timer = 0
        self.move = False
        self.dur = 0
        self.path = None
        self.path_segment = 0
        self.ysort = True
        self.show_last = False
    def move_by(self, x, y, duration):
        self.vx = x/(FPS*duration)
        self.vy = y/(FPS*duration)
        self.timer = 0
        self.move = True
        self.dur = duration * FPS
    def move_path(self, path):
        self.path = path
        self.path_segment = 0
        self.timer = 0
    def update(self):
        if self.move:
            self.rect.x += self.vx
            self.rect.y += self.vy
            
            self.timer += 1
            if self.timer >= self.dur:
                self.vx = 0
                self.vy = 0
                self.move = False
        if self.path is not None:
            self.rect.x += self.path[self.path_segment][0]/(FPS*self.path[self.path_segment][2])
            self.rect.y += self.path[self.path_segment][1]/(FPS*self.path[self.path_segment][2])
            self.timer += 1
            if self.timer >= self.path[self.path_segment][2] * FPS:
                self.timer = 0
                self.path_segment += 1
                if self.path_segment == len(self.path):
                    self.path = None





clock = pg.time.Clock()

camera_group = CameraGroup()

for tile in tile_layer.tiles():
    camera_group.add(Tile(tile))
for object in object_layer:
    camera_group.add(Object(object))
player = Player()
camera_group.add(player)


counter_manager = counter.CounterManager()



def icarus_lovescene_end():
    camera_group.auto_center = True
    effects.empty()

    def alona_sit():
        camera_group.get_npc("Alona").rect.x -= 20
        camera_group.get_npc("Alona").rect.y -= 45
        camera_group.get_npc("Alona").image = pg.transform.scale_by(load_frame_from_spritesheet_with_tileset_size(pg.image.load('assets/characters/alona/alona.png'), 2, 2, 1, 1), 4)
        # camera_group.get_npc('Alona').show_last = True
        player.locked = False

    def alona_walk_to_chair():
        camera_group.get_npc('Alona').move_path([
            (-250, 0, 0.5),
            (0, 25, 0.2),
            (-400, 0, 1),
            (0, -150, 0.5),
            (90, 0, 0.5),
        ])
        counter_manager.add(counter.Counter(FPS*(2.7), alona_sit))

    def remind_breakfast():
        dialogues.add(Dialogue('Well, anyways\nyour mom made breakfast, so lets eat!', 0.08, os.path.join("assets", 'sounds', 'alona_voice.wav'), os.path.join('assets', 'characters', 'alona', 'avatar.png'), alona_walk_to_chair))

    dialogues.add(Dialogue('Umm...\nIcarus?', 0.08, os.path.join("assets", 'sounds', 'alona_voice.wav'), os.path.join('assets', 'characters', 'alona', 'avatar.png'), remind_breakfast))
    pg.mixer.music.pause()

class TextCharacter(pg.sprite.Sprite):
    def __init__(self, text, size, pos, color):
        super().__init__()
        self.text = text
        self.color = color
        self.size = size
        self.font = pg.font.Font(os.path.join('assets', 'fonts', 'MatchupPro.ttf'), self.size)
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        
class Heart(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('assets/images/heart.png'), (HEIGHT-100, HEIGHT-100))
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.opacity = 0
        self.image.set_alpha(self.opacity)
        self.reached_end = False
        
    def update(self):
        self.image.set_alpha(self.opacity)
        self.opacity += 1
        if self.opacity > 255 and not self.reached_end:
            self.opacity = 255 
            self.reached_end = True
            counter_manager.add(counter.Counter(FPS*2, icarus_lovescene_end))
            


class Dialogue(pg.sprite.Sprite):
    def __init__(self, text, delay, voice, avatar, callback=None):
        super().__init__()
        self.text = text
        self.delay = delay
        self.pos = 0
        if avatar:
            self.avatar = pg.transform.scale(pg.image.load(avatar), (100, 100))
        else:
            self.avatar = None

        self.image = pg.Surface((1000, 200), pg.SRCALPHA)
        pg.draw.rect(self.image, (50, 50, 50), self.image.get_rect(), border_radius=13)
        pg.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), 6, border_radius=13)
        self.rect = self.image.get_rect(centerx=WIDTH/2, top = 50)
        self.text_group = pg.sprite.Group()
        self.tick = 0
        self.cursor_x = 200
        self.size = 38
        self.cursor_y = 50
        self.voice = voice
        self.callback = callback
        self.control_lock_state = player.locked
        player.locked = True
        if self.avatar:
            self.image.blit(self.avatar, self.avatar.get_rect(center=(100, 100)))
        
    def update(self):
        if self.tick >= self.delay * FPS:
            if self.text[self.pos] != '\n':
                self.text_group.add(TextCharacter(self.text[self.pos], self.size, (self.cursor_x, self.cursor_y), (255, 255, 255)))

            self.pos += 1
            if self.pos == len(self.text):
                self.pos = len(self.text) - 1
                keys = pg.key.get_pressed()
                if keys[pg.K_KP_ENTER] or keys[pg.K_RETURN]:
                    self.kill()
                    if self.callback is not None:
                        self.callback()
                    player.locked = self.control_lock_state
            else:
                keys = pg.key.get_pressed()

                        


                if self.text[self.pos - 1] == ' ':
                    self.cursor_x += self.size * 0.6
                elif self.text[self.pos - 1] == '\n':
                    self.cursor_x = 200
                    self.cursor_y += self.size
                else:
                    self.cursor_x += self.size * 0.5
                    pg.mixer.Sound(self.voice).play(1)
                
                if keys[pg.K_x] or keys[pg.K_x]:
                    for i in range(len(self.text)-self.pos-1):
                        if self.text[self.pos] != '\n':
                            self.text_group.add(TextCharacter(self.text[self.pos], self.size, (self.cursor_x, self.cursor_y), (255, 255, 255)))
                        self.pos += 1
                        if self.text[self.pos - 1] == ' ':
                            self.cursor_x += self.size * 0.6
                        elif self.text[self.pos - 1] == '\n':
                            self.cursor_x = 200
                            self.cursor_y += self.size
                        else:
                            self.cursor_x += self.size * 0.5
            
            self.image = pg.Surface((1000, 200), pg.SRCALPHA)
            pg.draw.rect(self.image, (50, 50, 50), self.image.get_rect(), border_radius=13)
            pg.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), 6, border_radius=13)
            if self.avatar:
                self.image.blit(self.avatar, self.avatar.get_rect(center=(100, 100)))
            self.text_group.draw(self.image)
            self.tick = 0
        
        else:
            self.tick += 1
       


dialogues = pg.sprite.Group()
effects = pg.sprite.Group()


def draw():

    camera_group.draw(screen)
    camera_group.update()
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(black_overlay)
    screen.blit(surf, (0, 0))
    
    dialogues.draw(screen)
    dialogues.update()
    effects.draw(screen)
    effects.update()

def post_transition():
    global tile_layer, tmx_data, object_layer, exits_layer, entrances_layer, room_borders, collision_layer, spawn_layer, interaction_layer
    camera_group.empty()
    tmx_data = load_pygame(f"assets/maps/{trans_dest}")
    tile_layer = tmx_data.get_layer_by_name('Ground')
    object_layer = tmx_data.get_layer_by_name('Objects')
    exits_layer = tmx_data.get_layer_by_name('Exits')
    entrances_layer = tmx_data.get_layer_by_name('Entrances')
    collision_layer = tmx_data.get_layer_by_name('Collision')
    spawn_layer = tmx_data.get_layer_by_name('Spawn')
    interaction_layer = tmx_data.get_layer_by_name('Interact')
    for entrance1 in entrances_layer:
        if entrance1.name == trans_entr:
            player.rect.centerx = (entrance1.x + (entrance1.width / 2)) * (TILE_SIZE/32)
            player.rect.centery = (entrance1.y + (entrance1.height / 2)) * (TILE_SIZE/32)
    for tile in tile_layer.tiles():
        camera_group.add(Tile(tile))
    for object in object_layer:
        camera_group.add(Object(object))
    camera_group.add(player)
    room_borders = pg.Rect(0, 0, tmx_data.width * TILE_SIZE, tmx_data.height * TILE_SIZE)
    if 'Characters' in tmx_data.layernames:
        chars = tmx_data.get_layer_by_name('Characters')
        for spawn in chars:
            camera_group.add(NPC(spawn.name, (spawn.x, spawn.y)))
    if tmx_data.filename == 'assets/maps/House_lower.tmx':
        player.locked = True
        def alona_greet():
            dialogues.add(Dialogue('Oh, hello Icarus!', 0.08, os.path.join('assets/sounds/alona_voice.wav'), 'assets/characters/alona/avatar.png', icarus_inlove))

        def alona_walkin():
            camera_group.get_npc('Alona').move_by(-150, 0, 1)
            counter_manager.add(counter.Counter(FPS*1.5, alona_greet))

        def heart_show():
            effects.add(Heart())
            pg.mixer.music.load(os.path.join('assets', 'sounds', 'love_bird.wav'))
            pg.mixer.music.play()

        def icarus_inlove():
            camera_group.lock_on(camera_group.get_npc('Alona'), 1)
            counter_manager.add(counter.Counter(FPS*1.3, heart_show))
            pg.mixer.music.pause()

            


        def done_counter():
            dialogues.add(Dialogue('Oh, Icarus you are awake!\nYour friend is waiting for you.', 0.05, os.path.join('assets', 'sounds', 'jessica_voice.wav'), 'assets/characters/jessica/avatar.png', alona_walkin))
        counter_manager.add(counter.Counter(FPS*0.5, done_counter))
        


def icarus_sitchair(obj):
    player.change_frame(1, 1)
    player.rect.centerx = (obj.x * (TILE_SIZE/32)) + ((obj.width * (TILE_SIZE/32)) / 2)
    player.rect.centery = (obj.y * (TILE_SIZE/32)) - 80
    player.locked = True
    player.show_last = True
    counter_manager.add(counter.Counter(FPS*2, emily_sit1))

def emily_sit1():
    camera_group.get_npc('Emily').move_by(0, -250, 1)
    counter_manager.add(counter.Counter(FPS, emily_sit2))
def emily_sit2():
    dialogues.add(Dialogue("Good morning Icarus, Hello Alona.", 0.05, os.path.join('assets', 'sounds', 'emily_voice.wav'), 'assets/characters/emily/avatar.png', emily_sit3))
def emily_sit3():
    camera_group.get_npc('Emily').move_by(0, -250, 1)
    counter_manager.add(counter.Counter(FPS*1.5, emily_sit4))

def emily_sit4():
    camera_group.get_npc('Emily').move_by(500, 0, 2)
    counter_manager.add(counter.Counter(FPS*3, emily_sit5))
def emily_sit5():
    camera_group.get_npc('Emily').move_by(0, -100, 1)
    counter_manager.add(counter.Counter(FPS*2, emily_sit6))
def emily_sit6():
    dialogues.add(Dialogue("You can eat later, lets go play\nbasketball at the park!", 0.05, os.path.join('assets', 'sounds', 'emily_voice.wav'), 'assets/characters/emily/avatar.png', emily_sit7))
def emily_sit7():
    counter_manager.add(counter.Counter(FPS*1, emily_sit8))
def emily_sit8():
    camera_group.get_npc('Emily').move_by(900, 0, 2)
    counter_manager.add(counter.Counter(FPS*3, end_breakfast1))

def end_breakfast1():
    camera_group.get_npc("Alona").rect.x -= 20
    camera_group.get_npc("Alona").rect.y += 45
    camera_group.get_npc("Alona").image = pg.transform.scale_by(load_frame_from_spritesheet_with_tileset_size(pg.image.load('assets/characters/alona/alona.png'), 2, 2, 0, 0), 4)
    counter_manager.add(counter.Counter(FPS*1, alona_agree_bsktball))
def alona_agree_bsktball():
    dialogues.add(Dialogue("Lets go Icarus!", 0.05, os.path.join('assets', 'sounds', 'alona_voice.wav'), 'assets/characters/alona/avatar.png', alona_agree_bsktball_walkout))

def alona_agree_bsktball_walkout():
    camera_group.get_npc('Alona').show_last = True
    camera_group.get_npc('Alona').move_path([
            (0, 100, 0.2),
            (500, 0, 2)
        ])
    counter_manager.add(counter.Counter(FPS*3, icarus_standup1))

def icarus_standup1():
    global alona_walk_outside_flag
    player.change_frame(0, 0)
    player.rect.centery += 180
    player.locked = False
    player.show_last = False
    camera_group.get_npc('Alona').show_last = False
    alona_walk_outside_flag = True






def mother_wakeup():
    dialogues.add(Dialogue('ICARUS, WAKE UP!', 0.08, os.path.join('assets', 'sounds', 'jessica_voice.wav'), 'assets/characters/jessica/avatar.png', icarus_wakeup))
def icarus_wakeup():
    player.change_frame(0, 1)
    player.move(1, 0)
    counter_manager.add(counter.Counter(FPS*1, icarus_stop_wakeup))
def icarus_stop_wakeup():
    player.move(0, 0)
    player.change_frame(0, 0)
    player.locked = False
    pg.mixer.music.load(os.path.join('assets', 'sounds', 'a_beginners_house.wav'))
    pg.mixer.music.play(-1)

def interact_with_object(obj):
    if hasattr(obj, 'dialogue_func'):
        exec(obj.dialogue_func)
    else:
        dialogues.add(Dialogue(obj.dialogue, 0.08, os.path.join('assets', 'sounds', 'general_voice.wav'), None, None))

def icarus_interact():
    if player.direction == 'left':
        ray = pg.math.Vector2(camera_group.scroll_rect(player.rect).center)
        for i in range(80):
            break_loop = False
            for interaction_area in interaction_layer:
                interaction_area_rect = pg.Rect(interaction_area.x * (TILE_SIZE/32), interaction_area.y * (TILE_SIZE/32), interaction_area.width * (TILE_SIZE/32), interaction_area.height * (TILE_SIZE/32))
            
                if camera_group.scroll_rect(interaction_area_rect).collidepoint(ray):
                    interact_with_object(interaction_area)
                    break_loop = True
                    break
            if break_loop:
                break

            ray.x -= 1
    elif player.direction == 'right':
        ray = pg.math.Vector2(camera_group.scroll_rect(player.rect).center)
        for i in range(80):
            break_loop = False
            for interaction_area in interaction_layer:
                interaction_area_rect = pg.Rect(interaction_area.x * (TILE_SIZE/32), interaction_area.y * (TILE_SIZE/32), interaction_area.width * (TILE_SIZE/32), interaction_area.height * (TILE_SIZE/32))
            
                if camera_group.scroll_rect(interaction_area_rect).collidepoint(ray):
                    interact_with_object(interaction_area)
                    break_loop = True
                    break
            if break_loop:
                break

            ray.x += 1
    elif player.direction == 'up':
        ray = pg.math.Vector2(camera_group.scroll_rect(player.rect).center)
        for i in range(80):
            break_loop = False
            for interaction_area in interaction_layer:
                interaction_area_rect = pg.Rect(interaction_area.x * (TILE_SIZE/32), interaction_area.y * (TILE_SIZE/32), interaction_area.width * (TILE_SIZE/32), interaction_area.height * (TILE_SIZE/32))
            
                if camera_group.scroll_rect(interaction_area_rect).collidepoint(ray):
                    interact_with_object(interaction_area)
                    break_loop = True
                    break
            if break_loop:
                break

            ray.y -= 1
    elif player.direction == 'down':
        ray = pg.math.Vector2(camera_group.scroll_rect(player.rect).center)
        for i in range(80):
            break_loop = False
            for interaction_area in interaction_layer:
                interaction_area_rect = pg.Rect(interaction_area.x * (TILE_SIZE/32), interaction_area.y * (TILE_SIZE/32), interaction_area.width * (TILE_SIZE/32), interaction_area.height * (TILE_SIZE/32))
            
                if camera_group.scroll_rect(interaction_area_rect).collidepoint(ray):
                    interact_with_object(interaction_area)
                    break_loop = True
                    break
            if break_loop:
                break

            ray.y += 1


            
running = True
waiting_in_emily_room = 0
counter_manager.add(counter.Counter(FPS*3, mother_wakeup))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                if not player.locked:
                    icarus_interact()
                           

    
    if room_transition:

        if room_trans_ph2:
            black_overlay -= 5
            if black_overlay <= 0:
                room_transition = False
                room_trans_ph2 = False
        else:
            black_overlay += 5
            if black_overlay >= 255:
                room_trans_ph2 = True
                post_transition()
        
    if os.path.basename(tmx_data.filename) == 'Outside_house.tmx':
        screen.fill((0, 255, 244))
    else:
        screen.fill(bg_color)
    draw()
    if os.path.basename(tmx_data.filename) == 'Emily_room.tmx':
        waiting_in_emily_room += 1
        if waiting_in_emily_room > FPS*160:
            door_show()
    counter_manager.update()
    clock.tick(FPS)
    pg.display.flip()

