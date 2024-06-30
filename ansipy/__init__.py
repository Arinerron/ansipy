#!/usr/bin/env python3

# prefix for all colors
# e.g. RED = "\033[0;31m"
#   'red': 31,
ALL_COLORS = {
    'reset': 0,
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
}

ALL_DECORATORS = {
    'reset': 0,
    'bold': 1
}


def get_ansi(color='', decorator=''):
    retval = '\033['

    if decorator:
        retval += str(ALL_DECORATORS[decorator])
    else:
        retval += '0'

    if decorator != 'reset':
        retval += ';'

        if color:
            retval += str(ALL_COLORS[color])

    retval += 'm'
    return retval



class ColoredStr:
    def __init__(self, *objs, color=None, skip_reset=False):
        if color is None:
            color = getattr(self.__class__, 'class_color', None)
        self.color = color

        self.skip_reset = skip_reset
        self.objs = list(objs)

    def __str__(self):
        color = self.color
        if color is None:
            color = ''

        # TODO: detect ansi reset and "undo" if str
        built_str = ''.join([color + str(obj) for obj in self.objs])

        if not self.skip_reset:
            built_str += get_ansi('', 'reset')
        
        return built_str

    def __add__(self, right):
        return ColoredStr(self, right, color=None, skip_reset=False)

    def __radd__(self, left):
        if isinstance(left, str):
            return left + str(self)

        color = None
        skip_reset = False
        return ColoredStr(left, self, color=color, skip_reset=skip_reset)
    
    # get length without colors
    def __len__(self):
        return sum([len(obj) for obj in self.objs])

    
    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.objs)[1:-1] + ')'


def _create_class(color, decorator):
    if color == 'reset':
        color = None
    if decorator == 'reset':
        decorator = None

    settings = list()
    if color != None:
        settings.append(color)
    if decorator != None:
        settings.append(decorator)
    if not settings:
        return

    class_name_pre_formatting = ' '.join(settings)
    class_name = class_name_pre_formatting.title().replace(' ', '')

    globals()[class_name] = type(
        class_name,
        (ColoredStr,),
        {
            'class_color': get_ansi(color, decorator)
        }
    )


# define globals
for color in ALL_COLORS.keys():
    for decorator in ALL_DECORATORS.keys():
        _create_class(color, decorator)

del _create_class

