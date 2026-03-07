#!/bin/bash

# Create a black video background with text overlays
ffmpeg -y \
  -f lavfi -i color=color=blue:s=1920x1080:d=10 \
  -i nh6000sc_voiceover_10s.mp3 \
  -vf \
"drawtext=fontfile=/System/Library/Fonts/Arial.ttf:text='Hach NH6000sc 氨氮分析儀':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2-150:enable='between(t,0,10)',
 drawtext=fontfile=/System/Library/Fonts/Arial.ttf:text='精準氨氮監測':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-50:enable='between(t,1.5,10)',
 drawtext=fontfile=/System/Library/Fonts/Arial.ttf:text='實時數據采集':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2+20:enable='between(t,3,10)',
 drawtext=fontfile=/System/Library/Fonts/Arial.ttf:text='輕鬆系統集成':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2+90:enable='between(t,4.5,10)',
 drawtext=fontfile=/System/Library/Fonts/Arial.ttf:text='您的水質分析夥伴':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2+160:enable='between(t,6,10)',
 drawtext=fontfile=/System/Library/Fonts/Arial.ttf:text='hach.com':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=h-100:enable='between(t,8,10)'" \
  -c:v libx264 -c:a aac -shortest \
  nh6000sc_final_video.mp4

echo "Video created! Testing audio..."
afplay nh6000sc_voiceover_10s.mp3

echo "Video properties:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 nh6000sc_final_video.mp4