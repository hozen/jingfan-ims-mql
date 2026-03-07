#!/bin/bash
# NH6000sc 10-second intro video creator

WORKSPACE="/Users/leishi/.openclaw/workspace"
cd "$WORKSPACE"

echo "=== Creating NH6000sc Intro Video ==="

# Step 1: Create Chinese voiceover script
# Professional tone about ammonia monitoring
SCRIPT="Hach NH6000sc 氨氮分析仪，实时水质监测，精准可靠，轻松集成。"
# Translation: "Hach NH6000sc ammonia analyzer, real-time water quality monitoring, precise and reliable, easy integration."

echo "Script: $SCRIPT"

# Step 2: Generate Chinese TTS using macOS say command
# Using zh-CN voice (Tingting or Mei-Jia are common Chinese voices on macOS)
echo "Generating Chinese voiceover..."

# Try to list available Chinese voices first
echo "Available voices:"
say -v '?' | grep -i chinese || say -v '?' | grep -i zh

# Generate audio with Chinese voice - try Tingting first, fallback to Mei-Jia
if say -v Tingting -o nh6000_voiceover.aiff "$SCRIPT" 2>/dev/null; then
    VOICE="Tingting"
elif say -v Mei-Jia -o nh6000_voiceover.aiff "$SCRIPT" 2>/dev/null; then
    VOICE="Mei-Jia"
else
    # Fallback to any available Chinese voice
    say -v '?' | grep -i chinese | head -1 | awk '{print $1}' | xargs -I {} say -v {} -o nh6000_voiceover.aiff "$SCRIPT"
    VOICE="default-chinese"
fi

echo "Voice used: $VOICE"

# Step 3: Get audio duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 nh6000_voiceover.aiff 2>/dev/null || echo "10")
echo "Audio duration: ${DURATION}s"

# Step 4: Create professional background graphic with product name
echo "Creating professional background graphic..."

# Create a 1920x1080 professional blue gradient background with product text
ffmpeg -y -f lavfi -i color=c=#003366:s=1920x1080:d=$DURATION \
    -vf "gradient=c0=#003366:c1=#0066cc:d=horizontal" \
    -vf "drawtext=fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-60:text='Hach NH6000sc'" \
    -vf "drawtext=fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=36:fontcolor=#00ffcc:x=(w-text_w)/2:y=(h-text_h)/2+20:text='氨氮分析仪'" \
    -vf "drawtext=fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=28:fontcolor=#ffffff:x=(w-text_w)/2:y=(h-text_h)/2+80:text='实时监测 · 精准可靠 · 轻松集成'" \
    nh6000_background.mp4 2>/dev/null

# If PingFang.ttc doesn't work, try alternative fonts
if [ ! -f nh6000_background.mp4 ]; then
    ffmpeg -y -f lavfi -i color=c=#003366:s=1920x1080:d=$DURATION \
        -vf "drawtext=fontfile=/System/Library/Fonts/Supplemental/PingFang.ttc:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-60:text='Hach NH6000sc'" \
        -vf "drawtext=fontfile=/System/Library/Fonts/Supplemental/PingFang.ttc:fontsize=36:fontcolor=#00ffcc:x=(w-text_w)/2:y=(h-text_h)/2+20:text='氨氮分析仪'" \
        -vf "drawtext=fontfile=/System/Library/Fonts/Supplemental/PingFang.ttc:fontsize=28:fontcolor=#ffffff:x=(w-text_w)/2:y=(h-text_h)/2+80:text='实时监测 · 精准可靠 · 轻松集成'" \
        nh6000_background.mp4 2>/dev/null
fi

# Fallback with system font
if [ ! -f nh6000_background.mp4 ]; then
    ffmpeg -y -f lavfi -i color=c=#003366:s=1920x1080:d=$DURATION \
        -vf "drawtext=fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-60:text='Hach NH6000sc'" \
        -vf "drawtext=fontsize=36:fontcolor=#00ffcc:x=(w-text_w)/2:y=(h-text_h)/2+20:text='Ammonia Analyzer'" \
        -vf "drawtext=fontsize=28:fontcolor=#ffffff:x=(w-text_w)/2:y=(h-text_h)/2+80:text='Real-time Monitoring'" \
        nh6000_background.mp4
fi

# Step 5: Combine video with audio
echo "Combining video and audio..."
ffmpeg -y -i nh6000_background.mp4 -i nh6000_voiceover.aiff \
    -c:v libx264 -preset fast -crf 22 \
    -c:a aac -b:a 192k \
    -shortest \
    -pix_fmt yuv420p \
    nh6000_intro.mp4

# Step 6: Verify output
echo ""
echo "=== Video Created Successfully ==="
if [ -f nh6000_intro.mp4 ]; then
    ffprobe -v error -show_entries format=duration,filename -of default=noprint_wrappers=1 nh6000_intro.mp4
    ls -lh nh6000_intro.mp4
    echo ""
    echo "Output file: $WORKSPACE/nh6000_intro.mp4"
else
    echo "ERROR: Video creation failed"
    exit 1
fi

# Cleanup intermediate files
rm -f nh6000_voiceover.aiff nh6000_background.mp4

echo ""
echo "Done!"
