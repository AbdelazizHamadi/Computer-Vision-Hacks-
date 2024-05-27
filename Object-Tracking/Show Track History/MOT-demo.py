################# MOT dataset

import os
from collections import defaultdict
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import random


#
def generate_random_color():
    # Generate a random color in RGB format
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)


dataset = "C:/Users/azizc/Downloads/MOT15/MOT15/train/PETS09-S2L1"
gt_path = dataset + "/gt/gt.txt"
images_path = dataset + "/img1"

images = os.listdir(images_path)


def read_gt_file(gt_file_path):
    # Dictionary to store track ID and corresponding frame IDs and bounding boxes
    track_dict = defaultdict(lambda: {'frames': [], 'bboxes': []})

    # Read the ground truth file
    with open(gt_file_path, 'r') as file:
        for line in file:
            # Parse each line
            parts = line.strip().split(',')
            frame_id = int(parts[0])
            track_id = int(parts[1])
            bbox = list(map(float, parts[2:6]))  # [x, y, width, height]

            # Append the frame ID and bbox to the list of the corresponding track ID
            if track_id != -1:
                track_dict[track_id]['frames'].append(frame_id)
                track_dict[track_id]['bboxes'].append(bbox)

    # Convert defaultdict to a regular dictionary and sort by track ID
    sorted_track_dict = dict(sorted(track_dict.items()))

    return sorted_track_dict


def plot_bboxes_on_frame(track_dict, frame_num=20, max_tracks=3, frame_range=(0, 56)):
    # Create a figure and axis
    fig, ax = plt.subplots(1, figsize=(10, 10))

    # simple way to find the corresponding frame (matching the frame found with the images in folder)

    frame_target = None
    for image_name in images:
        if int(image_name.split(".")[0]) == frame_num:
            frame_target = plt.imread(os.path.join(images_path, image_name))

    # plot frame
    ax.imshow(frame_target)

    # generate random colors
    num_colors = max_tracks
    random_colors = [generate_random_color() for _ in range(num_colors)]

    # Plot the bounding boxes for the first `max_tracks` tracks
    for track_id, color in zip(list(track_dict.keys())[:max_tracks], random_colors):

        track_data = track_dict[track_id]
        for frame_id, bbox in zip(track_data['frames'], track_data['bboxes']):
            if frame_id == frame_num:
                rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=2, edgecolor=color,
                                         facecolor='none')
                ax.add_patch(rect)
                # Annotate with track ID
                plt.text(bbox[0], bbox[1] - 10, f"ID: {track_id}", color='white', fontsize=12,
                         bbox=dict(facecolor=color, alpha=0.5))

            if frame_id >= frame_range[0] and frame_id <= frame_range[1]:
                # Add a rectangle for the bounding box
                x_center = bbox[0]
                y_center = bbox[1] + bbox[3]

                # Plot the center point
                plt.plot(x_center, y_center, 'o', label=f"ID: {track_id}", c=color)

    # Set plot title and limits
    ax.set_title(f'Track history between {frame_range[0]} and {frame_range[1]}')
    # Show the plot
    plt.show()


def main():
    # Path to the gt.txt file (change this to your actual path)
    gt_file_path = gt_path

    if not os.path.exists(gt_file_path):
        print(f"File {gt_file_path} does not exist.")
        return

    # Read and process the gt file
    track_dict = read_gt_file(gt_file_path)
    # specify the right ranges here

    # i just chose random intervals that goes well with the video chosen
    ranges = [(100, 200), (250, 300), (400, 500), (600, 650), (700, 750), (750, 795)]

    for ranging in ranges:
        plot_bboxes_on_frame(track_dict, frame_num=(ranging[0] + ranging[1]) // 2, max_tracks=6, frame_range=ranging)


if __name__ == "__main__":
    main()
