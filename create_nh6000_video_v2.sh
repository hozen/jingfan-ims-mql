#!/bin/bash
# NH6000sc 10-second intro video creator - Chinese version
# Creates professional video with Chinese voiceover using simple approach

set -e
WORKSPACE="/Users/leishi/.openclaw/workspace"
cd "$WORKSPACE"

echo "=== Creating NH6000sc Chinese Intro Video ==="
echo ""

# Step 1: Chinese voiceover script (professional tone)
SCRIPT="Hach NH6000sc 氨氮分析仪。实时水质监测，数据精准，集成简便。"

echo "📝 Chinese Script:"
echo "   $SCRIPT"
echo ""

# Step 2: Generate Chinese TTS using macOS say command
echo "🎤 Generating Chinese voiceover..."

# Find Chinese voice
CHINESE_VOICE=$(say -v '?' 2>/dev/null | grep -i "chinese\|zh-CN\|Mandarin\|Tingting\|Mei-Jia" | head -1 | awk '{print $1}')

if [ -z "$CHINESE_VOICE" ]; then
    for voice in Tingting Mei-Jia Sinji; do
        if say -v "$voice" "test" &>/dev/null; then
            CHINESE_VOICE=$voice
            break
        fi
    done
fi

if [ -n "$CHINESE_VOICE" ]; then
    echo "   ✓ Using voice: $CHINESE_VOICE"
    say -v "$CHINESE_VOICE" -o nh6000_voiceover.aiff "$SCRIPT"
else
    echo "   ⚠️  Using default voice"
    say -o nh6000_voiceover.aiff "$SCRIPT"
fi

echo "   ✓ Voiceover generated"

# Get audio duration
AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 nh6000_voiceover.aiff 2>/dev/null || echo "9")
VIDEO_DURATION=10

echo "   Audio duration: ${AUDIO_DURATION}s"

echo ""
echo "🎨 Creating professional graphics..."

# Create a solid color background with gradient using available filters
# Then use ImageMagick or sips to create text overlay, combine with ffmpeg

# Create base video with color gradient
ffmpeg -y -f lavfi -i "smptebars=s=1920x1080:d=$VIDEO_DURATION" \
    -vf "hue=s=0:b=0.3" \
    -c:v libx264 -preset fast -crf 20 \
    temp_base.mp4 2>/dev/null

# Create title card image using sips and textutil (macOS native)
# Or use a simpler approach: create frames with text using imagemagick if available

if command -v convert &> /dev/null; then
    echo "   Using ImageMagick for text overlay..."
    
    # Create background image with gradient
    convert -size 1920x1080 gradient:'#001a33-#0066cc' temp_bg.png
    
    # Add main title
    convert temp_bg.png \
        -font Helvetica-Bold -pointsize 80 -fill white \
        -gravity center -geometry +0-80 \
        -annotate 0 'Hach NH6000sc' \
        temp_title1.png
    
    # Add Chinese subtitle
    convert temp_title1.png \
        -font Helvetica -pointsize 48 -fill '#00d4ff' \
        -gravity center -geometry +0+10 \
        -annotate 0 '氨氮分析仪' \
        temp_title2.png
    
    # Add tagline
    convert temp_title2.png \
        -font Helvetica -pointsize 32 -fill white \
        -gravity center -geometry +0+100 \
        -annotate 0 'Real-time · Precise · Easy Integration' \
        temp_title.png
    
    # Convert image to video
    ffmpeg -y -loop 1 -i temp_title.png -t $VIDEO_DURATION \
        -c:v libx264 -preset fast -crf 20 \
        -pix_fmt yuv420p \
        temp_video.mp4 2>/dev/null
    
    rm -f temp_bg.png temp_title1.png temp_title2.png temp_title.png
else
    echo "   Using simple color background..."
    # Simple blue background
    ffmpeg -y -f lavfi -i "color=c=#003366:s=1920x1080:d=$VIDEO_DURATION" \
        -c:v libx264 -preset fast -crf 20 \
        -pix_fmt yuv420p \
        temp_video.mp4 2>/dev/null
fi

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
    rm -f temp_base.mp4 temp_video.mp4 nh6000_voiceover.aiff
    
    echo "🎉 Done! Video is ready to use."
else
    echo "❌ ERROR: Video creation failed"
    exit 1
fi
