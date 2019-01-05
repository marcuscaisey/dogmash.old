import click
import pathlib
import sys

import requests
from PIL import Image

ROOT_DIR = pathlib.Path(__file__).parent
DOWNLOAD_DIR = ROOT_DIR / "dogmash/static/images/dogs"
ASPECT_RATIO = 3 / 4
# Largest width images will need to be is 45vh at 4K. I.e. 0.45 * 2560 = 1152
MAX_WIDTH = 1152


def crop_around_centre(image, w, h):
    """Return image cropped to width `w` and height `h` around its centre.

    Args:
        image (PIL.Image.Image): Image to be cropped.
        w (int): Width to crop to.
        h (int): Height to crop to.

    Returns:
        PIL.Image.Image: Cropped image.
    """
    # Need to crop the image so that an equal length is cropped from the left
    # and right side. Let d be the width cropped from each side, then it
    # follows that 2d + w = current_w as shown below.
    #       0                                                        currrent_w
    #       -------------------------------------------------------------
    #       |_______||_________________________________________||_______|
    #           d                         w                         d
    # So d = (current_w - w) / 2 and we need to crop the image between the
    # the x coordinates d and d + w.
    #
    # A almost identical argument (replacing w, current_w, d with h, current_h,
    # d_) shows that we need to crop the image between the y coordinates d_ and
    # d_ + h, where d_ = (current_h - h) / 2.
    current_w, current_h = image.width, image.height
    d = round((current_w - w) / 2)
    d_ = round((current_h - h) / 2)
    # PIL uses Cartesian coordinates with (0, 0) in top left corner.
    top_left = (d, d_)
    bottom_right = (d + w, d_ + h)
    cropped_image = image.crop((*top_left, *bottom_right))
    return cropped_image


def cropped_dimensions(w, h, r):
    """Return dimensions that image should be cropped to so that it has aspect
    ratio `r` and neither its width nor height need to be increased.

    Args:
        w (int): Original width of image.
        h (int): Original height of image.
        r (float): Desired aspect ratio of image.

    Returns:
        tuple of int: Width and height as a tuple: (width, height).
    """
    current_r = w / h

    # No need to crop if current aspect ratio is equal to desired ratio.
    if current_r == r:
        new_w, new_h = w, h

    # Either height needs to be increased, or width decreased to reduce
    # current_r. Reduce width since we don't want to increase the height, so
    # fix h. Then we have new_w / h = r => new_w = r * h.
    elif current_r > r:
        new_w = round(r * h)
        new_h = h

    # Same as above except now we are fixing w, giving us
    # w / new_h = r => new_h = w / r
    elif current_r < r:
        new_w = w
        new_h = round(w / r)

    return new_w, new_h


def download_images(access_key, images):
    """Download `images` number of images of dogs from unsplash, crop them to
    aspect ratio `ASPECT_RATIO`, and resize them to width `MAX_WIDTH` to reduce
    file size.

    Args:
        access_key (str): Unsplash API access key.
        images (int, optional): Number of images to download.
    """
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {access_key}",
    }
    params = {
        "query": "dog",
        "page": 1,
        "per_page": 30,  # Unsplash API only allows max of 30 images per page
        "orientation": "portrait",
    }

    downloaded = 0
    while downloaded < images:
        api_response = requests.get(url, headers=headers, params=params)
        results = api_response.json()["results"]

        for result in results:
            # Download image
            image_url = result["urls"]["raw"]
            r = requests.get(image_url)
            image_path = DOWNLOAD_DIR / f"{result['id']}.jpg"
            with image_path.open("wb") as f:
                f.write(r.content)

            image = Image.open(image_path)

            # Crop image
            w, h = cropped_dimensions(image.width, image.height, ASPECT_RATIO)
            image = crop_around_centre(image, w, h)

            # Resize image
            if w > MAX_WIDTH:
                image = image.resize(
                    (MAX_WIDTH, int(MAX_WIDTH / ASPECT_RATIO))
                )

            # Save image
            image.save(image_path)

            downloaded += 1
            if downloaded == images:
                break

        if downloaded < images:
            params["page"] += 1


@click.command()
@click.argument("access_key")
@click.option(
    "--images",
    "-n",
    default=50,
    type=int,
    help="Number of images to download.",
    show_default=True,
    metavar="",
)
def main(access_key, images):
    """Download images of dogs from Unsplash."""
    download_images(access_key, images)


if __name__ == "__main__":
    main()
