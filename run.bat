@echo off

set /p video_path="Please enter the video file path: "
set /p num_proc="Please enter the max number of processes in parallel: "
rem setting a variable video_path, whose value is the string entered by the user in the command line, the content in quotation marks is the prompt information

python multiprocess-sr.py "%video_path%" "%num_proc%"