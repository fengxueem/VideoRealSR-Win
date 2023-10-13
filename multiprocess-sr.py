import os
import subprocess
import sys
import multiprocessing

# Get the video file path and max process number from CLI
if len(sys.argv) < 3:
    print("Please set video path and max number of process")
    exit()
video_path = sys.argv[1]
max_proc = int(sys.argv[2])

# Check if the file exists, if not, display an error message and exit
if not os.path.exists(video_path):
    print("File does not exist, please check if the path is correct.")
    input("Press any key to exit.")
    exit()

tmp_path = os.path.join(os.path.dirname(__file__), "tmp")
sr_tmp_path = os.path.join(os.path.dirname(__file__), "tmp_sr")

def prepare():
    # Create a temporary directory to store the video frames
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    else:
        # Delete all files in the temporary directory
        for file in os.listdir(tmp_path):
            os.remove(os.path.join(tmp_path, file))

    # Create a temporary directory to store the super-resolution video frames
    if not os.path.exists(sr_tmp_path):
        os.mkdir(sr_tmp_path)
    else:
        # Delete all files in the temporary directory
        for file in os.listdir(sr_tmp_path):
            os.remove(os.path.join(sr_tmp_path, file))
    return tmp_path, sr_tmp_path

def get_fps(file):
    # create a command list with ffprobe and its options
    command = ["ffprobe", "-v", "0", "-of", "csv=p=0", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", file]
    # run the command and capture its output
    output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()
    # parse the output to get the frame rate as a fraction
    frame_rate = output.strip()
    return round(eval(frame_rate))

# Perform super-resolution on video frames
def run_sr_command(file):
    pic_path = os.path.join(tmp_path, file)
    pic_name = os.path.splitext(file)[0]
    sr_pic_path = os.path.join(sr_tmp_path, pic_name + ".jpg")
    subprocess.run(["realsr-ncnn-vulkan.exe", "-i", pic_path, "-o", sr_pic_path])
    return pic_path

if __name__ == '__main__':
    # Prepare
    prepare()
    fps = get_fps(video_path)
    
    # Extract video frames
    subprocess.run(["ffmpeg.exe", "-i", video_path, "-qscale:v", "1", os.path.join(tmp_path, "%d.jpg")], check=True)
    file_list = os.listdir(tmp_path)

    # Perform super-resolution on frames
    pool = multiprocessing.Pool(max_proc)
    for file in pool.map(run_sr_command, file_list):
        print(f"Finished: {file}")
    
    # Generate output mp4
    subprocess.run(["ffmpeg.exe", "-framerate", str(fps), "-i", os.path.join(sr_tmp_path, "%d.jpg"), "-c:v", "libx265", "-crf", "28", "-pix_fmt", "yuv420p", "output.mp4"], check=True)

