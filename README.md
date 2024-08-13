
# Image Annotation Tools

## Features
#### 1. COCO Json Split Tool
Split the coco json of multiple labeled images into one labeled image and one coco json.

```angular2html
split_coco(input_file_path, output_dir_path)
```

#### 2. Double Check Annotation Tool
Double check 2 coco json. Just for bbox, not for segmentation.

Keep the bbox with IoU greater than the threshold among the different two group of annotations from two people in the same image.

The remaining annotations require further manual inspection. 

```angular2html
# how to run it

e.g.
    
    coco_json1_file_path = 'J:\\workspace_j\\20240812-yolo10\\lotus_PBCs_new_20240812_one_cal\\coco-1723429856.0694387-20240812-1.json'
    coco_json2_file_path = 'J:\\workspace_j\\20240812-yolo10\\lotus_PBCs_new_20240812_one_cal\\coco-1723429856.0694387-20240812-2.json'

    double_check_two_cocos(coco_json1_file_path, coco_json2_file_path, os.path.join(os.path.abspath(os.curdir), "results"))

# result file structure

group represent the two annotators.
results contains two folders, one for each annotator.
each group have matched and suspected annotations.

results/
    group1/
        matched/
            image1.json
            image2.json
        suspected/
            image1.json
            image2.json
    group2/
        matched/
            image1.json
            image2.json
        suspected/
            image1.json
            image2.json


```

#### 3. COCO 2 YOLO Tool
COCO Json convert to YOLO txt format, for YOLO training.

```angular2html
## 1. cd ./coco_2_yolo_tool

## 2. install 
# pip install -r requirements.txt

## 3. run 
directory_coco_json = "J:\\workspace_j\\20240812-yolo10\\lotus_PBCs_new_20240812_one_cal"
output_yolo_dir_path = "J:\\workspace_j\\20240812-yolo10\\lotus_PBCs_new_20240812_one_cal\\labels\\training"

source = "COCO"

if source == "COCO":
    convert_coco_json(
        directory_coco_json,  # directory with *.json
        output_yolo_dir_path,
        use_segments=True,
        cls91to80=False,
    )


```