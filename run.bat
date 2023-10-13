@echo off

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

set sr_tmp_path=%~dp0\tmp_sr
rem creating a tmp path storing frames of the input video
if not exist "%sr_tmp_path%" (
    mkdir "%sr_tmp_path%"
) else (
    del /q /s /f "%sr_tmp_path%\*"
)

rem extracting frames
ffmpeg.exe -i "%video_path%" -qscale:v 1 "%tmp_path%\%%d.jpg"

rem super-resolute frames
setlocal enabledelayedexpansion
for %%f in ("%tmp_path%\*.jpg") do (
    set pic_path=%%~ff
    set pic_name=%%~nf
    realsr-ncnn-vulkan.exe -i !pic_path! -o "!sr_tmp_path!\!pic_name!.jpg"
)

pause
