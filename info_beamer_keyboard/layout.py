import copy

class Layout:
    def __init__(self, json_data):
        json_data = copy.deepcopy(json_data)
        self.rows = []
        self.row_width = 0
        y = 0
        for row in json_data['rows']:
            if 'y' in row:
                y = row['y']
            x = 0
            keys = []
            for key in row['keys']:
                if isinstance(key, str):
                    key = {
                        'key': 'KEY_{}'.format(key),
                        'letter': key,
                        'type': 'letter'
                    }
                if 'x' in key:
                    x = key['x']
                else:
                    key['x'] = x
                key['y'] = y
                if 'width' not in key:
                    key['width'] = 1
                if 'descender' not in key:
                    key['descender'] = False
                keys.append(key)
                x += key['width']
            self.rows.append(keys)
            self.row_width = max(self.row_width, x)
            y += 1
        self.num_rows = y

    def __iter__(self):
        for row in self.rows:
            for key in row:
                yield key
