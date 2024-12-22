from Scripts.Engine import Transform, Vector, Controller, Collider
import pygame
import time
import threading


class GameObject:
    def __init__(self, cords, image_path, scale=1, tag_collision='default'):
        self.image_path = image_path
        self.scale = scale
        self.transform = Transform(cords)
        self.normal_sprite = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (
            pygame.image.load(image_path).convert_alpha().get_width() * self.scale,
            pygame.image.load(image_path).convert_alpha().get_height() * self.scale))
        self.sprite = self.normal_sprite
        self.tag_collision = tag_collision
        self.is_dead = False

    def update_frame(self):
        pass

    def update_collision(self, objects):
        pass

    def __str__(self):
        return self.tag_collision


DURATION_BULLET = 0.5
DURATION_GOLD_BULLET = 0.05
DURATION_ICE_BULLET = 3


class Character(GameObject):
    def __init__(self, cords, speed, screen):
        super().__init__(cords, 'character.png', scale=3, tag_collision='character')
        self.controller = Controller()
        self.first_time = time.time()
        self.camera = None
        self.screen = screen
        # stats
        self.health = 100
        self.speed = speed
        self.exp = 0
        # colliders
        self.collider_area_attack = Collider((500, 500), self.transform, offset=(-225, -225))
        self.collider_character = Collider((80, 80), self.transform, offset=(-20, -20))
        # buffs
        self.gold_bullet = False

        self.counter = 0

    def update_collision(self, objects: list[GameObject]):
        for game_object in objects:
            if game_object.tag_collision == 'enemy':
                if self.collider_area_attack.on_collider_stay(game_object.collider):
                    if self.check_reload(DURATION_BULLET):
                        self.shoot(game_object)
                if self.collider_character.on_collider_stay(game_object.collider):
                    game_object.attack(self)

    def shoot(self, target):
        self.counter += 1
        bullet = Bullet('bullet.png', self.transform.vector.get_cords(), target, damage=5)
        self.camera.add_objects(bullet)
        if self.gold_bullet:
            threading.Timer(DURATION_GOLD_BULLET, self.shoot_gold, args=[target]).start()
        if self.counter % DURATION_ICE_BULLET == 0 and self.counter >= DURATION_ICE_BULLET:
            threading.Timer(0.2, self.shoot_ice, args=[target]).start()

    def shoot_gold(self, target):
        target: Enemy = target
        if not target.is_dead:
            bullet = Bullet('gold_bullet.png', self.transform.vector.get_cords(), target, damage=15)
            self.camera.add_objects(bullet)
        return 0

    def shoot_ice(self, target):
        target: Enemy = target
        bullet = IceBullet('ice_bullet.png', self.transform.vector.get_cords(), target, damage=25, ice_debuff=1)
        self.camera.add_objects(bullet)

    def check_reload(self, duration):
        if time.time() - self.first_time >= duration:
            self.first_time = time.time()
            return True
        else:
            return False

    def move(self):
        keys = pygame.key.get_pressed()
        x, y = 0, 0
        if keys[self.controller.right]:
            x = 1
        if keys[self.controller.left]:
            x = -1
        if keys[self.controller.down]:
            y = 1
        if keys[self.controller.up]:
            y = -1
        vector = Vector((x, y))
        if x and y:
            normalized_vector = vector.normalize()
            self.transform.vector += Vector((normalized_vector.x * self.speed, normalized_vector.y * self.speed))
        else:
            self.transform.vector += Vector((vector.x * self.speed, vector.y * self.speed))

    def update_frame(self):
        self.move()
        if self.exp == 10:
            self.exp = 0
            self.gold_bullet = True


class Enemy(GameObject):
    def __init__(self, cords, character: Character, screen, speed=1, health=100, id=0):
        super().__init__(cords, 'enemy.png', scale=3, tag_collision='enemy')
        self.health = health
        self.can_walk = True
        self.speed = speed
        self.character = character
        self.screen = screen
        self.start_time = time.time()
        self.can_fight = True
        self.id = id
        # collider
        self.collider = Collider((80, 80), self.transform, offset=(-20, -20))
        # sprite
        self.damage_sprite = pygame.transform.scale(pygame.image.load('enemy_damage.png').convert_alpha(), (
            pygame.image.load('enemy_damage.png').convert_alpha().get_width() * self.scale,
            pygame.image.load('enemy_damage.png').convert_alpha().get_height() * self.scale))

    def update_collision(self, objects: list[GameObject]):
        for game_object in objects:
            if game_object.tag_collision == 'bullet':
                if self.collider.on_collider_stay(game_object.collider):
                    game_object.on_enter_body()
                    if self.health - game_object.damage <= 0:
                        self.character.exp += 10
                        self.is_dead = True
                    else:
                        self.health -= game_object.damage
                        self.sprite = self.damage_sprite
                        threading.Timer(0.1, self.return_normal_sprite).start()
                    game_object.is_dead = True

    def attack(self, other):
        self.reload()
        if self.can_fight:
            other.health -= 10
            self.can_fight = False
            print(other.health, self.id)

    def return_normal_sprite(self):
        self.sprite = self.normal_sprite

    def update_frame(self):
        vector = self.character.transform.vector
        if int(self.transform.dist(vector)) < 50:
            self.can_walk = False
        elif int(self.transform.dist(vector)) > 70:
            self.can_walk = True
        if self.can_walk:
            self.transform.goto(self.character.transform.vector, self.speed)

    def reload(self):
        if time.time() - self.start_time >= 3:
            self.can_fight = True
            self.start_time = time.time()


class Bullet(GameObject):
    def __init__(self, image_path, cords, target, damage=50):
        super().__init__(cords, image_path=image_path, scale=2, tag_collision='bullet')
        self.sprite = pygame.transform.rotate(pygame.image.load(self.image_path).convert_alpha(), 0)
        self.target = target
        self.is_dead = False
        self.collider = Collider((1, 1), self.transform)
        self.damage = damage

    def update_frame(self):
        self.transform.goto(self.target.transform.vector, 10)
        if self.target.is_dead:
            self.is_dead = True

    def on_enter_body(self):
        pass


class IceBullet(Bullet):
    def __init__(self, image_path, cords, target, damage, ice_debuff=1):
        super().__init__(image_path, cords, target, damage)
        self.ice_debuff = ice_debuff

    def on_enter_body(self):
        speed = self.target.speed
        self.target.speed -= 1
        threading.Timer(1, self.return_normal_speed, args=[speed]).start()

    def return_normal_speed(self, speed):
        print(speed)
        self.target.speed = speed


class StaticObject(GameObject):
    def __init__(self, cord, image_path):
        super().__init__(cord, image_path, 1)
