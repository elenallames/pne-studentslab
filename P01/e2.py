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


# -- Creating a Null sequence
s1 = Seq()
# -- Creating a valid sequence
s2 = Seq("TATAC")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")
