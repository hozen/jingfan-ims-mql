#!/bin/bash

# Create the video using ffmpeg's text overlay capabilities
# This uses a simpler approach that should work on macOS

echo "Creating professional NH6000sc intro video..."

# Create the video with animated text using ffmpeg's internal text capabilities
ffmpeg -y \
  -f lavfi -i color=color=#0055aa:s=1920x1080:d=10 \
  -i nh6000sc_voiceover_10s.mp3 \
  -vf \
"drawtext=text='Hach NH6000sc 氨氮分析儀':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2-200:enable='between(t,0,10)',
 drawtext=text='精準氨氮監測':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-50:enable='between(t,1.5,10)',
 drawtext=text='實時數據采集':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2+20:enable='between(t,3,10)',
 drawtext=text='輕鬆系統集成':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2+90:enable='between(t,4.5,10)',
 drawtext=text='您的水質分析夥伴':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2+160:enable='between(t,6,10)',
 drawtext=text='hach.com':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=h-100:enable='between(t,8,10)'" \
  -c:v libx264 -c:a aac -shortest \
  nh6000sc_final_video.mp4

echo "Testing audio output..."
afplay nh6000sc_voiceover_10s.mp3

echo "Video properties:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 nh6000sc_final_video.mp4

echo "Checking video file..."
ls -lh nh6000sc_final_video.mp4