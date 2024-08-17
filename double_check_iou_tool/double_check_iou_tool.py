import os.path

import utils


def cal_iou(box1, box2):
    """
    calculate two coco bbox's IOU.
    "bbox": [x_min,y_min,width,height]
    :param box1:
    :param box2:
    :return: IoU float
    """
    x1_min, y1_min, x1_max, y1_max = box1[0], box1[1], box1[0] + box1[2], box1[1] + box1[3]
    x2_min, y2_min, x2_max, y2_max = box2[0], box2[1], box2[0] + box2[2], box2[1] + box2[3]

    # cal inter
    x_inter_min = max(x1_min, x2_min)
    x_inter_max = min(x1_max, x2_max)
    y_inter_min = max(y1_min, y2_min)
    y_inter_max = min(y1_max, y2_max)

    # cal junction area
    inter_width = max(0, x_inter_max - x_inter_min)
    inter_height = max(0, y_inter_max - y_inter_min)
    junction_area = inter_width * inter_height

    # cal box area
    boxa_area = (x1_max - x1_min) * (y1_max - y1_min)
    boxb_area = (x2_max - x2_min) * (y2_max - y2_min)

    # cal union area
    union_area = boxa_area + boxb_area - junction_area

    if union_area == 0:
        return 0.0

    # cal IoU
    iou = junction_area / union_area

    return iou


def gen_new_coco_dict(coco_dict, annotations_list):
    new_coco_dict = {}
    new_coco_dict["images"] = coco_dict["images"]
    new_coco_dict["categories"] = coco_dict["categories"]
    new_coco_dict["annotations"] = annotations_list
    return new_coco_dict


def get_all_annotaions_in_image(image, coco_data_dict):
    this_image_dict = {}
    this_image_dict["images"] = [image]
    this_image_dict["categories"] = coco_data_dict["categories"]
    this_image_dict["annotations"] = []

    for annotation in coco_data_dict["annotations"]:
        if annotation["image_id"] == image["id"]:
            # print(annotation)
            this_image_dict["annotations"].append(annotation)
            # print(this_image_dict)
    return this_image_dict


def get_this_image_in_group(image, coco_data_dict) -> (dict, bool):
    for image_in_other_group in coco_data_dict["images"]:
        if image["file_name"] == image_in_other_group["file_name"]:
            return image_in_other_group, True
    return {}, False


def if_annotation_in_group1_is_smaller_remain(annotation1, annotation2, image_to_inherit,
                                              annotation_category_to_inherit, set_color) -> dict:
    # 1. smaller box area remain.
    if annotation1["bbox"][2] * annotation1["bbox"][3] <= annotation2["bbox"][2] * annotation2["bbox"][3]:
        return convert_conclusion_annotaion(annotation1, image_to_inherit, annotation_category_to_inherit, set_color)
    return None


# conclusion annotation is based on group1 image, image id/file_name/path, and based on group1's category id.
# color green represent matched. #1A971E
# color red represent not matched.  #C9151A
def convert_conclusion_annotaion(annotation, image_to_inherit, annotation_category_to_inherit, set_color) -> dict:
    annotation["image_id"] = image_to_inherit["id"]
    annotation["category_id"] = annotation_category_to_inherit["category_id"]
    if set_color is not None:
        # color green represent matched. #1A971E
        # color red represent not matched.  #C9151A
        annotation["color"] = set_color
    return annotation


def double_check_two_cocos(
        coco_json1_file_path,
        coco_json2_file_path,
        double_check_result_output_dir_path,
        iou_threshold=0.5

):
    coco1_data_dict = utils.file_json_loads(coco_json1_file_path)
    coco2_data_dict = utils.file_json_loads(coco_json2_file_path)

    # 1. all images in input1
    for image in coco1_data_dict["images"]:

        if image["path"] == "/datasets/PBCs_new/aba_01.jpg":
            pass

        this_image_in_group2, is_found_image = get_this_image_in_group(image, coco2_data_dict)
        if not is_found_image:
            continue;

        # 1.1 two group of annotationall_annotations_in_this_image_dict_2 = {dict: 3} {'annotations': [], 'categories': [{'color': '#0000ff', 'id': 3, 'keypoint_colors': [], 'metadata': {}, 'name': 'microorgansim', 'supercategory': ''}], 'images': [{'annotated': False, 'annotating': [], 'category_ids': [], 'dataset_id': 1, 'deleted': False,... View
        all_annotations_in_this_image_dict_1 = get_all_annotaions_in_image(image, coco1_data_dict)
        all_annotations_in_this_image_dict_2 = get_all_annotaions_in_image(this_image_in_group2, coco2_data_dict)

        # record result
        # matched annotation list is each coco's annotation bbox beyond IoU threshold. suspected list is not matched, need further manual inspection.
        matched_annotations_in_this_image_list_1 = []
        suspected_annotations_in_this_image_list_1 = []
        matched_annotations_in_this_image_list_2 = []
        suspected_annotations_in_this_image_list_2 = []

        # conclusion annotation is based on group1 image, image id/file_name/path, and based on group1's category id.
        conclusion_matched_annotations_in_this_image_list = []
        conclusion_suspected_annotations_in_this_image_list = []
        conclusion_all_annotations_in_this_image_list = []

        # 1.2 calculate IoU of two group of annotation. for annotation1
        for annotation1 in all_annotations_in_this_image_dict_1['annotations']:
            is_this_annotation_matched = False
            for annotation2 in all_annotations_in_this_image_dict_2['annotations']:
                iou = cal_iou(annotation1["bbox"], annotation2["bbox"])
                if iou >= iou_threshold:
                    is_this_annotation_matched = True
            if is_this_annotation_matched:
                matched_annotations_in_this_image_list_1.append(annotation1)
                # keep the smaller area of annotation
                # green color #1A971E represent matched.
                conclusion_matched_annotation = if_annotation_in_group1_is_smaller_remain(annotation1, annotation2,
                                                                                          image_to_inherit=image,
                                                                                          annotation_category_to_inherit=annotation1,
                                                                                          set_color="#1A971E")
                if conclusion_matched_annotation is not None:
                    conclusion_matched_annotations_in_this_image_list.append(conclusion_matched_annotation)
            else:
                suspected_annotations_in_this_image_list_1.append(annotation1)
                # red color #C9151A represent suspected.
                conclusion_suspected_annotation = convert_conclusion_annotaion(annotation1, image_to_inherit=image,
                                                                               annotation_category_to_inherit=annotation1,
                                                                               set_color="#C9151A")
                if conclusion_suspected_annotation is not None:
                    conclusion_suspected_annotations_in_this_image_list.append(conclusion_suspected_annotation)

        # 1.3 calculate IoU of two group of annotation. for annotation2
        for annotation2 in all_annotations_in_this_image_dict_2['annotations']:
            is_this_annotation_matched = False
            for annotation1 in all_annotations_in_this_image_dict_1['annotations']:
                iou = cal_iou(annotation2["bbox"], annotation1["bbox"])
                if iou >= iou_threshold:
                    is_this_annotation_matched = True
            if is_this_annotation_matched:
                matched_annotations_in_this_image_list_2.append(annotation1)
                # # keep the smaller area of annotation
                # green color #1A971E represent matched.
                conclusion_matched_annotation = if_annotation_in_group1_is_smaller_remain(annotation2, annotation1,
                                                                                          image_to_inherit=image,
                                                                                          annotation_category_to_inherit=annotation1,
                                                                                          set_color="#1A971E")
                if conclusion_matched_annotation is not None:
                    conclusion_matched_annotations_in_this_image_list.append(conclusion_matched_annotation)
            else:
                suspected_annotations_in_this_image_list_2.append(annotation2)
                # red color #C9151A represent suspected.
                conclusion_suspected_annotation = convert_conclusion_annotaion(annotation2, image_to_inherit=image,
                                                                               annotation_category_to_inherit=annotation1,
                                                                               set_color="#C9151A")
                if conclusion_suspected_annotation is not None:
                    conclusion_suspected_annotations_in_this_image_list.append(conclusion_suspected_annotation)

        # 1.4 output this result to file.
        raw_file_name = image["file_name"]
        # output file format is coco .json
        parts = raw_file_name.split('.')
        file_name = parts[0] + ".json"

        ###### output result ######

        # 1.1 output group1 matched result
        matched_output_result_file_path_for_group1 = os.path.join(double_check_result_output_dir_path, "group1",
                                                                  "matched", file_name)
        matched_result_group1 = gen_new_coco_dict(all_annotations_in_this_image_dict_1,
                                                  matched_annotations_in_this_image_list_1)
        utils.json_dict_dump_to_file(matched_result_group1, matched_output_result_file_path_for_group1)

        # 1.2 output group1 suspected result
        suspected_output_result_file_path_for_group1 = os.path.join(double_check_result_output_dir_path, "group1",
                                                                    "suspected", file_name)
        suspected_result_group1 = gen_new_coco_dict(all_annotations_in_this_image_dict_1,
                                                    suspected_annotations_in_this_image_list_1)
        utils.json_dict_dump_to_file(suspected_result_group1, suspected_output_result_file_path_for_group1)

        # 2.1 output group2 matched result
        matched_output_result_file_path_for_group2 = os.path.join(double_check_result_output_dir_path, "group2",
                                                                  "matched", file_name)
        matched_result_group2 = gen_new_coco_dict(all_annotations_in_this_image_dict_2,
                                                  matched_annotations_in_this_image_list_2)
        utils.json_dict_dump_to_file(matched_result_group2, matched_output_result_file_path_for_group2)

        # 2.2 output group2 suspected result
        suspected_output_result_file_path_for_group2 = os.path.join(double_check_result_output_dir_path, "group2",
                                                                    "suspected", file_name)
        suspected_result_group2 = gen_new_coco_dict(all_annotations_in_this_image_dict_2,
                                                    suspected_annotations_in_this_image_list_2)
        utils.json_dict_dump_to_file(suspected_result_group2, suspected_output_result_file_path_for_group2)

        # 3.1 conclusion output matched
        matched_output_result_file_path_for_conclusion = os.path.join(double_check_result_output_dir_path, "conclusion",
                                                                      "matched", file_name)
        matched_result_for_conclusion = gen_new_coco_dict(all_annotations_in_this_image_dict_1,
                                                          conclusion_matched_annotations_in_this_image_list)
        utils.json_dict_dump_to_file(matched_result_for_conclusion, matched_output_result_file_path_for_conclusion)

        # 3.2 conclusion output suspected
        suspected_output_result_file_path_for_conclusion = os.path.join(double_check_result_output_dir_path,
                                                                        "conclusion",
                                                                        "suspected", file_name)
        suspected_result_for_conclusion = gen_new_coco_dict(all_annotations_in_this_image_dict_1,
                                                            conclusion_suspected_annotations_in_this_image_list)
        utils.json_dict_dump_to_file(suspected_result_for_conclusion, suspected_output_result_file_path_for_conclusion)

        # 3.3 conclusion output all
        all_output_result_file_path_for_conclusion = os.path.join(double_check_result_output_dir_path, "conclusion",
                                                                  "all", file_name)
        conclusion_all_annotations_in_this_image_list = conclusion_matched_annotations_in_this_image_list + conclusion_suspected_annotations_in_this_image_list
        reindex_id_conclusion_all_annotations_in_this_image_list = []
        reindex_annotation_id = 0
        for annotation in conclusion_all_annotations_in_this_image_list:
            reindex_annotation_id += 1
            annotation["id"] = reindex_annotation_id
            reindex_id_conclusion_all_annotations_in_this_image_list.append(annotation)
        all_result_for_conclusion = gen_new_coco_dict(all_annotations_in_this_image_dict_1,
                                                      reindex_id_conclusion_all_annotations_in_this_image_list)
        utils.json_dict_dump_to_file(all_result_for_conclusion, all_output_result_file_path_for_conclusion)

    # end for group1 images

    # 2. judge if have different images
    for image_in_group1 in coco1_data_dict["images"]:
        this_image_in_group2, is_found_image = get_this_image_in_group(image_in_group1, coco2_data_dict)
        if not is_found_image:
            # this image is never showed in group1
            # give a warning log.
            print("[WARNING] image file_name: " + image_in_group1['file_name'] + "never showed in group2.")

    for image_in_group2 in coco2_data_dict["images"]:
        this_image_in_group1, is_found_image = get_this_image_in_group(image_in_group2, coco1_data_dict)
        is_showed_in_group1 = False
        if not is_found_image:
            # this image is never showed in group2
            # give a warning log.
            print("[WARNING] image file_name: " + image_in_group2['file_name'] + "never showed in group2.")


print("finished.")

if __name__ == "__main__":
    coco_json1_file_path = 'J:\\workspace_j\\20240816-double-check\\PBCs_new-240813.json'
    # coco_json2_file_path = 'J:\\workspace_j\\20240816-double-check\\PBCs-5.json'
    coco_json2_file_path = 'J:\\workspace_j\\20240816-double-check\\eccfacb5-c740-45e8-99e0-ce91954f1e4f.json'

    double_check_two_cocos(coco_json1_file_path, coco_json2_file_path,
                           os.path.join(os.path.abspath(os.curdir), "results"), iou_threshold=0.1)
