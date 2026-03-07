#!/bin/bash

# Create a video with fading text using ffmpeg

# First create individual text images
echo "Creating text images..."

# Main title text
convert -size 1920x200 -background transparent -fill white -pointsize 72 -gravity center label:"Hach NH6000sc 氨氮分析儀" title.png

# Feature texts
convert -size 1920x100 -background transparent -fill white -pointsize 48 -gravity center label:"精準氨氮監測" feature1.png
convert -size 1920x100 -background transparent -fill white -pointsize 48 -gravity center label:"實時數據采集" feature2.png
convert -size 1920x100 -background transparent -fill white -pointsize 48 -gravity center label:"輕鬆系統集成" feature3.png
convert -size 1920x100 -background transparent -fill white -pointsize 48 -gravity center label:"您的水質分析夥伴" feature4.png

# Website text
convert -size 1920x100 -background transparent -fill white -pointsize 60 -gravity center label:"hach.com" website.png

# Create video with fading text overlay
echo "Creating video..."
ffmpeg -y \
  -f lavfi -i color=color=blue:s=1920x1080:d=10 \
  -i nh6000sc_voiceover_10s.mp3 \
  -i title.png \
  -i feature1.png \
  -i feature2.png \
  -i feature3.png \
  -i feature4.png \
  -i website.png \
  -filter_complex \
"[0][2] overlay=x=(W-w)/2:y=(H-h)/2-200:enable='between(t,0,10)' [v0];
 [v0][3] overlay=x=(W-w)/2:y=(H-h)/2-50:enable='between(t,1.5,10)' [v1];
 [v1][4] overlay=x=(W-w)/2:y=(H-h)/2+20:enable='between(t,3,10)' [v2];
 [v2][5] overlay=x=(W-w)/2:y=(H-h)/2+90:enable='between(t,4.5,10)' [v3];
 [v3][6] overlay=x=(W-w)/2:y=(H-h)/2+160:enable='between(t,6,10)' [v4];
 [v4][7] overlay=x=(W-w)/2:y=H-100:enable='between(t,8,10)' [v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -c:a aac -shortest \
  nh6000sc_final_video.mp4

echo "Cleaning up temporary files..."
rm title.png feature1.png feature2.png feature3.png feature4.png website.png

echo "Video created! Testing audio..."
afplay nh6000sc_voiceover_10s.mp3

echo "Video properties:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 nh6000sc_final_video.mp4