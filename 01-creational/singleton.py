class AppConfig:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance= super().__new__(cls)
        return cls._instance

a = AppConfig()
b = AppConfig()

print(a is b)

# -----------------

class AppConfig2:
    _obj = None
    def __new__(cls):
        if cls._obj is None:
            cls._obj = object.__new__(cls)
        return cls._obj
    
c = AppConfig2()
d = AppConfig2()
print(c is d)