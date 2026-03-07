#!/bin/bash

# Create a professional-looking final video

# Method 1: Try to use drawtext if available with simpler syntax
if ffmpeg -f lavfi -i color=color=blue:s=100x100:d=1 -vf "drawtext=text='Test':x=0:y=0" -f null - 2>&1 | grep -q "drawtext"; then
    echo "drawtext filter is available"
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
      -c:v libx264 -c:a aac \
      nh6000sc_professional_video.mp4
else
    echo "drawtext filter not available - creating simple video"
    # Just copy the video with our audio
    ffmpeg -y -i nh6000sc_base_video.mp4 -i nh6000sc_voiceover_10s.mp3 -c copy -map 0:v -map 1:a nh6000sc_professional_video.mp4
fi

# Test the audio
echo "Testing audio output..."
afplay nh6000sc_voiceover_10s.mp3

# Verify the resultecho "Final video properties:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 nh6000sc_professional_video.mp4

# Create a simple text file explaining the video
cat > video_description.txt << EOF
NH6000sc 氨氮分析儀介紹影片
=======================

影片內容：Hach NH6000sc 氨氮分析儀 - 精準氨氮監測，實時數據采集，輕鬆系統集成，您的水質分析夥伴。hach.com

檔案：nh6000sc_professional_video.mp4
長度：10秒
解析度：1920x1080 (Full HD)
音訊：中文語音導覽

創建時間：$(date)
EOF

echo "Video creation completed!"