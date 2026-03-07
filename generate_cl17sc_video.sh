#!/bin/bash
# Hach CL17sc + IMS Marketing Video Generator (v2)

OUTPUT_DIR="/Users/leishi/.openclaw/workspace/hach_marketing_videos"
mkdir -p "$OUTPUT_DIR"

PRODUCT="CL17sc余氯分析仪"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_NAME="hach_cl17sc_ims_${TIMESTAMP}"

echo "=========================================="
echo "Hach CL17sc + IMS Video Generator"
echo "=========================================="

# Step 1: Create 30-second gradient background
echo "1. Creating background..."
ffmpeg -y -f lavfi -i "color=c=0x1a5a8c:s=1080x1920:d=30" \
    -c:v libx264 -t 30 -pix_fmt yuv420p \
    "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" 2>/dev/null

# Step 2: Create slides with text
echo "2. Creating slides..."

# Slide 1
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" \
    -vf "drawtext=text='【$PRODUCT】智能运维':fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+50:borderw=3:bordercolor=black" \
    -t 5 -c:a copy "$OUTPUT_DIR/slide_01.mp4" 2>/dev/null

# Slide 2  
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" \
    -vf "drawtext=text='试剂更换不及时？':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-20:borderw=3:bordercolor=black,drawtext=text='浪费成本 or 停机损失？':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+40:borderw=3:bordercolor=black" \
    -ss 5 -t 5 -c:a copy "$OUTPUT_DIR/slide_02.mp4" 2>/dev/null

# Slide 3
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" \
    -vf "drawtext=text='IMS + $PRODUCT':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-20:borderw=3:bordercolor=black,drawtext=text='智能试剂用量预测':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+40:borderw=3:bordercolor=black" \
    -ss 10 -t 5 -c:a copy "$OUTPUT_DIR/slide_03.mp4" 2>/dev/null

# Slide 4
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" \
    -vf "drawtext=text='精准计算消耗':fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-20:borderw=3:bordercolor=black,drawtext=text='提前提醒更换':fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+40:borderw=3:bordercolor=black" \
    -ss 15 -t 5 -c:a copy "$OUTPUT_DIR/slide_04.mp4" 2>/dev/null

# Slide 5
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" \
    -vf "drawtext=text='不早不晚':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-20:borderw=3:bordercolor=black,drawtext=text='刚刚好':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+40:borderw=3:bordercolor=black" \
    -ss 20 -t 5 -c:a copy "$OUTPUT_DIR/slide_05.mp4" 2>/dev/null

# Slide 6
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_bg.mp4" \
    -vf "drawtext=text='扫码了解更多':fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-20:borderw=3:bordercolor=black,drawtext=text='IMS - 仪器管理系统':fontsize=44:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+40:borderw=3:bordercolor=black" \
    -ss 25 -t 5 -c:a copy "$OUTPUT_DIR/slide_06.mp4" 2>/dev/null

# Step 3: Concatenate
echo "3. Concatenating..."
cat > "$OUTPUT_DIR/concat.txt" 
file '$OUTPUT_DIR/slide_01.mp4'
file '$OUTPUT_DIR/slide_02.mp4'
file '$OUTPUT_DIR/slide_03.mp4'
file '$OUTPUT_DIR/slide_04.mp4'
file '$OUTPUT_DIR/slide_05.mp4'
file '$OUTPUT_DIR/slide_06.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i "$OUTPUT_DIR/concat.txt" \
    -c copy "$OUTPUT_DIR/${OUTPUT_NAME}_video.mp4" 2>/dev/null

# Step 4: Generate voiceover
echo "4. Generating voiceover..."
say -v "Ting-Ting" -o "$OUTPUT_DIR/${OUTPUT_NAME}_voice.aiff" \
    "$PRODUCT 携手 IMS 智能试剂管理系统，精准预测试剂用量，提前提醒更换时机，避免浪费和停机损失，让您的水处理运维更轻松。"

# Step 5: Combine
echo "5. Combining video and audio..."
ffmpeg -y -i "$OUTPUT_DIR/${OUTPUT_NAME}_video.mp4" \
    -i "$OUTPUT_DIR/${OUTPUT_NAME}_voice.aiff" \
    -c:v copy -c:a aac -shortest \
    "$OUTPUT_DIR/${OUTPUT_NAME}_final.mp4" 2>/dev/null

echo ""
echo "=========================================="
echo "✅ Video Generated!"
echo "=========================================="
echo "📁 Output: $OUTPUT_DIR/${OUTPUT_NAME}_final.mp4"
ls -lh "$OUTPUT_DIR/${OUTPUT_NAME}_final.mp4"
