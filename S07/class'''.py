class Vehicle:
    def set_speed(self, speed):
        self.speed = speed
class Car(Vehicle):
    def __init__(self, brand, speed=0):
        self.car_brand = brand
        self.speed = speed
class Ferrari(Car):
    def __init__(self):
        #call the innit of the mother class
        super().__init__("Ferrari", 100)
        self.music = "classic"
    def make_cabrio(self):
        self.speed = 20
        self.music = "loud"
        return "wow"

mycar = Car("Renault")
yourcar = Ferrari() # ---> __init__
print(yourcar.car_brand)
yourcar.set_speed(120)
print(yourcar.speed)

print(yourcar.make_cabrio(), "and music is", yourcar.music, "and speed is", yourcar.speed)


