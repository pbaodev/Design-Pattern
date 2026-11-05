class Button : pass

class HTML(Button) : pass
class MobileButton(Button): pass

class Dialog:
    def create(self): raise NotImplementedError

class Web(Dialog):
    def create(self):
        return HTML()
    
class Mobile(Dialog):
    def create(self):
        return MobileButton()
    
b=Web().create()
