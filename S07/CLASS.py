class Car:
    def __init__(self, brand):
        self.brand = brand
        self.speed = 0
    def set_speed(self, speed):
        self.speed = speed
    def get_speed(self):
        return self.speed

mycar = Car("Renault")
print(mycar.get_speed())
mycar.set_speed(80)
print(mycar.get_speed())

yourcar = Car("Ferrari")
print(yourcar.speed)
print(yourcar.get_speed())


