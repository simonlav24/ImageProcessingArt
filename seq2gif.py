import glob, argparse
from PIL import Image

def make_gif(frame_folder, resize):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    print("frame count: ", len(frames))
    if resize != 1.0:
        for frame in frames:
            frame.thumbnail((int(frame.size[0] * resize), int(frame.size[1] * resize)))



    frame_one = frames[0]
    frame_one.save("./results/result.gif", format="GIF", append_images=frames[1:],
               save_all=True, duration=100, loop=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ff", "--frame_folder", type=str, default="")
    # float that represents the resizing of the image
    parser.add_argument("-r", "--resize", type=float, default=1.0)
    args = parser.parse_args()

    make_gif(args.frame_folder, args.resize)