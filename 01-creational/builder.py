class UserBuilder:
    def __init__(self):
        self.d = {}
    def name(self,x): self.d['name'] = x; return self
    def age(self,v) : self.d['age'] = v; return self
    def build(self) : return self.d.copy()


u = UserBuilder().name('bao').age('2')

print(u)
