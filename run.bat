@echo off
rem turning off the echo function of the command line, that is, not showing the input commands and output results

set /p video_path="Please enter the video file path: "
rem setting a variable video_path, whose value is the string entered by the user in the command line, the content in quotation marks is the prompt information

if not exist "%video_path%" (
    echo File does not exist, please check if the path is correct.
    pause
    exit
)
rem judging whether the file corresponding to video_path exists, if NOT, display an error message and exit

set tmp_path=%~dp0\tmp
rem creating a tmp path storing frames of the input video
if not exist "%tmp_path%" (
    mkdir "%tmp_path%"
) else (
    del /q /s /f "%tmp_path%\*"
)

rem extracting frames
ffmpeg.exe -i "%video_path%" -qscale:v 1 "%tmp_path%\%%d.jpg"

pause
