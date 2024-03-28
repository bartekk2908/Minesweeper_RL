import os
import imageio
import numpy as np

def create_gif(directory, file, ending_frames=0, frame_time=0.2):
    file_names = os.listdir(directory)
    images = np.empty(len(file_names) + ending_frames, dtype=object)
    for file_name in file_names:
        images[int(str(file_name).replace(".jpg", ""))] = imageio.imread(f"{directory}\\{file_name}")
    for i in range(ending_frames):
        images[len(file_names) + i] = images[len(file_names) - 1]
    imageio.mimwrite(file, list(images), duration=frame_time)


if __name__ == "__main__":

    SCREENS_DIR = "screenshots"
    GIFS_DIR = "gifs"
    ENDING_FRAMES = 4
    FRAME_TIME = 700

    if not os.path.exists(GIFS_DIR):
        os.makedirs(GIFS_DIR)

    for i in range(1, len(os.listdir(SCREENS_DIR)) + 1):
        create_gif(f"{SCREENS_DIR}\\{i}", f"{GIFS_DIR}\\{i}.gif", ENDING_FRAMES, FRAME_TIME)
