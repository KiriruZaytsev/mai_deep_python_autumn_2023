class CustomMeta(type):
    
    def __setattr__(cls, name, value):
        if not (name.startswith('__') or name.endswith('__')):
            name = f'custom_{name}'
        super(CustomMeta, cls).__setattr__(name, value)

    def __new__(cls, name, bases, dct):
        custom_dct = {}
        for attr_name, value in dct.items():
            if attr_name.startswith('__') and attr_name.endswith('__'):
                custom_dct[attr_name] = value
            else:
                custom_dct[f'custom_{attr_name}'] = value
        def _set_attr_(cls, key, value):
            cls.__dict__[f'custom_{key}'] = value
        
        custom_dct['__setattr__'] = _set_attr_
        return super().__new__(cls, name, bases, custom_dct)

    def __call__(cls, *args, **kwargs):
        inst = super().__call__(*args, **kwargs)
        return inst
        

class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


#assert CustomClass.custom_x == 50
#CustomClass.x  ошибка

#inst = CustomClass()
#assert inst.custom_x == 50
#assert inst.custom_val == 99
#assert inst.custom_line() == 100
#assert str(inst) == "Custom_by_metaclass"

#inst.x  # ошибка
#inst.val  # ошибка
#inst.line() # ошибка
#inst.yyy  # ошибка

#inst.dynamic = "added later"
#assert inst.custom_dynamic == "added later"
#inst.dynamic  # ошибка