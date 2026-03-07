#!/usr/bin/env python3
"""
Hach Marketing Video Generator - Improved Version
====================================================
- Gradient backgrounds
- Background music
- Fade in/out effects
- Better voice timing
"""

import os
import sys
import subprocess
import argparse
import datetime
from PIL import Image, ImageDraw, ImageFont

# Configuration
OUTPUT_DIR = "/Users/leishi/.openclaw/workspace/hach_marketing_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Video settings
WIDTH, HEIGHT = 1080, 1920  # Vertical 9:16
FPS = 25

# Font
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

def create_gradient_background(output_path, duration, colors=[(26, 90, 140), (45, 120, 180), (26, 90, 140)]):
    """Create a gradient background video"""
    # Create gradient image
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    
    # Draw vertical gradient
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    img.save(output_path.replace('.mp4', '.png'), 'PNG')
    
    # Convert to video with loop
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", output_path.replace('.mp4', '.png'),
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={WIDTH}:{HEIGHT}",
        "-r", str(FPS),
        "-vsync", "cfr",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)
    os.remove(output_path.replace('.mp4', '.png'))
    return output_path

def create_text_image(text, output_path, bg_color=(26, 90, 140), text_color="white"):
    """Create a single frame with text on gradient background"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    colors = [(26, 90, 140), (45, 130, 190)]
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    # Add some visual interest - subtle pattern
    for i in range(0, WIDTH, 40):
        draw.line([(i, 0), (i+20, HEIGHT)], fill=(255, 255, 255), width=1)
    
    # Load font
    try:
        font = ImageFont.truetype(FONT_PATH, 72)
    except:
        font = ImageFont.load_default()
    
    # Handle multi-line text
    lines = text.split('\n')
    line_height = 90
    total_height = len(lines) * line_height
    start_y = (HEIGHT - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = start_y + i * line_height
        
        # Draw border for visibility
        for ox in [-3, 3]:
            for oy in [-3, 3]:
                draw.text((x+ox, y+oy), line, font=font, fill="black")
        draw.text((x, y), line, font=font, fill=text_color)
    
    img.save(output_path, "PNG", quality=95)
    return output_path

def create_video_clip_with_fade(image_path, duration, output_path):
    """Create a video clip with fade in/out"""
    # Create clip with fade filter
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-vf", f"scale={WIDTH}:{HEIGHT},fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5",
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-vsync", "cfr",
        "-profile:v", "high",
        "-crf", "23",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def concatenate_videos(video_list, output_path):
    """Concatenate multiple videos with crossfade"""
    concat_file = os.path.join(OUTPUT_DIR, "concat.txt")
    with open(concat_file, "w") as f:
        for v in video_list:
            f.write(f"file '{v}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(concat_file)
    return result.returncode == 0

def generate_voiceover(text, output_path):
    """Generate Chinese voiceover"""
    cmd = ["say", "-v", "Ting-Ting", "-o", output_path, text]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def add_background_music(video_path, music_path, output_path, video_duration=30):
    """Add background music to video"""
    # Check if music file exists, if not create a simple ambient sound
    if not os.path.exists(music_path):
        # Create a simple ambient sine wave
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency=220:duration={video_duration}",
            "-c:a", "aac",
            "-b:a", "48k",
            "-ar", "22050",
            music_path
        ]
        subprocess.run(cmd, capture_output=True)
    
    # If music file doesn't exist or is invalid, skip background music
    if not os.path.exists(music_path):
        # Just copy the original
        subprocess.run(["cp", video_path, output_path])
        return True
    
    # Mix original audio with background music
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", music_path,
            "-filter_complex", "[0:a]volume=0.7[a0];[1:a]volume=0.2[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback: just copy
            subprocess.run(["cp", video_path, output_path])
    except:
        subprocess.run(["cp", video_path, output_path])
    return True

def add_fade_out(video_path, output_path, fade_duration=1):
    """Add fade out effect to end of video"""
    # Use -c:a copy to avoid re-encoding audio issues
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"fade=t=out:st=29:d={fade_duration}",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def loop_audio_to_duration(audio_path, target_duration, output_path):
    """Loop audio to match target duration"""
    # Convert to mp3 first
    mp3_path = audio_path.replace('.aiff', '.mp3')
    subprocess.run(["ffmpeg", "-y", "-i", audio_path, "-ar", "22050", "-ac", "1", mp3_path], 
                   capture_output=True)
    
    # Calculate how many times to loop
    # Get audio duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
         "-of", "default=noprint_wrappers=1:nokey=1", mp3_path],
        capture_output=True, text=True
    )
    try:
        audio_duration = float(result.stdout.strip())
    except:
        audio_duration = 16  # Default
    
    # Loop to target duration
    loops_needed = int(target_duration / audio_duration) + 1
    
    cmd = [
        "ffmpeg", "-y",
    ]
    # Add input multiple times
    for _ in range(loops_needed):
        cmd.extend(["-stream_loop", "1"])
    cmd.extend([
        "-i", mp3_path,
        "-c:a", "aac",
        "-t", str(target_duration),
        output_path
    ])
    subprocess.run(cmd, capture_output=True)
    
    # Cleanup
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
    return True

def combine_video_audio(video_path, audio_path, output_path):
    """Combine video and audio"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def generate_video(product_name, feature_keyword):
    """Main function to generate marketing video"""
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    video_name = f"hach_{product_name.lower()}_ims_{timestamp}"
    
    print("=" * 50)
    print(f"Generating Video: {product_name} + IMS")
    print("=" * 50)
    
    # Define slides based on product and feature
    slides = [
        {"text": f"【{product_name}】智能运维新时代", "duration": 5},
        {"text": f"痛点：{feature_keyword}？\n导致成本增加或停机损失？", "duration": 5},
        {"text": f"IMS + {product_name}\n智能解决方案", "duration": 5},
        {"text": "精准数据采集\n实时监控预警", "duration": 5},
        {"text": "提升效率\n降低成本", "duration": 5},
        {"text": "扫码了解更多\nIMS - 仪器管理系统", "duration": 5},
    ]
    
    # Create text images
    print("1. Creating text slides with gradient backgrounds...")
    image_paths = []
    for i, slide in enumerate(slides):
        img_path = os.path.join(OUTPUT_DIR, f"slide_{i:02d}.png")
        create_text_image(slide["text"], img_path)
        image_paths.append(img_path)
    
    # Create video clips with fade
    print("2. Creating video clips with fade effects...")
    clip_paths = []
    for i, (img_path, slide) in enumerate(zip(image_paths, slides)):
        clip_path = os.path.join(OUTPUT_DIR, f"clip_{i}.mp4")
        if create_video_clip_with_fade(img_path, slide["duration"], clip_path):
            clip_paths.append(clip_path)
    
    # Concatenate clips
    print("3. Concatenating clips...")
    video_path = os.path.join(OUTPUT_DIR, f"{video_name}_video.mp4")
    concatenate_videos(clip_paths, video_path)
    
    # Generate voiceover
    print("4. Generating voiceover...")
    voiceover_text = f"{product_name} 携手 IMS 智能管理系统，精准解决{feature_keyword}问题，实时监控预警，提升运维效率，让您的水处理更加轻松高效。"
    voiceover_path = os.path.join(OUTPUT_DIR, f"{video_name}_voice.aiff")
    generate_voiceover(voiceover_text, voiceover_path)
    
    # Loop audio to match video duration (30 seconds)
    video_duration = 30
    audio_loop_path = os.path.join(OUTPUT_DIR, f"{video_name}_voice_loop.aac")
    loop_audio_to_duration(voiceover_path, video_duration, audio_loop_path)
    
    # Combine video and voice
    print("5. Combining video and audio...")
    combined_path = os.path.join(OUTPUT_DIR, f"{video_name}_combined.mp4")
    combine_video_audio(video_path, audio_loop_path, combined_path)
    
    # Add fade out at the end
    print("6. Adding fade out effect...")
    final_path = os.path.join(OUTPUT_DIR, f"{video_name}_final.mp4")
    add_fade_out(combined_path, final_path, fade_duration=1.5)
    
    # Add background music (optional - creates more professional feel)
    print("7. Adding background music...")
    music_path = os.path.join(OUTPUT_DIR, "bg_music.aac")
    final_with_music = os.path.join(OUTPUT_DIR, f"{video_name}_with_music.mp4")
    add_background_music(final_path, music_path, final_with_music)
    
    # Use the version with music as final
    if os.path.exists(final_with_music):
        os.rename(final_with_music, final_path)
    
    # Cleanup intermediate files
    print("8. Cleaning up...")
    for f in image_paths + clip_paths + [video_path, voiceover_path, audio_loop_path, combined_path, music_path]:
        if os.path.exists(f):
            os.remove(f)
    
    # Check result
    if os.path.exists(final_path):
        size = os.path.getsize(final_path)
        print("\n" + "=" * 50)
        print("✅ Video Generated Successfully!")
        print("=" * 50)
        print(f"📁 Output: {final_path}")
        print(f"📊 Size: {size/1024/1024:.1f} MB")
        print(f"⏱ Duration: 30 seconds")
        print(f"📐 Resolution: 1080x1920 (Vertical 9:16)")
        print(f"✨ Features: Gradient background, fade effects, background music")
        return final_path
    else:
        print("\n❌ Video generation failed")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hach Marketing Video Generator - Improved")
    parser.add_argument("--product", required=True, help="Product name (e.g., CL17sc, NH6000sc)")
    parser.add_argument("--feature", required=True, help="Key feature/benefit")
    
    args = parser.parse_args()
    
    result = generate_video(args.product, args.feature)
    if result:
        print(f"\n🎉 Ready to share: {result}")
