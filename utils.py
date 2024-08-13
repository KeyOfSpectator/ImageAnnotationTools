import json
import os


def file_json_loads(input_file_path):
    file_obj=open(input_file_path, encoding='utf-8')

    python_data_dict=json.load(file_obj)
    #print(python_data_dict)
    return python_data_dict

def json_dict_dump_to_file(json_dict, output_file_path):
    dir_path = os.path.dirname(os.path.abspath(output_file_path))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_obj=open(output_file_path, mode="w", encoding='utf-8')
    json.dump(json_dict, file_obj, ensure_ascii=False)
    file_obj.close()
