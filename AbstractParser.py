import json

class AbstractParser:
    def __init__(self, file_path):
        self.file_path = file_path
        # List image instance
        self.data = self.load_file()
        self.categories = None
        self.annotations = None

    def __getitem__(self, id_):
        return self.data[id_]

    def __len__(self):
        return len(self.data)
            
    def __repr__(self):
        print(f'Dataset with {self.__len__()} images')


    def load_file(self):
        pass

    def get_bnd_boxes(self, id_):
        return [x['bbox'] for x in self.data[id_]["annotations"]]

    def get_image(self, id_):
        return self.data[id_]["file_name"]
    
    # def get_category(self, id_):
    #     return [x['category_id'] for x in self.data[id_]["annotations"]]

    @staticmethod
    def write_json(obj, file_name):
        obj_string = json.dumps(obj, indent=4)
        with open(file_name, 'w') as writer:
            writer.write(obj_string)