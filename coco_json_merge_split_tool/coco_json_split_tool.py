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

    input_file_path="C:\\Users\\KeyOfSpectator\\Desktop\\Lotus\\xxxxxx-double-check\\PBCs-annotation-1.json"
    output_dir_path = 'J:\\workspace_j\\xxxxxx\\splited_export_dir\\'

    split_coco(input_file_path, output_dir_path)