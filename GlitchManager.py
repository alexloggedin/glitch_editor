import os
import json
import subprocess
import argparse
import string

FF_PATH = os.path.dirname(os.path.realpath(__file__)) + "/ffglitch/"

FFEDIT = FF_PATH+"ffedit"
FFGAC = FF_PATH+"ffgac"

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
WRK = os.path.join(WORKING_DIR, "wrk")

# Base .mpg file that glitch sequences are applied to
WRK_BASE_PATH = "wrk/base.mpg"

# Glitched .mpg that has been glitched
WRK_GLITCH_PATH = "wrk/glitched.mpg"

class GlitchManager:
    def __init__(self):

        self.file_path = ""
        self.output_file_path = "wrk/output.mp4" # If no output path/file type selected just output to wrk folder
        self.glitches = []
        self.video_mosh = True
        self.frame_count = 0
        self.frame_rate = 0
        self.script_databse = PopulateGlitchDatabase()

        if (not os.path.exists(WRK)):
            os.mkdir(WRK)

    def display_database(self):
        return self.script_databse

    def set_input_file_path(self, fp):
        self.file_path = fp
    
    def set_output_file_path(self, fp):
        self.output_file_path = fp
    
    def get_frame_data(self):
        command = f"ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate,nb_frames -of default=noprint_wrappers=1:nokey=1 {self.file_path}"
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
            output = result.stdout.strip().split('\n')
        
        # Parse frame rate
            frame_rate_fraction = output[0]
            numerator, denominator = map(int, frame_rate_fraction.split('/'))
            self.frame_rate = numerator / denominator
        
        # Parse frame count
            self.frame_count = int(output[1])
        
        except subprocess.CalledProcessError as e:
            print(f"Error running ffprobe command: {e}")
        except ValueError as e:
            print(f"Error parsing output: {e}")

    def preprocess(self):

        # Create mpg file
        prep_command = [
            FFGAC,
            '-i', self.file_path,
            '-an',
            '-mpv_flags', '+nopimb+forcemv',
            '-qscale:v', '0',
            '-g', 'max',
            '-sc_threshold', 'max',
            '-vcodec', 'mpeg2video',
            '-f', 'rawvideo',
            '-y', WRK_BASE_PATH
        ]
        print(prep_command)
        
        subprocess.call(prep_command)

        self.get_frame_data()
    
    def bake(self):
        ## maybe use ffmpeg for output
        bake_command = [
            "ffmpeg", 
            "-i", WRK_BASE_PATH,
            "-y", WRK_GLITCH_PATH
        ]

        subprocess.call(bake_command)

    def glitch_video(self):
        # Dunp GlitchList into JSON File
        with open('js/GlitchSequence.js', 'w') as file:
            file.write("export default \n")
            json.dump(self.glitches, file, indent=4)
        
        # Run Script Glitch
        video_command = [
            FFEDIT,
            '-i', WRK_BASE_PATH, 
            '-f', 'mv', 
            '-s', 'js/VideoGlitcher.js',
            '-o', WRK_GLITCH_PATH
        ]

        print(video_command)
        subprocess.call(video_command)

    def add_glitch(self, index, name, start, end, params = None):

        #validate glitch
        if name not in self.script_databse:
            return None

        new_glitch = {
            "index": index,
            "name": name,
            "start": start,
            "end": end,
            "params": params
        }
        self.glitches.append(new_glitch)
        return new_glitch
    
    def get_glitch(self, index):
        for glitch in self.glitches:
            if glitch["index"] == index:
                return glitch
        return None  # Or raise an exception if preferred

    def update_glitch(self, index, name=None, start=None, end=None):
        glitch = self.get_glitch(index)
        if glitch:
            if name is not None:
                glitch["name"] = name
            if start is not None:
                glitch["start"] = start
            if end is not None:
                glitch["end"] = end
        else:
            raise ValueError("Glitch with index {} not found.".format(index))

    def delete_glitch(self, index):
        self.glitches = [glitch for glitch in self.glitches if glitch["index"] != index]

    def display_glitches(self):
        for glitch in self.glitches:
            print(glitch)
        return self.glitches

def PopulateGlitchDatabase():

    JSPATH = os.path.dirname(os.path.realpath(__file__)) + "/js"
    SCRIPT_PATH = JSPATH + "/scripts"
    SCRIPT_DATABASE = JSPATH + "/ScriptDatabase.js"

    import_template = string.Template("import { glitch_frame as $name } from './scripts/$filename' \n")
    export_template = string.Template('"$name": $name, \n')

    if (not os.path.exists(SCRIPT_PATH)):
        print("Script Database does not exist...")
        return

    file_dict = {}

    print("Loading Glitches...")

    for root, dirs, files in os.walk(SCRIPT_PATH):
        # Using the root path as the key and file names as a list of values
        relative_root = os.path.relpath(root, SCRIPT_PATH)

        file_dict[relative_root] = [(os.path.splitext(file)[0], file) for file in files]

    script_list = []

    with open(SCRIPT_DATABASE, 'w') as f:
        for files in file_dict.items():
        
            # Loop To Write Imports
            for file in files:
                f.write(import_template.safe_substitute({
                    "name": file[0],
                    "filename": file[1]
                }))
            
            f.write("\nvar SCRIPTS = { \n")

            for file in files:
                print(f"Adding Glitch: {file[0]}")
                script_list.append(file[0])
                f.write(export_template.safe_substitute({
                    "name": file[0]
                }))
            
            f.write("} \n \nexport { SCRIPTS } ")

    print("Glitches Loaded.")

    return script_list
