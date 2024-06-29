#!/usr/bin/env python3

# prefix for all colors
# e.g. RED = "\033[0;31m"
#   'red': 31,
ALL_COLORS = {
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
    'reset': 0
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
        for obj in objs:
            #setattr(obj, '_parent_coloredstr', self)
            #obj._parent_coloredstr = self
            obj.__setattr__('parent_coloredstr', self)
            print(dir(obj))

    def __str__(self):
        color = self.color
        if color is None:
            color = ''

        built_str = ''.join([color + str(obj) for obj in self.objs])

        if not self.skip_reset:
            built_str += get_ansi('', 'reset')

        return built_str

    def __add__(self, right):
        return ColoredStr(self, right, color=self.color, skip_reset=self.skip_reset)

    def __radd__(self, left):
        if isinstance(left, str):
            return left + str(self)

        color = None
        skip_reset = False
        if hasattr(left, '_parent_coloredstr'):
            parent = getattr(left, 'parent_coloredstr')
            color = parent.color
            skip_reset = parent.skip_reset

        return ColoredStr(left, self, color=color, skip_reset=skip_reset)
    
    # get length without colors
    def __len__(self):
        return sum([len(obj) for obj in self.objs])


# define globals
for color in ALL_COLORS.keys():
    class_name = color.title().replace(' ', '')
    globals()[class_name] = type(
        class_name,
        (ColoredStr,),
        {
            'class_color': get_ansi(color)
        }
    )


if __name__ == '__main__':
    print(Red("this is" + Blue(' not ') + "a test"))

    print(len(ColoredStr('hello', color='G') + ColoredStr('world')))

