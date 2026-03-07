#!/bin/bash
# NH6000sc 10-second intro video creator - Chinese version
# Creates professional video with Chinese voiceover

set -e
WORKSPACE="/Users/leishi/.openclaw/workspace"
cd "$WORKSPACE"

echo "=== Creating NH6000sc Chinese Intro Video ==="
echo ""

# Step 1: Chinese voiceover script (professional tone)
# "Hach NH6000sc ammonia analyzer - real-time water quality monitoring, precise data, easy integration"
SCRIPT="Hach NH6000sc 氨氮分析仪。实时水质监测，数据精准，集成简便。"

echo "📝 Chinese Script:"
echo "   $SCRIPT"
echo ""

# Step 2: Generate Chinese TTS using macOS say command
echo "🎤 Generating Chinese voiceover..."

# List available voices and find Chinese ones
echo "   Checking available voices..."
CHINESE_VOICE=$(say -v '?' 2>/dev/null | grep -i "chinese\|zh-CN\|Mandarin" | head -1 | awk '{print $1}')

if [ -z "$CHINESE_VOICE" ]; then
    # Try common Chinese voice names on macOS
    for voice in Tingting Mei-Jia Sinji; do
        if say -v "$voice" "test" &>/dev/null; then
            CHINESE_VOICE=$voice
            break
        fi
    done
fi

if [ -z "$CHINESE_VOICE" ]; then
    echo "   ⚠️  No Chinese voice found, using default voice"
    CHINESE_VOICE=""
    VOICE_FLAG=""
else
    echo "   ✓ Using voice: $CHINESE_VOICE"
    VOICE_FLAG="-v $CHINESE_VOICE"
fi

# Generate audio - target ~8-9 seconds of speech for 10s video
say $VOICE_FLAG -o nh6000_voiceover.aiff "$SCRIPT"
echo "   ✓ Voiceover generated"

# Get actual audio duration
AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 nh6000_voiceover.aiff 2>/dev/null || echo "8")
echo "   Audio duration: ${AUDIO_DURATION}s"

# Target video duration: 10 seconds
VIDEO_DURATION=10

echo ""
echo "🎨 Creating professional background graphics..."

# Create a professional 1920x1080 animated background with gradient and text
# Using ffmpeg filter_complex for better quality

# First create a blue gradient background
ffmpeg -y -f lavfi -i "color=c=#0a1628:s=1920x1080:d=$VIDEO_DURATION" \
    -vf "format=yuva420p" \
    -c:v libx264 -preset fast -crf 20 \
    temp_bg.mp4 2>/dev/null

# Create the main video with layered text and effects
ffmpeg -y \
    -f lavfi -i "color=c=#0a1628:s=1920x1080:d=$VIDEO_DURATION" \
    -vf "
    format=yuva420p,
    drawbox=x=0:y=0:w=1920:h=1080:color=#004080@0.3:t=fill,
    drawgradient=direction=horizontal:0=#001a33:1=#0066cc,
    drawtext=fontfile=/System/Library/Fonts/Supplemental/PingFang.ttc:fontsize=80:fontcolor=#ffffff:x=(w-text_w)/2:y=h/2-80:text='Hach NH6000sc':alpha=1,
    drawtext=fontfile=/System/Library/Fonts/Supplemental/PingFang.ttc:fontsize=48:fontcolor=#00d4ff:x=(w-text_w)/2:y=h/2:text='氨氮分析仪':alpha=1,
    drawtext=fontfile=/System/Library/Fonts/Supplemental/PingFang.ttc:fontsize=32:fontcolor=#ffffff:x=(w-text_w)/2:y=h/2+60:text='实时监测 · 精准数据 · 简便集成':alpha=1
    " \
    -c:v libx264 -preset fast -crf 20 \
    -pix_fmt yuv420p \
    temp_video.mp4 2>/dev/null || {
    
    # Fallback without PingFang font
    echo "   Using fallback font..."
    ffmpeg -y \
        -f lavfi -i "color=c=#003366:s=1920x1080:d=$VIDEO_DURATION" \
        -vf "
        drawtext=fontsize=80:fontcolor=#ffffff:x=(w-text_w)/2:y=h/2-80:text='Hach NH6000sc',
        drawtext=fontsize=48:fontcolor=#00d4ff:x=(w-text_w)/2:y=h/2:text='Ammonia Analyzer',
        drawtext=fontsize=32:fontcolor=#ffffff:x=(w-text_w)/2:y=h/2+60:text='Real-time · Precise · Easy Integration'
        " \
        -c:v libx264 -preset fast -crf 20 \
        -pix_fmt yuv420p \
        temp_video.mp4
}

echo "   ✓ Background created"

echo ""
echo "🎬 Combining video and audio..."

# Combine video with voiceover
ffmpeg -y \
    -i temp_video.mp4 \
    -i nh6000_voiceover.aiff \
    -c:v libx264 -preset fast -crf 20 \
    -c:a aac -b:a 192k \
    -shortest \
    -pix_fmt yuv420p \
    -movflags +faststart \
    nh6000sc_intro_chinese.mp4

echo "   ✓ Video assembled"

# Verify and show output
echo ""
echo "=== ✅ Video Created Successfully ==="
echo ""

if [ -f nh6000sc_intro_chinese.mp4 ]; then
    echo "📁 Output file: $WORKSPACE/nh6000sc_intro_chinese.mp4"
    echo ""
    echo "📊 Video details:"
    ffprobe -v error -show_entries stream=codec_type,codec_name,duration,width,height -show_entries format=duration,size -of default=noprint_wrappers=1 nh6000sc_intro_chinese.mp4
    echo ""
    ls -lh nh6000sc_intro_chinese.mp4
    echo ""
    
    # Cleanup
    rm -f temp_bg.mp4 temp_video.mp4 nh6000_voiceover.aiff
    
    echo "🎉 Done! Video is ready to use."
else
    echo "❌ ERROR: Video creation failed"
    exit 1
fi
