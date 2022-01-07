import lib

from .VectorialMotion import VectorialMotion


class UniformlyAcceleratedMotion(VectorialMotion):
    _acceleration: lib.Vector

    def __init__(
        self,
        initialSpeed: lib.Vector = lib.Vector((0, 0)),
        acceleration: lib.Vector = lib.Vector((0, 0)),
    ) -> None:
        self._acceleration = acceleration
        super().__init__(initialSpeed)

    def updateReferences(self, deltaTime: float) -> None:
        self._speed = self.speed(deltaTime)
        self.updateIsStatic()

    def relativePosition(self, deltaTime: float = 0) -> lib.Vector:
        return self._acceleration * (deltaTime ** 2 / 2) + self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> lib.Vector:
        return self._acceleration * deltaTime + self._speed

    def acceleration(self, deltaTime: float = 0) -> lib.Vector:
        return self._acceleration

    def set_acceleration(self, newAcceleration: lib.Vector) -> None:
        self._acceleration = newAcceleration
        self.updateIsStatic()

    def updateIsStatic(self) -> None:
        self._static = not (self.speed() or self.acceleration())