import glob, argparse, sys
from PIL import Image

def make_gif(frame_folder, resize, crop):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    print("frame count: ", len(frames))
    if resize != 1.0:
        for frame in frames:
            frame.thumbnail((int(frame.size[0] * resize), int(frame.size[1] * resize)))
    # crop frame
    cropped = []
    for frame in frames:
        cropped.append(frame.crop((crop[0], crop[1], frame.size[0] - crop[0], frame.size[1] - crop[1])))

    frame_one = cropped[0]
    frame_one.save("./results/result.gif", format="GIF", append_images=cropped[1:],
               save_all=True, duration=100, loop=0)

def unpackFrames(path):
    im = Image.open(path)
    framesCount = im.n_frames
    for i in range(framesCount):
        im.seek(i)
        num = str(i).zfill(3)
        im.save(f"{path}_{num}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ff", "--frame_folder", type=str, default="")
    parser.add_argument("-f", "--file_path", type=str, default="")
    parser.add_argument("-r", "--resize", type=float, default=1.0)
    parser.add_argument("-u", "--unpack", action="store_true")
    parser.add_argument("-ca", "--crop_top_bottom", type=int, default=0)
    parser.add_argument("-cr", "--crop_left_right", type=int, default=0)

    args = parser.parse_args()

    if args.unpack:
        unpackFrames(args.file_path)
        sys.exit()
    crop = (args.crop_left_right, args.crop_top_bottom)
    make_gif(args.frame_folder, args.resize, crop)
    sys.exit()