from pathlib import Path
import subprocess
import shutil
import argparse
import tqdm
from PIL import Image
import numpy as np

TEMP_DIR = "temp"

parser = argparse.ArgumentParser()
parser.add_argument("json_dir", help="JSON files directory.")
parser.add_argument("-o", required=True, help="Output directory.")
parser.add_argument("-label_file", required=True, help="Label name file.")

args = parser.parse_args()

json_dir_path = Path(args.json_dir)
out_dir_path = Path(args.o)
label_file_path = Path(args.label_file)

assert json_dir_path.exists(), "JSON directory is not exist."
assert out_dir_path.exists(), "Output directory is not exist."
assert label_file_path.exists(), "Label file is not exist."

# Preprocessing.
correct_label_dict = {}
with open(str(label_file_path), "r") as file:
    for i, line in enumerate(file):
        correct_label_dict[line.replace("\n", "")] = i + 1
temp_dir_path = out_dir_path.joinpath(TEMP_DIR)
if not temp_dir_path.exists():
    temp_dir_path.mkdir()

# Batch process Converting json to png.
for json_file_path in tqdm.tqdm(list(json_dir_path.glob("*.json"))):
    # Execute "labelme_json_to_dataset".
    subprocess.run(["labelme_json_to_dataset", str(json_file_path), "-o", str(temp_dir_path)], stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, text=True)

    image: Image.Image = Image.open(str(temp_dir_path.joinpath("label.png")))
    origin_color_palette = image.getpalette()

    image_array = np.array(image)
    # Fix label.
    with open(str(temp_dir_path.joinpath("label_names.txt")), "r") as label_file:
        for label_num, label_name in enumerate(label_file):
            label_name = label_name.replace("\n", "")
            if label_name == "_background_":
                continue
            correct_label_num = correct_label_dict[label_name]
            image_array[image_array == label_num] = correct_label_num
    new_image = Image.fromarray(image_array)
    new_image.convert("P")
    new_image.putpalette(origin_color_palette)
    new_image.save(str(out_dir_path.joinpath(json_file_path.name).with_suffix(".png")))

# Post processing.
if temp_dir_path.exists():
    shutil.rmtree(str(temp_dir_path))

print("Conversion is finished.")
