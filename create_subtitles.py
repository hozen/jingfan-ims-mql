#!/usr/bin/env python3

# Create SRT subtitles with timing that matches the voiceover
srt_content = """1
00:00:00,000 --> 00:00:10,000
Hach NH6000sc 氨氮分析儀

精準氨氮監測
實時數據采集
輕鬆系統集成

您的水質分析夥伴

hach.com"""

with open("nh6000sc_subtitles.srt", "w") as f:
    f.write(srt_content)

print("SRT subtitle file created!")
print("Now let's try to add subtitles to the video...")