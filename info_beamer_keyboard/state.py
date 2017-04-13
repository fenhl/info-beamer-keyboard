import copy
import evdev

class State:
    def __init__(self, layout):
        self.layout = layout
        self.pressed = set()

    def __copy__(self):
        result = type(self)(self.layout)
        result.pressed = self.pressed.copy()
        return result

    def copy(self):
        return copy.copy(self)

    def dump(self):
        with open('data.json', 'w') as data_f:
            json.dump(self.to_json(), data_f, indent=4, sort_keys=True)
            print(file=data_f) # add trailing newline

    def to_json(self):
        result = []
        for key in self.layout:
            key = key.copy()
            key['pressed'] = key['key'] in self.pressed
            result.append(key)
        return {
            'keys': result,
            'meta': {
                'keySize': 50,
                'numRows': self.layout.num_rows,
                'rowWidth': self.layout.row_width
            }
        }

    def with_event(self, device, event):
        if event.type != evdev.ecodes.EV_KEY:
            # we don't care about mouse events or timestamps, only keyboard input
            return self
        key_code = evdev.ecodes.KEY[event.code]
        if event.value == 1:
            # press
            result = self.copy()
            result.pressed.add(key_code)
            return result
        elif event.value == 0:
            # release
            result = self.copy()
            result.pressed.remove(key_code)
            return result
        return self # hold
