# -*- coding: utf-8 -*-
"""RASHMI_IVA_LAB2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18V7PMcbDxoLVEU-iRgT3D51dZ4YvssY2

LAB2 IMAGE AND VIDEO ANALYTICS

21MIA1077
RASHMI AV

Lab Task 1: Setup and Basic Extraction
Objective:
Install the necessary tools and libraries, and extract frame information from a video.
Steps:
1.	Install ffmpeg and ffmpeg-python:

  Install the ffmpeg tool and the ffmpeg-python library.
2.	Extract Frame Information:
  
  Extract frame information from a sample video.
"""

!pip install pyav

"""Lab Task 2: Frame Type Analysis

Objective:
Analyze the extracted frame information to understand the distribution of I, P, and B frames in a video.

Steps:
1.	Modify the Script:

	Count the number of I, P, and B frames.

	Calculate the percentage of each frame type in the video.
2.	Analyze Frame Distribution:
	Plot the distribution of frame types using a library like matplotlib.
  
  Plot a pie chart or bar graph showing the distribution of frame types using matplotlib.

"""

import av

container = av.open("/content/file_example_MP4_480_1_5MG.mp4")
total_frames = 0
frame_types = {'I': 0, 'P': 0, 'B': 0}

for frame in container.decode(video=0):
    total_frames += 1
    frame_types[frame.pict_type.name] += 1

container.close()

print(f"Total frames: {total_frames}")
print(f"Frame types: {frame_types}")

!pip install ffmpeg

import av
import matplotlib.pyplot as plt

def analyze_frame_types(video_path):
    total_frames = 0
    frame_types = {'I': 0, 'P': 0, 'B': 0}

    container = av.open(video_path)

    for frame in container.decode(video=0):
        total_frames += 1
        frame_types[frame.pict_type.name] += 1

    return frame_types, total_frames
def plot_frame_distribution(frame_counts, total_frames):
    frame_types = ['I Frames', 'P Frames', 'B Frames']
    counts = [frame_counts.get('I', 0), frame_counts.get('P', 0), frame_counts.get('B', 0)]

    if total_frames > 0:
        percentages = [(count / total_frames) * 100 for count in counts]

        print("Frame Type Distribution:")
        for frame_type, count, percentage in zip(frame_types, counts, percentages):
            print(f"{frame_type}: Count = {count}, Percentage = {percentage:.2f}%")

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(frame_types, counts, color=['blue', 'orange', 'green'])
        plt.title('Frame Type Count')
        plt.ylabel('Number of Frames')

        plt.subplot(1, 2, 2)
        plt.pie(percentages, labels=frame_types, autopct='%1.1f%%', startangle=90)
        plt.title('Frame Type Distribution')

        plt.show()
    else:
        print("No frames found in the video.")
def main(video_path):
    frame_counts, total_frames = analyze_frame_types(video_path)
    plot_frame_distribution(frame_counts, total_frames)

if __name__ == "__main__":
    video_path = '/content/file_example_MP4_480_1_5MG.mp4'
    main(video_path)

"""Lab Task 3: Visualizing Frames

Objective:

Extract actual frames from the video and display them using Python.

Steps:
1.	Extract Frames:

	Use ffmpeg to extract individual I, P, and B frames from the video.

	Save these frames as image files.
2.	Display Frames:

	Use a library like PIL (Pillow) or opencv-python to display the extracted frames.

Tasks:
1.	Save I, P, and B frames as separate image files using ffmpeg.
2.	Use PIL or opencv-python to load and display these frames in a Python script.
3.	Compare the visual quality of I, P, and B frames.

"""

import av
import matplotlib.pyplot as plt
import numpy as np

container = av.open('/content/file_example_MP4_480_1_5MG.mp4')

frame_counts = {'I': 0, 'P': 0, 'B': 0}

frames_to_display = {'I': [], 'P': [], 'B': []}

for frame in container.decode(video=0):
    frame_type = frame.pict_type.name

    if frame_counts[frame_type] < 2:
        frame_image = frame.to_image()

        frame_array = np.array(frame_image)

        frames_to_display[frame_type].append(frame_array)

        frame_counts[frame_type] += 1
    if all(count >= 2 for count in frame_counts.values()):
        break

def display_frames(frames, frame_type):
    for i, frame in enumerate(frames):
        plt.figure(figsize=(10, 5))
        plt.imshow(frame)
        plt.title(f"{frame_type} Frame: {i+1}")
        plt.axis('off')
        plt.show()

for frame_type in ['I', 'P', 'B']:
    display_frames(frames_to_display[frame_type], frame_type)

"""Lab Task 4: Frame Compression Analysis

Objective:

Analyze the compression efficiency of I, P, and B frames.

Steps:
1.	Calculate Frame Sizes:
	Calculate the file sizes of extracted I, P, and B frames.
	Compare the average file sizes of each frame type.
2.	Compression Efficiency:
	Discuss the role of each frame type in video compression.
	Analyze why P and B frames are generally smaller than I frames.

"""

# Extract I frames
!ffmpeg -i 5927708-hd_1080_1920_30fps.mp4 -vf "select='eq(pict_type\,I)'" -vsync vfr -frame_pts true I_frame_%04d.png

# Extract P frames
!ffmpeg -i 5927708-hd_1080_1920_30fps.mp4 -vf "select='eq(pict_type\,P)'" -vsync vfr -frame_pts true P_frame_%04d.png

# Extract B frames
!ffmpeg -i 5927708-hd_1080_1920_30fps.mp4 -vf "select='eq(pict_type\,B)'" -vsync vfr -frame_pts true B_frame_%04d.png

import os
import glob

def calculate_average_frame_size(frame_type):
    frame_files = glob.glob(f'{frame_type}_frame_*.png')
    total_size = sum(os.path.getsize(frame) for frame in frame_files)
    average_size = total_size / len(frame_files) if frame_files else 0
    print(f"Total size of all {frame_type} frames: {total_size} KB")
    return average_size

average_size_I = calculate_average_frame_size('I')
average_size_P = calculate_average_frame_size('P')
average_size_B = calculate_average_frame_size('B')

print(f"Average size of I frames: {average_size_I / 1024:.2f} KB")
print(f"Average size of P frames: {average_size_P / 1024:.2f} KB")
print(f"Average size of B frames: {average_size_B / 1024:.2f} KB")

"""In video compression, three primary frame types—Intra-coded (I), Predicted (P), and Bidirectional (B) frames—each play unique roles. I-frames are key frames that are encoded independently, serving as reference points, but they are large due to containing complete image data. P-frames store only changes from previous frames, using predictive coding, resulting in smaller sizes by encoding just the differences. B-frames use both preceding and following frames for reference, capturing redundancies in both directions, making them the smallest.\
 P and B frames achieve higher compression through temporal compression and motion compensation, reducing data by encoding motion vectors and residual differences. This efficient compression reduces file sizes significantly compared to I-frames.

Lab Task 5: Advanced Frame Extraction

Objective:

Extract frames from a video and reconstruct a part of the video using only I frames.

Steps:

1.	Extract and Save I Frames:

	Extract I frames from the video and save them as separate image files.
2.	Reconstruct Video:

	Use the extracted I frames to reconstruct a portion of the video.
  
	Create a new video using these I frames with a reduced frame rate.
"""

import subprocess
import os

def extract_i_frames(video_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'select=eq(pict_type\\,I)',
            '-vsync', 'vfr',
            f'{output_dir}/frame_%04d.png'
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"I-frames extracted successfully to {output_dir}")

    except Exception as e:
        print(f"Error extracting I-frames: {str(e)}")

video_path = '/content/file_example_MP4_480_1_5MG.mp4'
i_frames_dir = 'I_frames'

extract_i_frames(video_path, i_frames_dir)
def reconstruct_video_from_i_frames(i_frames_dir, output_video_path, frame_rate=1):
    try:
        cmd = [
            'ffmpeg',
            '-framerate', str(frame_rate),
            '-i', os.path.join(i_frames_dir, 'frame_%04d.png'),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_video_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Video reconstructed successfully and saved to {output_video_path}")

    except Exception as e:
        print(f"Error reconstructing video: {str(e)}")

output_video_path = 'reconstruct_video.mp4'
reconstruct_video_from_i_frames(i_frames_dir, output_video_path,frame_rate=3)

from IPython.display import Video
Video('reconstruct_video.mp4', embed=True)

