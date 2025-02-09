import threading
import time

import pygame

from Scripts.Engine import Transform, Vector, Controller, Collider

pygame.mixer.init()
damage_sound = pygame.mixer.Sound('assets/sounds/minecraft-death-sound.mp3')
death_sound = pygame.mixer.Sound('assets/sounds/death.mp3')
blaster_sound = pygame.mixer.Sound('assets/sounds/vyistrel-blastera-v-mejgalakticheskom-prostranstve.mp3')
stone_sound = pygame.mixer.Sound('assets/sounds/popadanie-tochno-v-tsel.mp3')


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


DURATION_GOLD_BULLET = 0.05
DURATION_ICE_BULLET = 3


class Character(GameObject):
    def __init__(self, image_path, damaged_img, cords, speed, screen):
        super().__init__(cords, image_path, scale=3, tag_collision='character')
        # damage bullets
        self.damage_bullet = 10
        self.damage_goldBullet = 15
        self.damage_iceBullet = 5
        self.cold_resist = 0.1
        self.duration_bullet = 1
        self.controller = Controller()
        self.first_time = time.time()
        self.camera = None
        self.screen = screen
        # stats
        self.health = 100
        self.speed = speed
        self.exp = 0
        self.level = 1
        # colliders
        self.collider_area_attack = Collider((500, 500), self.transform, offset=(-225, -225))
        self.collider_character = Collider((80, 80), self.transform, offset=(-20, -20))
        # buffs
        self.can_shoot_gold_bullet = False
        self.can_shoot_ice_bullet = False
        self.counter = 0
        self.max_cords = (-2000, 2000)
        self.background_offset = Vector(self.transform.vector.get_cords())

        self.damage_sprite = pygame.transform.scale(pygame.image.load(damaged_img).convert_alpha(), (
            pygame.image.load(damaged_img).convert_alpha().get_width() * self.scale,
            pygame.image.load(damaged_img).convert_alpha().get_height() * self.scale))

    def update_collision(self, objects: list[GameObject]):
        for game_object in objects:
            if game_object.tag_collision == 'enemy':
                if self.collider_area_attack.on_collider_stay(game_object.collider):
                    if self.check_reload(self.duration_bullet):
                        self.shoot(game_object)
                if self.collider_character.on_collider_stay(game_object.collider):
                    game_object.attack(self)
            if game_object.tag_collision == 'bullet_enemy':
                if self.collider_character.on_collider_stay(game_object.collider):
                    self.get_damage(game_object.damage)
                    game_object.is_dead = True

    def get_damage(self, damage):
        self.sprite = self.damage_sprite
        threading.Timer(0.1, self.return_normal_sprite).start()
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            death_sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))

    def return_normal_sprite(self):
        self.sprite = self.normal_sprite

    def shoot(self, target):
        self.counter += 1
        bullet = Bullet('assets/bullets/bullet.png', self.transform.vector.get_cords(), target, self.damage_bullet)
        stone_sound.play()
        self.camera.add_objects(bullet)
        if self.can_shoot_gold_bullet:
            threading.Timer(DURATION_GOLD_BULLET, self.shoot_gold, args=[target]).start()
        if self.counter % DURATION_ICE_BULLET == 0 and self.counter >= DURATION_ICE_BULLET and self.can_shoot_ice_bullet:
            threading.Timer(0.2, self.shoot_ice, args=[target]).start()

    def shoot_gold(self, target):
        target: Enemy = target
        if not target.is_dead:
            bullet = Bullet('assets/bullets/gold_bullet.png', self.transform.vector.get_cords(), target,
                            self.damage_goldBullet)
            self.camera.add_objects(bullet)
        return 0

    def shoot_ice(self, target):
        target: Enemy = target
        bullet = IceBullet('assets/bullets/ice_bullet.png', self.transform.vector.get_cords(), target,
                           self.damage_iceBullet, self.cold_resist)
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
        if keys[self.controller.right] and self.max_cords[1] > self.transform.vector.x:
            x = 1
        if keys[self.controller.left] and self.max_cords[0] < self.transform.vector.x:
            x = -1
        if keys[self.controller.down] and self.max_cords[1] > self.transform.vector.y:
            y = 1
        if keys[self.controller.up] and self.max_cords[0] < self.transform.vector.y:
            y = -1
        vector = Vector((x, y))
        if x and y:
            normalized_vector = vector.normalize()
            self.transform.vector += Vector((normalized_vector.x * self.speed, normalized_vector.y * self.speed))
            self.background_offset -= Vector((normalized_vector.x * self.speed, normalized_vector.y * self.speed))
        else:
            self.transform.vector += Vector((vector.x * self.speed, vector.y * self.speed))
            self.background_offset -= Vector((vector.x * self.speed, vector.y * self.speed))

    def update_frame(self):
        self.move()
        if self.exp >= 30:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
            self.level += 1
            if self.level == 5:
                self.can_shoot_gold_bullet = True
            if self.level == 7:
                self.can_shoot_ice_bullet = True
            self.exp = 0


class Enemy(GameObject):
    def __init__(self, image_path, damaged_img, cords, character: Character, screen, speed=1, health=100, damage=1):
        super().__init__(cords, image_path, scale=3, tag_collision='enemy')
        self.damage = damage
        self.health = health
        self.can_walk = True
        self.speed = speed
        self.character = character
        self.screen = screen
        self.start_time = time.time()
        self.can_fight = True
        # collider
        self.collider = Collider((80, 80), self.transform, offset=(-20, -20))
        # sprite
        self.damage_sprite = pygame.transform.scale(pygame.image.load(damaged_img).convert_alpha(), (
            pygame.image.load(damaged_img).convert_alpha().get_width() * self.scale,
            pygame.image.load(damaged_img).convert_alpha().get_height() * self.scale))

    def update_collision(self, objects: list[GameObject]):
        for game_object in objects:
            if game_object.tag_collision == 'bullet':
                if self.collider.on_collider_stay(game_object.collider):
                    game_object.on_enter_body()
                    damage_sound.play()
                    damage = game_object.damage
                    game_object.is_dead = True
                    if self.health - damage <= 0:
                        self.character.exp += 500
                        self.is_dead = True
                    else:
                        self.health -= damage
                        self.sprite = self.damage_sprite
                        threading.Timer(0.1, self.return_normal_sprite).start()

    def attack(self, other):
        self.reload()
        if self.can_fight:
            other.get_damage(self.damage)
            self.can_fight = False

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
    def __init__(self, image_path, cords, target, damage=50, tag='bullet'):
        super().__init__(cords, image_path=image_path, scale=2, tag_collision=tag)
        self.sprite = pygame.transform.rotate(pygame.image.load(self.image_path).convert_alpha(), 0)
        self.target = target
        self.is_dead = False
        self.collider = Collider((1, 1), self.transform)
        self.damage = damage

    def update_frame(self):
        if self.target.is_dead or Transform.dist(self.transform, self.target.transform) < 0.8:
            self.is_dead = True
        else:
            self.transform.goto(self.target.transform.vector, 10)

    def on_enter_body(self):
        pass


class IceBullet(Bullet):
    def __init__(self, image_path, cords, target, damage, ice_debuff):
        super().__init__(image_path, cords, target, damage)
        self.ice_debuff = ice_debuff

    def on_enter_body(self):
        speed = self.target.speed
        self.target.speed -= 1
        threading.Timer(1, self.return_normal_speed, args=[speed]).start()

    def return_normal_speed(self, speed):
        self.target.speed = speed


class StaticObject(GameObject):
    def __init__(self, cord, image_path):
        super().__init__(cord, image_path, 1)


class EnemyShooters(Enemy):
    def __init__(self, image_path, damage_img, cords, character, screen, speed, health, damage):
        super().__init__(image_path, damage_img, cords, character, screen, speed, health, damage)
        self.camera = character.camera
        self.target_walk = Vector((0, 0))

    def attack(self, other):
        self.reload()
        blaster_sound.play()
        if self.can_fight:
            bullet = EnemyBullet('assets/bullets/robot_bullet.png', self.transform.vector.get_cords(),
                                 Vector(self.character.transform.vector.get_cords()), self.damage)
            self.camera.add_objects(bullet)
            self.can_fight = False

    def update_frame(self):
        vector = self.character.transform.vector
        if int(self.transform.dist(vector)) < 300:
            self.can_walk = True
        if self.can_walk:
            if self.transform.vector.x >= self.character.transform.vector.x:
                self.transform.vector.x += 1 * self.speed
            else:
                self.transform.vector.x -= 1 * self.speed
            if self.transform.vector.y >= self.transform.vector.y:
                self.transform.vector.y += 1 * self.speed
            else:
                self.transform.vector.y -= 1 * self.speed
        if int(self.transform.dist(vector)) > 550:
            self.can_walk = False
        self.attack(self.character)

    def reload(self):
        if time.time() - self.start_time >= 1.5:
            self.can_fight = True
            self.start_time = time.time()


class EnemyBullet(Bullet):
    def __init__(self, image_path, cord, target, damage, tag='bullet_enemy'):
        super().__init__(image_path, cord, target, damage, tag)

    def update_frame(self):
        if Transform.dist(self.transform, self.target) < 4:
            self.is_dead = True
        else:
            self.transform.goto(self.target, 6)
