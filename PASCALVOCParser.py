import os
import glob
import xml.etree.ElementTree as ET

from AbstractParser import AbstractParser

class VOCParser(AbstractParser):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.data, self.categories = self.load_file()
        self.annotations = self.data_process()
        
    def data_process(self):
        annotations = []
        imgs = self.data
        for img in imgs:
            for anno in img['annotations']:
                annotations.append(anno)
        return annotations
        
    def load_file(self):
        data = []
        object_names = []


        for file in glob.glob(self.file_path + "/*.xml"):
            img_id = os.path.split(file)[-1].split('.')[0]
            tree = ET.parse(file)
            root = tree.getroot()

            # Create new image instance
            img_obj = {'annotations' : []}
            img_obj['file_name'] = root.find('filename').text
            # Image size : W, H, D
            for size_ in root.find('size'):
                img_obj[size_.tag] = size_.text

            for obj in root.findall('object'):
                obj_instance = {}
                obj_instance['category_id'] = obj.find('name').text
                obj_instance['pose'] = obj.find('pose').text
                obj_instance['truncated'] = obj.find('truncated').text
                obj_instance['difficult'] = obj.find('difficult').text
                bnd_ = []
                for coor in obj.find('bndbox').iter():
                    bnd_.append(coor.text)
                obj_instance['bbox'] = bnd_[1:]
            
                obj_instance["image_id"] = img_id
                img_obj["annotations"].append(obj_instance)
                object_names.append(obj.find('name').text)
            
            data.append(img_obj)
        return data, list(set(object_names))

# VOC_PATH = "PASCAL_VOC/VOCdevkit/VOC2007/Annotations"
# voc = VOCParser(VOC_PATH)