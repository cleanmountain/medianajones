from pymediainfo import MediaInfo
import json


# MODIFY THESE PARAMETERS
ALL_FILES = []  # e.g. ["swing-video.mp4", "fireworks.mp4", "berlin-2088.mp4"]
HIDE_NOT_IN_COMMONS = False


def load_video(file):
    media_info = MediaInfo.parse(file, output="JSON")
    
    data = json.loads(media_info)["media"]["track"]
    
    general = [f"{key}: {value}" for [key, value] in data[0].items()]
    video = [f"{key}: {value}" for [key, value] in data[1].items()]
    audio = [f"{key}: {value}" for [key, value] in data[2].items()]
    
    return general, video, audio


def find_commons(number_of_files, general, video, audio):
    
    # font colors
    okblue = "\033[94m"
    failred = "\033[91m"
    
    if HIDE_NOT_IN_COMMONS: 
        # ignore not-in-commons
        general_in_common = [okblue + info for info in general if general[info] == number_of_files]
        video_in_common = [okblue + info for info in video if video[info] == number_of_files]
        audio_in_common = [okblue + info for info in audio if audio[info] == number_of_files]
    else: 
        # color in-commons blue and not-in-commons red
        general_in_common = [okblue + info if general[info] == number_of_files else failred + info for info in general]
        video_in_common = [okblue + info if video[info] == number_of_files else failred + info for info in video]
        audio_in_common = [okblue + info if audio[info] == number_of_files else failred + info for info in audio]

    print_result(general_in_common, video_in_common, audio_in_common)


def print_result(general, video, audio):
    # font color
    header = "\033[95m"

    print("\n")
    print(header + ">>>> GENERAL <<<<")
    for line in general:
        print(line)
    print("\n\n")

    print(header + ">>>> VIDEO <<<<")
    for line in video:
        print(line)
    print("\n\n")

    print(header + ">>>> AUDIO <<<<")
    for line in audio:
        print(line)


def count_occurences():
    general_info_counter = {}
    video_info_counter = {}
    audio_info_counter = {}

    NUM_OF_FILES = len(ALL_FILES)

    for file in ALL_FILES:
        general, video, audio = load_video(file)
        
        for info in general:
            if info in general_info_counter:
                general_info_counter[info] += 1
            else:
                general_info_counter[info] = 1
        
        for info in video:
            if info in video_info_counter:
                video_info_counter[info] += 1
            else:
                video_info_counter[info] = 1

        for info in audio:
            if info in audio_info_counter:
                audio_info_counter[info] += 1
            else:
                audio_info_counter[info] = 1
    
    find_commons(NUM_OF_FILES, general_info_counter, video_info_counter, audio_info_counter)


count_occurences()
