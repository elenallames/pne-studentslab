class Car:
    def __init__(self, brand, speed=0):
        self.car_brand = brand
        self.speed = speed

    def set_speed(self, speed):
        self.speed = speed

class Ferrari(Car):
    pass

mycar = Car("Renault")
yourcar = Ferrari("Ferrari")
print(yourcar.car_brand)
yourcar.set_speed(120)
print(yourcar.speed)