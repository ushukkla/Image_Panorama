import cv2
import numpy as np
import glob
import numpy
import random
def stitching():
    all_img = []
    all_img.extend(glob.glob('images/' + '*.jpg'))
    all_img.sort()

    result = cv2.imread(all_img[0])
    for i, image in enumerate(all_img):
        if i is 0:
            continue

        image1 = result
        image2 = cv2.imread(all_img[i])

        cross1, cross2, good = compare_matches(image1, image2)

        if len(good) < 38:
            print("Notfound: ", len(good))
            return

        src_pts = np.float32([cross1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([cross2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
         h2, w2 = image1.shape[:2]
        h, w = image2.shape[:2]
        points2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
        points1 = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        points2 = cv2.perspectiveTransform(points1, M)

        pts = np.concatenate((points1, points2), axis=0)

        [xmin, ymin] = np.int32(pts.min(axis=0).ravel() - 0.5)
        [xmax, ymax] = np.int32(pts.max(axis=0).ravel() + 0.5)
        t = [-xmin, -ymin]

        transfer = np.array([[1, 0, t[0]], [0, 1, t[1]], [0, 0, 1]])  

        result = cv2.warpPerspective(image1, transfer.dot(M), (xmax - xmin, ymax - ymin))
        result[t[1]:h + t[1], t[0]:w + t[0]] = image2

    cv2.imwrite('result.jpg', result)


def compare_matches(image1, image2):
    sift = cv2.xfeatures2d.SIFT_create()

    cross1, final1 = sift.detectAndCompute(image1, None)
    cross2, final2 = sift.detectAndCompute(image2, None)

    match = cv2.BFMatcher(crossCheck=True)
    matches = match.match(final1, final2)
    good = sorted(matches, key=lambda x: x.distance)[:100]  # Pick top 100

    parameters = dict(matchColor=(0, 255, 0),
                       singlePointColor=None,
                       flags=2)

    image3 = cv2.drawMatches(image1, cross1, image2, cross2, good, None, **parameters)
    return cross1, cross2, good

stitching()