#!/usr/bin/env python3
import cv2
import numpy as np
import subprocess
import os

# Video settings
WIDTH, HEIGHT = 1920, 1080
FPS = 30
DURATION = 10
TOTAL_FRAMES = FPS * DURATION

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('nh6000sc_video.mp4', fourcc, FPS, (WIDTH, HEIGHT))

# Create background gradient
def create_gradient_background(frame_count):
    """Create animated gradient background"""
    gradient = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # Create blue gradient that shifts slightly
    for y in range(HEIGHT):
        progress = frame_count / TOTAL_FRAMES
        blue_val = int(30 + 10 * np.sin(progress * np.pi * 2))
        green_val = int(100 + 30 * np.sin(progress * np.pi * 2 + np.pi/2))
        
        # Vertical gradient
        gradient[y, :, 0] = blue_val  # Blue channel
        gradient[y, :, 1] = green_val # Green channel
        gradient[y, :, 2] = 0        # Red channel
    
    return gradient

def add_text(frame, text, y_position, font_scale=1.0, color=(255, 255, 255), thickness=2):
    """Add text to frame with proper positioning"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Center horizontally
    x_position = (WIDTH - text_width) // 2
    
    cv2.putText(frame, text, (x_position, y_position), 
                font, font_scale, color, thickness, cv2.LINE_AA)
    
    return y_position + text_height + baseline + 20

def create_frame(frame_count):
    """Create a single frame with animated text"""
    frame = create_gradient_background(frame_count)
    
    # Animation progress
    progress = frame_count / TOTAL_FRAMES
    
    # Starting y position
    y_pos = HEIGHT // 3
    
    # Animate text appearance
    if progress < 0.2:
        # Product name appears first
        text_opacity = min(progress * 5, 1.0)
        color = (255, 255, 255) if text_opacity > 0.5 else (128, 128, 128)
        y_pos = add_text(frame, "Hach NH6000sc 氨氮分析儀", y_pos, 2.0, color)
    else:
        y_pos = add_text(frame, "Hach NH6000sc 氨氮分析儀", y_pos, 2.0)
    
    if progress > 0.3:
        # Features appear sequentially
        features = [
            "精準氨氮監測",
            "實時數據采集", 
            "輕鬆系統集成",
            "您的水質分析夥伴"
        ]
        
        for i, feature in enumerate(features):
            if progress > 0.3 + i * 0.15:
                opacity = min((progress - (0.3 + i * 0.15)) * 6.66, 1.0)
                color = (200, 200, 200) if opacity > 0.5 else (100, 100, 100)
                y_pos = add_text(frame, feature, y_pos, 1.2, color)
    
    if progress > 0.85:
        # Website appears last
        opacity = min((progress - 0.85) * 6.66, 1.0)
        color = (220, 220, 220) if opacity > 0.5 else (100, 100, 100)
        y_pos = add_text(frame, "hach.com", HEIGHT - 100, 1.5, color)
    
    return frame

# Generate all frames
print("Creating video frames...")
for frame_count in range(TOTAL_FRAMES):
    frame = create_frame(frame_count)
    video.write(frame)
    
    if frame_count % 30 == 0:  # Progress update every second
        print(f"Generated {frame_count}/{TOTAL_FRAMES} frames")

video.release()
print("Video created successfully!")

# Combine video with audio
print("Combining video with audio...")
subprocess.run([
    'ffmpeg', '-y',
    '-i', 'nh6000sc_video.mp4',
    '-i', 'nh6000sc_voiceover_10s.mp3',
    '-c', 'copy',
    '-shortest',
    'nh6000sc_final_video.mp4'
], check=True)

print("Final video created: nh6000sc_final_video.mp4")
print("Testing audio output...")
subprocess.run(['afplay', 'nh6000sc_voiceover_10s.mp3'])

# Check file size and properties
result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', 
                        '-of', 'default=noprint_wrappers=1', 'nh6000sc_final_video.mp4'], 
                       capture_output=True, text=True)
print("Video properties:")
print(result.stdout)