
from general_json2yolo import convert_coco_json

## REF https://github.com/ultralytics/JSON2YOLO?tab=readme-ov-file


if __name__ == "__main__":

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
