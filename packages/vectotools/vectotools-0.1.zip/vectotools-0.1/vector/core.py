from math import sqrt,acos
from functools import total_ordering

RAD = 57.2958


@total_ordering
class Vector():
    
    def __init__(self,x,y):
        self.__dict__['x'] = x
        self.__dict__['y'] = y
        self.len = self._calclen()

    def normalize(self):
        self.x = self.x/self.len
        self.y = self.y/self.len
    
    def normalized(self):
        x = self.x/self.len
        y = self.y/self.len
        return Vector(x,y)

    def angle_to(self,other,units='degrees'):
        c = (self*other)/(self.len*other.len)
        if c > 1:
            c = 1
        c = acos(c)
        if units == 'degrees':
            c*=RAD
        return round(c,2)

    def _calclen(self):
        return round(sqrt((self.x**2)+(self.y**2)),2)

    def __setattr__(self,name,value):
        self.__dict__[name] = round(value,2)
        if name != 'len':
            self.__dict__['len'] = self._calclen()

    def __neg__(self):
        return Vector(-self.x,-self.y)
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x,y)

    def __mul__(self, other):
        if type(other) == type(1) or type(other) == type(1.1):
            x = self.x*other
            y = self.y*other
            return Vector(x,y)
        elif type(other) == type(self):
            return (self.x*other.x)+(self.y*other.y)
        else:
            raise TypeError
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.len < other.len
    
    def __gt__(self, other):
        return self.len > other.len

    def __nonzero__(self):
        return bool(self.len)

    def __len__(self):
        return round(self.len)
    
    def __repr__(self):
        return "Vector object ({},{})".format(self.x,self.y)
