# Multi-Image Panorama Creation SUing Image Stitching

![Result](examples/result.jpg)

## Why?

When you visit any place and take out the camera, and you get to know that you can't capture only one image for the specific scene.

What we can do in this case is capture multiple images and stitch them together to form one large image (of the entire scene).

Such photos of ordered scenes of collections are called panoramas. The entire process of acquiring multiple image and converting them into such panoramas is called as image stitching


## How?

Creating such panoramas involves the following steps:

1.  Estimate [homography](https://docs.opencv.org/3.4.1/d9/dab/tutorial_homography.html)
    1. Compute the sift-key points and descriptors (feature extraction)
    2. Select the top best matches for each descriptor of an image.
    3. Match correspondence between descriptors of the images.
    4. Use these matched points with [RANSAC](https://www.mathworks.com/discovery/ransac.html) to compute [homography](https://docs.opencv.org/3.4.1/d9/dab/tutorial_homography.html)

2.  Image-Warping
    1. Use the homography calculated to align the images properly

3. Stitch the images
    1. Stitch the aligned images
    1. Do any cleaning if needed (eg. trim)

## The process

### The images
I will be using the following images:

![Image 1](images/row-1-col-1.jpg)  |  ![Image 2](images/row-1-col-2.jpg) | ![Image 3](images/row-1-col-3.jpg)
:-------------------------:|:-------------------------:|:-------------------------:

### Finding Keypoints
In order to join any two images into a bigger image, we must find overlapping points. These overlapping points will give us an idea of the orientation of the second image according to first one.

Some features might be existing in multiple places. So we filter out through all the matches to obtain the best ones using [Lowe's] ratio test.

We can use SIFT and BFMatcher from `opencv` for the same which give us the following result:
![Key points](examples/keypoints.jpg)

### Stitching them up!
Once we find the relative orientations, we flip the perspective to match the others.
Then we stitch them all together!
![Result](examples/result.jpg)
