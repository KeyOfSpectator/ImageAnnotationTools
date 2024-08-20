import utils

def split_coco(input_file_path, output_dir_path):

    data_dict = utils.file_json_loads(input_file_path)

    for image in data_dict["images"]:
        #print(image)
        this_image_dict = {}
        this_image_dict["images"] = [image]
        this_image_dict["categories"] = data_dict["categories"]
        this_image_dict["annotations"] = []

        for annotation in data_dict["annotations"]:
            if annotation["image_id"] == image["id"]:
                #print(annotation)
                this_image_dict["annotations"].append(annotation)
                #print(this_image_dict)

        #print(this_image_dict)

        #output json
        raw_file_name=image["file_name"]

        # output file is .json
        parts=raw_file_name.split('.')
        file_name=parts[0]+".json"

        output_result_file_path=output_dir_path + file_name
        utils.json_dict_dump_to_file(this_image_dict, output_result_file_path)
        print("file: " + raw_file_name + " annotation count: " + str(len(this_image_dict["annotations"])))

    print("finished all. output dir path: " + output_dir_path)


if __name__ == '__main__':

    # 20240610
    # input_file_path='C:\\Users\\KeyOfSpectator\\Desktop\\Lotus\\20240610-export-coco-results\\PBCs-5.json'
    # output_dir_path='C:\\Users\\KeyOfSpectator\\Desktop\\Lotus\\20240610-export-coco-results\\results_20240610\\'

    # 20240804
    # input_file_path='J:\\workspace_j\\20240812-yolo10\\lotus_PBCs_new_20240804_one_cal\\coco-1723429856.0694387-20240804-1.json'
    # output_dir_path='J:\\workspace_j\\20240812-yolo10\\lotus_PBCs_new_20240804_one_cal\\labels\\all-coco\\'

    # 20240819
    input_file_path="C:\\Users\\KeyOfSpectator\\Desktop\\Lotus\\20240819-double-check\\PBCs-初稿标注.json"
    output_dir_path = 'J:\\workspace_j\\20240819\\splited_微生物目标检测导出240819\\'

    split_coco(input_file_path, output_dir_path)