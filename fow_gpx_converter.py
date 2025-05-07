import os
import gpxpy
import gpxpy.gpx
from GPSPhoto import gpsphoto
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()
from geopy.distance import geodesic
import argparse


def safe_join(*args):
    return os.path.normpath(os.path.join(*args))

def convert_gps_coordinates(gps_data):
    def dms_to_decimal(degree, minute, second):
        return float(degree + minute / 60 + second / 3600)

    latitude = gps_data['GPSLatitude']
    longitude = gps_data['GPSLongitude']

    latitude_decimal = dms_to_decimal(*latitude)
    longitude_decimal = dms_to_decimal(*longitude)

    if gps_data['GPSLatitudeRef'] == 'S':
        latitude_decimal = -latitude_decimal
    if gps_data['GPSLongitudeRef'] == 'W':
        longitude_decimal = -longitude_decimal

    return {'Latitude': latitude_decimal, 'Longitude': longitude_decimal, 'Altitude': gps_data['GPSAltitude'],'UTC-Time':'00:00:00.00','Date': '01/193/2000' }


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif().get_ifd(0x8825)


def get_geotagging(exif):
    geo_tagging_info = {}
    if not exif:
        raise ValueError("No EXIF metadata found")
    else:
        gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                    'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                    'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                    'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
                    'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance',
                    'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']

        for k, v in exif.items():
            try:
                #geo_tagging_info[gps_keys[k]] = str(v)
                geo_tagging_info[gps_keys[k]] = v
                #pass
            except IndexError:
                pass
        return geo_tagging_info

def save_waypoints_to_gpx(directory):
    # Create GPX object
    gpx = gpxpy.gpx.GPX()

    # Supported file extensions
    #extensions = ['.jpg', '.jpeg', '.mp4']
    extensions = ['.jpg', '.jpeg']

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Check if file has a supported extension
        if any(filename.lower().endswith(ext) for ext in extensions):
            # Get full file path
            file_path = safe_join(directory, filename)

            try:
                # Get GPS data from image
                
                gps_data = gpsphoto.getGPSData(file_path)
                #print(f"GPS data found in {filename}")

                # Create a new waypoint
                waypoint = gpxpy.gpx.GPXWaypoint(latitude=gps_data['Latitude'], longitude=gps_data['Longitude'])

                # Add waypoint to GPX file
                gpx.waypoints.append(waypoint)
                
            except:
                aa=1+1
                #print(f"No GPS data found in {filename}")

    # Save GPX file in the same directory
    with open(safe_join(directory, 'waypoints.gpx'), 'w') as file:
        file.write(gpx.to_xml())

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif().get_ifd(0x8825)


def get_geotagging(exif):
    geo_tagging_info = {}
    if not exif:
        raise ValueError("No EXIF metadata found")
    else:
        gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                    'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                    'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                    'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
                    'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance',
                    'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']

        for k, v in exif.items():
            try:
                #geo_tagging_info[gps_keys[k]] = str(v)
                geo_tagging_info[gps_keys[k]] = v
                #pass
            except IndexError:
                pass
        return geo_tagging_info


def save_HEIC_waypoints_to_gpx(directory):
    # Create GPX object
    gpx = gpxpy.gpx.GPX()

    # Supported file extensions
    extensions = [ '.heic']

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Check if file has a supported extension
        if any(filename.lower().endswith(ext) for ext in extensions):
            # Get full file path
            file_path = safe_join(directory, filename)

            try:
                # Get GPS data from image
                
                #gps_data = gpsphoto.getGPSData(file_path)
                image_info = get_exif(file_path)
                results = get_geotagging(image_info)
                #print(results)
                gps_data = convert_gps_coordinates(results)
                #print(f"GPS data found in {filename}")
                #print(gps_data)
                

                # Create a new waypoint
                waypoint = gpxpy.gpx.GPXWaypoint(latitude=gps_data['Latitude'], longitude=gps_data['Longitude'])
                #print(waypoint)

                # Add waypoint to GPX file
                gpx.waypoints.append(waypoint)
                
            except:
                aa=1+1
                #print(f"No GPS data found in {filename}")

    # Save GPX file in the same directory
    with open(safe_join(directory, 'waypoints_HEIC.gpx'), 'w') as file:
        file.write(gpx.to_xml())

def process_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        #print(dirpath)
        save_waypoints_to_gpx(dirpath)
        save_HEIC_waypoints_to_gpx(dirpath)

def save_all_waypoints(root_dir, output_dir):
    # Create an empty list to store waypoints
    waypoints = []

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check each file in the directory
        for filename in filenames:
            # If the file is a GPX file
            if filename.endswith('.gpx'):
                # Open the file
                with open(safe_join(dirpath, filename), 'r') as gpx_file:
                    # Parse the file with gpxpy
                    gpx = gpxpy.parse(gpx_file)
                    # Add the waypoints to the list
                    waypoints.extend(gpx.waypoints)

    # Create a new GPX object
    gpx = gpxpy.gpx.GPX()

    # Add the waypoints to the new GPX object
    for waypoint in waypoints:
        gpx.waypoints.append(waypoint)

    # Write the new GPX object to a file in the output directory
    with open(safe_join(output_dir, 'all_waypoints.gpx'), 'w') as output_file:
        output_file.write(gpx.to_xml())



def create_tracks_from_waypoints(input_file_path, output_file_path):
    # Parse the original GPX file
    with open(input_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Create a new GPX file
    new_gpx = gpxpy.gpx.GPX()

    # For each waypoint in the original file
    for waypoint in gpx.waypoints:
        # Create a new waypoint 1 meter to the north
        new_location = geodesic(meters=1).destination((waypoint.latitude, waypoint.longitude), 0)
        new_waypoint = gpxpy.gpx.GPXWaypoint(latitude=new_location.latitude, longitude=new_location.longitude)

        # Create a track connecting the original waypoint and the new waypoint
        gpx_track = gpxpy.gpx.GPXTrack()
        new_gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=waypoint.latitude, longitude=waypoint.longitude))
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=new_waypoint.latitude, longitude=new_waypoint.longitude))

    # Save the new GPX file
    with open(output_file_path, 'w') as output_file:
        output_file.write(new_gpx.to_xml())


def delete_waypoints_files(folder_path):
    # Loop through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file name matches the target names
            if file == 'waypoints_HEIC.gpx' or file == 'waypoints.gpx':
                file_path = safe_join(root, file)
                os.remove(file_path)
                #print(f"Deleted: {file_path}")

def images_to_tracks(root_dir, output_dir_input=''):
    if output_dir_input == '':
        output_dir = os.getcwd()
    else:
        output_dir = output_dir_input

    process_directories(root_dir)  # Generate gpx files for each subfolder under root_dir.
    save_all_waypoints(root_dir, output_dir)  # Gather all waypoints into a single GPX file.

    all_waypoints_path = safe_join(output_dir, 'all_waypoints.gpx')
    tracks_to_import_path = safe_join(output_dir, 'tracks_to_import.gpx') #use safe_join()

    create_tracks_from_waypoints(all_waypoints_path, tracks_to_import_path)  # Convert waypoints to tracks.
    delete_waypoints_files(root_dir)  # Remove temporary files
    os.remove(all_waypoints_path)  # Remove temporary file

    print('GPX tracks saved to:', tracks_to_import_path, '. Import it to your Fog of World')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert image GPS data to GPX tracks for Fog of World.")
    parser.add_argument('-i', '--input', required=True, help="Path to the folder containing images.")
    parser.add_argument('-o', '--output',default='', help="Path to the folder where the GPX file will be saved. Defaults to the current working directory.")
    args = parser.parse_args()
    images_to_tracks(args.input, args.output)
