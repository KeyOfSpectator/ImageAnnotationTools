
import os

import utils


def merge_coco(input_dir_path, output_file_path, metadata_file_path):
    """
    This tool file help to merge each one-image coco file to one dataset's coco file.
    :param input_dir_path: filepath of the input dir, will merge the files in input dir, each file is a coco json file for one image.

    :param output_file_path: merge coco json result will be saved in this file.

    :param: metadata_file_path: the output file's image id and category id will be the same as the metadata file, mapping the same image filename and category name.
    """
    ret_coco_dict = {}
    metadata_dict = utils.file_json_loads(metadata_file_path)

    ret_coco_dict['images'] = metadata_dict['images']
    ret_coco_dict['categories'] = metadata_dict['categories']
    ret_coco_dict['annotations'] = []

    reindex_annotation_id = 0

    for dirpath, dirnames, filenames in os.walk(input_dir_path):
        for filename in filenames:
            if filename.endswith('.json'):
                # print(os.path.join(dirpath, filename))
                abs_filepath = os.path.join(dirpath, filename)
                # the image dict need to be merged.
                image_dict = utils.file_json_loads(abs_filepath)

                for meta_image in metadata_dict['images']:
                    if meta_image['file_name'] == image_dict['images'][0]['file_name']:

                        # for each annotation
                        for annotation in image_dict['annotations']:
                            reindex_annotation_id += 1
                            annotation['image_id'] = meta_image['id']
                            annotation['id'] = reindex_annotation_id
                            # find category id
                            category_name = "unknown_category_name"
                            for category in image_dict['categories']:
                                if category['id'] == annotation['category_id']:
                                    category_name = category['name']
                                    break
                            if category_name == "unknown_category_name":
                                print("not found category in this image coco file, image file: ", abs_filepath, " annotation: ", annotation)

                            not_found_category = True
                            for metadata_category in metadata_dict['categories']:
                                if metadata_category['name'] == category_name:
                                    annotation['category_id'] = metadata_category['id']
                                    not_found_category = False
                                    break
                            if not_found_category:
                                print("not found category:", category_name, " image file: ", abs_filepath, " annotation: ", annotation)

                            # append annotation
                            ret_coco_dict['annotations'].append(annotation)


        # end every image file
        utils.json_dict_dump_to_file(ret_coco_dict, output_file_path)
        print("end all.")

if __name__ == '__main__':

    # will merge the files in input dir, each file is a coco json file for one image.
    input_dir_path = "J:\\workspace_j\\20240819\\splited_annotator2"

    # merge coco json result will be saved in this file
    output_file = "J:\\workspace_j\\20240819\\merged_annotator1\\PCBs_annotator2.json"

    # the output file's image id and category id will be the same as the metadata file, mapping the same image filename and category name.
    coco_metadata_json_file = "J:\\workspace_j\\20240819\\PBCs_new-19-export-backup-20240919.json"

    merge_coco(input_dir_path, output_file, coco_metadata_json_file)

