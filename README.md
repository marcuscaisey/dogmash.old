# DogMash
This is a clone of Mark Zuckerberg's FaceMash (except with dogs).

## Usage
If you would like to use your own dog images, then place them in `dogmash/static/images/dogs`. It's recommended that they all have an aspect ratio of 3:4.

If you don't want to use your own images, then you can download some from [Unsplash](https://unsplash.com/) using the script `downloadimages.py`. (You will need to create an Unsplash application to get an API access key.)

Run the script with `downloadimages.py access_key [images]` where `access_key` is your Unsplash API access key and `images` is an optional argument specifying the number of images to download.

## To do
- Use argparse or similar library to parse arguments to `downloadimages.py`
- Refactor messy JS
