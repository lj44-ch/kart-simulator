from lib import Point, Vector

from . import motions


class Object:
    _name: str
    _formID: int

    _center: Point
    _angle: float

    angularMotion: motions.angulars.AngularMotion
    vectorialMotion: motions.vectorials.VectorialMotion

    _fill: str
    _opacity: float
    _mass: float
    _friction: float

    def formID(self) -> int:
        return self._formID

    def name(self) -> str:
        return self._name

    def center(self, deltaTime: float = 0) -> Point:
        if not deltaTime:
            return self._center
        return Point(*(Vector(*self.center()) + self.relativePosition(deltaTime)))

    def relativePosition(self, deltaTime: float) -> Vector:
        fromRotationCenterBefore = Vector.fromPoints(
            self.angularMotion.center(), self.center()
        )
        fromRotationCenterAfter = Vector(*fromRotationCenterBefore)
        fromRotationCenterAfter.rotate(self.angularMotion.relativeAngle(deltaTime))
        return (
            self.vectorialMotion.relativePosition(deltaTime)
            - fromRotationCenterBefore
            + fromRotationCenterAfter
        )

    def angle(self, deltaTime: float = 0) -> float:
        if not deltaTime:
            return self._angle
        return self._angle + self.relativeAngle(deltaTime)

    def relativeAngle(self, deltaTime: float) -> float:
        return self.angularMotion.relativeAngle(deltaTime)

    def fill(self) -> str:
        return self._fill

    def set_fill(self, color: str) -> None:
        self._fill = color

    def opacity(self) -> float:
        return self._opacity

    def mass(self) -> float:
        return self._mass

    def friction(self) -> float:
        return self._friction

    def translate(self, vector: Vector) -> None:
        self._center.translate(vector)

    def rotate(self, angle: float) -> None:
        self._angle += angle

    def updateReferences(self, deltaTime: float) -> None:
        # mise à jour de la vitesse angulaire
        # self._angle = self.angle(deltaTime)
        self.angularMotion.updateReferences(deltaTime)
        rotationCenter = Point(*self.angularMotion.center())
        rotationCenter.translate(self.vectorialMotion.relativePosition(deltaTime))
        self.angularMotion.set_center(rotationCenter)

        # mise à jour de la vitesse vectorielle
        # self._center = self.center(deltaTime)
        self.vectorialMotion.updateReferences(deltaTime)

    def collides(self, object: "Object") -> bool:
        return False

    def collisionPoint(self, object: "Object") -> Point:
        return object.center()

    def collisionTangent(self, object: "Object") -> Vector:
        return Vector(0, 0)

    def speedAtPoint(self, point: Point, deltaTime: float = 0) -> Vector:
        return self.angularMotion.speedAtPoint(
            point, deltaTime
        ) + self.vectorialMotion.speed(deltaTime)
