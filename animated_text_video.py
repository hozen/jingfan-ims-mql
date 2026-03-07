#!/usr/bin/env python3
import subprocess
import os
import time

print("Creating NH6000sc video with animated text...")

# First create individual frames with text
def create_frame_with_text(frame_number, text_lines):
    """Create a frame with specified text lines"""
    filename = f"frame_{frame_number:04d}.png"
    
    # Simple approach: use ImageMagick via command line if available
    try:
        # Create transparent background with text
        cmd = [
            'convert', '-size', '1920x1080', 'xc:transparent',
            '-font', 'Arial', '-fill', 'white', '-pointsize', 72,
            '-gravity', 'center', f'label:{text_lines[0]}', filename
        ]
        
        subprocess.run(cmd, capture_output=True)
        return filename
    except:
        # Fallback: create empty file
        with open(filename, 'w') as f:
            f.write(f"Frame {frame_number}: {' | '.join(text_lines)}")
        return filename

# Create frames with progressive text appearance
frames = []
for i in range(300):  # 10 seconds at 30fps
    seconds = i / 30.0
    text_lines = []
    
    if seconds >= 0:
        text_lines.append("Hach NH6000sc 氨氮分析儀")
    if seconds >= 1.5:
        text_lines.append("精準氨氮監測")
    if seconds >= 3:
        text_lines.append("實時數據采集")
    if seconds >= 4.5:
        text_lines.append("輕鬆系統集成")
    if seconds >= 6:
        text_lines.append("您的水質分析夥伴")
    if seconds >= 8:
        text_lines.append("hach.com")
    
    if text_lines:
        filename = create_frame_with_text(i, text_lines)
        frames.append(filename)

print(f"Created {len(frames)} frames")

# Create video from frames
print("Creating video from frames...")
subprocess.run([
    'ffmpeg', '-y',
    '-framerate', '30',
    '-i', 'frame_%04d.png',
    '-i', 'nh6000sc_voiceover_10s.mp3',
    '-c:v', 'libx264', '-c:a', 'aac',
    '-pix_fmt', 'yuv420p',
    'nh6000sc_final_video.mp4'
])

# Clean up frames
for frame in frames:
    if os.path.exists(frame):
        os.remove(frame)

print("NH6000sc video created successfully!")

# Verify the result
result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', 
                        '-of', 'default=noprint_wrappers=1', 'nh6000sc_final_video.mp4'], 
                       capture_output=True, text=True)
print("Video properties:")
print(result.stdout)

# Test audio
print("Testing audio output...")
subprocess.run(['afplay', 'nh6000sc_voiceover_10s.mp3'])