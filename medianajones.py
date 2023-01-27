from pymediainfo import MediaInfo
import json


# MODIFY THESE PARAMETERS
ALL_FILES = ["swing-rain-new-audio.mp4", "tree-rain.mp4"]
HIDE_NOT_IN_COMMONS = False


class bcolors:
    HEADER = '\033[95m'
    ENDC = '\033[0m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    
    #not in use
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def load_video(file):
    USUAL_TRACKS = ["general", "video", "audio"]
    media_info = MediaInfo.parse(file, output="JSON")
    data = json.loads(media_info)["media"]["track"]
    
    tracks_data = []

    for track in data:
        track_data = {}
        track_type = track["@type"].lower().strip()
        track_type_id = track["StreamKindID"]
        
        if track_type not in USUAL_TRACKS:
            print(f"Unusual track type {track_type} found")
        
        media_info_for_track = {}

        for mediainfo in track:
            media_info_for_track[mediainfo] = track[mediainfo]

        track_data["type"] = track_type  # e.g. video
        track_data["track_type_id"] = track_type_id  # e.g. 0
        track_data["id"] = track_type + "_" + track_type_id  # e.g. video_0
        track_data["data"] = media_info_for_track  # all mediainfo for the track

        tracks_data.append(track_data)    

    
    return tracks_data


def count_occurences():
    all_videos_data = {}
    longest_key_word = 0

    for file in ALL_FILES:
        video_tracks = load_video(file)  # e.g. [{'type': 'audio', 'track_type_id': '1', 'id': 'audio_1', 'data': {'@type': 'Audio', '@typeorder': '2',]
        
        for track in video_tracks:
            track_type = track["type"]
            for key in track["data"]:

                if key == "extra":  # can't decide what to do with this rn (it's a dictionary of extra details)
                    continue
                
                if len(key) > longest_key_word:
                    longest_key_word = len(key)

                if not track_type in all_videos_data:
                    all_videos_data[track_type] = {}
                
                track_type_data = all_videos_data[track_type]
                
                if not key in track_type_data:
                    """" INITIALIZE DICT STRUCTURE """
                    track_type_data[key] = {"tracks_with_key": 0, "videos": set(), "entries": set()}

                if not file in track_type_data[key]["videos"]:
                    track_type_data[key]["videos"].add(file)
                
                track_type_data[key]["tracks_with_key"] += 1
                track_type_data[key]["entries"].add(track["data"][key])

    print_result(all_videos_data, longest_key_word)


def print_result(all_videos_data, longest_key_word):
    # Criteria for being a common: len(entries) == 1 && len(videos) == len(ALL_FILES)
    # ...since it means that all videos have added their value to the respective key, and that all the values were identical (entries is a set)
    
    for track_type in all_videos_data:

        """PRINT HEADER"""
        print(f"\n\n{bcolors.HEADER}{(track_type.upper() + ' • ')*4 + track_type.upper()}{bcolors.ENDC}")
        
        for key in all_videos_data[track_type]:
            
            entries = all_videos_data[track_type][key]["entries"]
            videos = all_videos_data[track_type][key]["videos"]
            
            
            if len(entries) == 1 and len(videos) == len(ALL_FILES):
                """PRINT IN COMMONS"""
                print(bcolors.OKGREEN + f"{key : <{longest_key_word}s}: {entries}")
            elif not HIDE_NOT_IN_COMMONS:
                """PRINT NOT IN COMMONS"""
                print(bcolors.FAIL + f"{key : <{longest_key_word}s}: {entries}")
        

count_occurences()