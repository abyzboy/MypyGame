from Scripts.GameObjects.GameObject import GameObject


class StaticObject(GameObject):
    def __init__(self, cord, image_path):
        super().__init__(cord, image_path, 1)
