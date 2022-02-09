import os
from COCOParser import COCOParser
from PASCALVOCParser import VOCParser
import pandas as pd

class ImageData():
    def __init__(self, obj):
        self.obj = obj
        self.meta_data = self.get_meta_data()
        self.df = self.meta_df()
        
    def get_meta_data(self):
        meta_data = {x:{"img_ids":[], "data_count":0} for x in self.obj.categories}
        for anno in self.obj.annotations:
            if isinstance(anno['category_id'], int):
                meta_data[self.obj.categories[anno['category_id'] - 1]]['data_count'] += 1
                meta_data[self.obj.categories[anno['category_id'] - 1]]['img_ids'].append(anno['image_id'])
            else:
                meta_data[anno['category_id']]['data_count'] += 1
                meta_data[anno['category_id']]['img_ids'].append(anno['image_id'])

        for k, v in meta_data.items():
            meta_data[k]['image_count'] = len(set(v['img_ids']))
            meta_data[k]['img_ids'] = [] 

        datas = []

        for k, v in meta_data.items():
            try:
                datas.append({"category": k, "image_count":v['image_count'], "data_count": v['data_count']})
            except KeyError: continue
        return datas
    
    def meta_df(self):
        df = pd.DataFrame.from_dict(self.meta_data)
        df.loc[-1] = ['total', len(self.obj), df['data_count'].sum()]  # adding a row
        df.index = df.index + 1  # shifting index
        df = df.sort_index()  # sorting by index
        return df

def main(file_paths, tasks, is_coco):
    result = {}
    df = []
    for path, task in zip(file_paths, tasks):
        result[task] = {}
        if is_coco: obj = COCOParser(path)
        else: obj = VOCParser(path)
        result[task]['total_image_count'] = len(obj)
        image_data = ImageData(obj)
        df.append(image_data.df)
        result[task]['datas'] = image_data.get_meta_data()
    

    if len(df) > 1:
        df_ = df[0]
        for i in range(1,  len(df)):
            df_ = df_.merge(df[i], how='inner', on='category')
        df = df_
    else:
        df = df[0]
        
    output_file = 'COCO' if is_coco else 'VOC'

    # Write JSON File
    obj.write_json(result, f'./log/{output_file}_meta.json')
    # Write Excel File
    df.to_excel(f'./log/{output_file}_meta.xlsx', index=False)


if __name__=='__main__':
    COCO_PATH = "../COCODataset_2017/annotations"
    VOC_PATH = "../PASCAL_VOC/VOCdevkit/VOC2007/Annotations"
    json_file_paths = ["instances_train2017.json", "instances_val2017.json"]
    file_paths = [os.path.join(COCO_PATH, x) for x in json_file_paths]
    tasks = ['train', 'val']

    main(file_paths, tasks, True)
    main([VOC_PATH], ['train'], False)