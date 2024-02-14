#exercice 1

class Seq:
    def __init__(self, strbases):
        count = 0
        for e in strbases:
            if e == "A":
                count += 1
            if e == "C":
                count += 1
            if e == "G":
                count += 1
            if e == "T":
                count += 1
        if count == len(strbases):
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR!!"
            print("ERROR!!")
#You can also use a for loop and if it is different than the four bases it is error

    def __str__(self):
        return self.strbases



s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")

