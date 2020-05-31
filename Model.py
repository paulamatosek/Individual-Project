
class Jewellery:
    def __init__(self, title, price,type):
        self.title = title
        self.price = price
        self.type = type


    def __str__(self):
        return '|%100s | %5s | %10s |' % \
               (self.title, self.price, self.type)