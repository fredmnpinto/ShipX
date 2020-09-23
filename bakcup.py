class Spritesheet():
    def __init__(self, obj):
        json_path = f'img/{obj}/{obj}.json'
        try:
            img_path = f'img/{obj}/{obj}.png'
        except:
            img_path = f'img/{obj}/{obj}.jpg'
        self.spritesheet = pg.image.load(img_path)
        self.json_file = json_path
        self.SPRITES = None
        self.frames = []
        self.read_json()

    def read_json(self):
        with open(self.json_file, 'r') as data:
            self.SPRITES = json.load(data)
            print('Printing json data as:')
            for i in self.SPRITES['frames']:
                print(i)
                frame_values = []

                for x in self.SPRITES['frames'][i]['frame'].values():
                    print(x)
                    frame_values.append(x)

                self.frames.append(self.get_image(frame_values[0], frame_values[1], frame_values[2], frame_values[3]))
                frame_values.clear()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

