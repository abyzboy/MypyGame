from GameObject import GameObject


class Enemy(GameObject):
    def __init__(self, cords, target, speed, screen):
        super().__init__(cords, '../../enemy.png', scale=3)
        self.can_walk = True
        self.speed = speed
        self.target = target
        self.screen = screen

    def update_frame(self):
        vector = self.target.camera.offset + self.target.transform.vector
        if int(self.transform.dist(vector)) < 50:
            self.can_walk = False
        elif int(self.transform.dist(self.target.camera.offset + self.target.transform.vector)) > 70:
            pass
        if self.can_walk:
            self.transform.goto(self.target.camera.offset + self.target.transform.vector, self.speed)
