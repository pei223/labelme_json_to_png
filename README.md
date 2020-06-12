# labelme_json_to_png
## Setup
```
pip install -r requirements.txt
```

## Usage
```
python labelme_json_to_png.py <Labelme JSON file directory.> -o=<output directory> -label_file=<label file>
```

### Label file format(Example)
Exclude background.
```
aeroplane
bicycle
bird
...
```