#!/bin/bash

# Create a simple video with blue background and add text overlay later
echo "Creating basic video with audio..."

# First create background video with audio
ffmpeg -y \
  -f lavfi -i color=color=#0055aa:s=1920x1080:d=10 \
  -i nh6000sc_voiceover_10s.mp3 \
  -c:v libx264 -c:a aac -shortest \
  nh6000sc_base_video.mp4

echo "Base video created!"
echo "Video properties:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 nh6000sc_base_video.mp4

echo "Files created:"
ls -l nh6000sc_*.mp3 nh6000sc_*.mp4 2>/dev/null | head -10