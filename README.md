# Exif-GPS-to-GPX
3rd party Fog of World* toolbox


## Image GPS to GPX Converter

This Python tool extracts GPS data from images (JPG, HEIC and others), converts them into GPX tracks, and prepares them for import into the **Fog of World** app.

## Features

- Supports JPG and HEIC image formats.
- Extracts GPS metadata from images.
- Converts GPS data into GPX waypoints.
- Combines waypoints into GPX tracks.
- Outputs a GPX file ready for import into Fog of World.
- Command-line interface for easy batch processing.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/garfieldw33/Exif-GPS-to-GPX.git
   cd Exif-GPS-to-GPX
   ```

2. Install the required Python packages:
   ```bash
   pip install gpxpy GPSPhoto pillow_heif geopy
   ```

## Usage

If preferred, you may open the Jupyter Notebook to review and run the scripts:
```bash
FoW_gpx_tool.ipynb
```

or, run the script from the terminal:

```bash
python fow_gpx_converter.py -i <input_folder> [-o <output_folder>]
```

### Arguments

- `-i`, `--input`: Path to the folder containing images (required).
- `-o`, `--output`: Path to the folder where the GPX file will be saved (optional). Defaults to the current working directory.

### Example Commands

```bash
# Save GPX to a specific folder
python fow_gpx_converter.py -i test_images -o waypoints

# Save GPX to the current directory
python fow_gpx_converter.py -i test_images
```

After running, the script will generate a file named:
```
tracks_to_import.gpx
```
You can import this file into the **Fog of World** app to visualize your travels.

## Output

- `tracks_to_import.gpx`: The final GPX file containing track segments based on image locations.

## License

This project is licensed under the MIT License.

