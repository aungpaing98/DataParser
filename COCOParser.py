import json
from AbstractParser import AbstractParser

class COCOParser(AbstractParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.data_  = self.load_file()
        self.annotations = self.get_annotations()
        self.categories = self.get_categories()
        self.data = self.data_process()
        

    def data_process(self):
        imgs_ = {}
        imgs = self.data_['images']
        for img in imgs:
            imgs_[img['id']] = img
            imgs_[img['id']]['annotations'] = []
        
        for anno in self.annotations:
            imgs_[anno['image_id']]['annotations'].append(anno)
        return [x for _, x in imgs_.items()]
        

    def load_file(self):
        with open(self.file_path, 'r') as reader:
            data = json.load(reader)
        return data
    
    def get_annotations(self):
        """
        Return in Annotation format.
        """
        return self.data_['annotations']
    
    def get_categories(self):
        """
        Return Detection Object List.
        """
        # 1 ~ 90 (80 classes)
        # ['person', 'cat', '', 'car']
        categories = self.data_['categories']
        cats = [""] * 90
        for cat in categories:
            id_ = cat['id'] - 1
            cats[id_] = cat['name']
        return cats
    
    # def get_category(self, id_):
    #     cats = []
    #     for anno in self.data[id_]["annotations"]:
    #         cats.append(self.categories[anno['category_id']])
    #     return cats
    
