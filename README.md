# Image Annotation Tools

## Features

#### 1. Double Check Annotation Tool
Double check 2 coco json. Just for bbox, not for segmentation.

Keep the bbox with IoU greater than the threshold among the different two group of annotations from two people in the same image.

The remaining annotations require further manual review. 

```angular2html
# how to run it

e.g.
    
    coco_json1_file_path = 'J:\\workspace\\xxxxxx\\dataset1-annotator1.json'
    coco_json2_file_path = 'J:\\workspace\\xxxxxx\\dataset1-annotator2.json'

    double_check_two_cocos(coco_json1_file_path, coco_json2_file_path, os.path.join(os.path.abspath(os.curdir), "results"))

Group represent the two annotators.
Results contains two folders, one for each annotator.
Each group have matched and suspected annotations.

Double-check result will save in conclusion folder.
when one annotaion is matched with another annotation, the matched annotation with smaller area box will be saved in matched conclusion folder.
The final conclusion merge all matched annotations and suspected annotations with different color.
# color green represent matched. #1A971E
# color red represent not matched. #C9151A

Results is a batch of coco json files of one labeled image. For convenient import, conclusion result's metadata is based on group1 image, including: image id/file_name/file_path, and based on group1's category id.

# result file structure

results/
    conclusion/
        all/
            image1.json  # merged all matched and suspected annotations
            image2.json
        matched/
            image1.json
            image2.json
        suspected/
            image1.json
            image2.json
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

#### 2. COCO Json Merge / Split Tool
Split Tool: Split the coco json of one dataset with multiple labeled images, to a batch of coco json files of one labeled image.

```angular2html
# Split coco json
# how to run it
split_coco(input_file_path, output_dir_path)

```

Merge Tool: Merge a batch of coco json files of one labeled image to one coco json of one dataset with multiple labeled images.

```angular2html
# Merge coco json
# how to run it

# Merge the files in input dir, each file is a coco json file for one image.
input_dir_path = "J:\\workspace\\xxxxxx\\splited_double_check"

# Merge coco json result will be saved in this file
output_file = "J:\\workspace\\xxxxxx\\merged_double_check\\merged_double_check.json"

# The output file's image id and category id will be the same as the metadata file, mapping the same image filename and category name.
coco_metadata_json_file = "J:\\workspace\\xxxxxx\\dataset1-metadata.json"

# If you want to remap the image id, you can use this file path.
# If you use the original dataset with same image id, you can set this file path to "".
image_id_remapping_file = "J:\\workspace\\20240820\\double_check_dataset_image_mapping.json"
e.g.
        [
            {
            "id": 2030,
            "file_name": "Bthe_01.jpg",
            "annotated": false,
            "annotating": [],
            "num_annotations": 0
            },
            ...
        ]

merge_coco(input_dir_path, output_file, coco_metadata_json_file, image_id_remapping_file)
```