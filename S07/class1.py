class Car:
    def __init__(self, brand, speed=0): #parameter of all methods, always the same, its the object itself
        self.car_brand = brand   #local attribute, can be applied all over the object, brand is a variable, self.brand is a variable(attribute, attached to the object
        self.speed = speed

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def get_brand_nationality(self):  #if you write brand (self, brand) is needed, if you put car_brand you already have smth called that inside the program
        if self.car_brand == "Renault":
            return "France"
        elif self.car_brand == "Ferrari":
            return "Italy"



mycar = Car("Renault", 30)
print(mycar.get_speed())
mycar.set_speed(80)
print(mycar.speed)

print(mycar.get_brand_nationality())

yourcar = Car("Ferrari", 250)
print(yourcar.speed) #prefered
print(yourcar.get_speed())