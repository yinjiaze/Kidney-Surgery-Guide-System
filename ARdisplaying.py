import cv2
import numpy as np
import math
from objloader import *


MIN_MATCHES = 20


def get_homography(des_model, frame1, Camera):
    try:
        kp_frame, des_frame = orb.detectAndCompute(frame1, None)
        matches = bf.match(des_model, des_frame)
        matches = sorted(matches, key=lambda x: x.distance)
        if len(matches) > MIN_MATCHES:
            src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            dst = cv2.perspectiveTransform(pts, homography)
            frame = cv2.polylines(frame1, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            if homography is not None:
                try:
                    projection = projection_matrix(Camera, homography)
                    frame = render(frame, obj, projection, model, False)
                    cv2.imshow('frame', frame)

                except Exception:
                    pass
                    
        else:
            print("Notbreak enough mathces")
    
    except Exception:
        pass


def projection_matrix(camera, homography):
    """
    From the camera calibration matrix and the estimated homography
    compute the 3D projection matrix
    """
    # Compute rotation along the x and y axis as well as the translation
    homography = homography * (-1)
    rot_and_transl = np.dot(np.linalg.inv(camera), homography)
    col_1 = rot_and_transl[:, 0]
    col_2 = rot_and_transl[:, 1]
    col_3 = rot_and_transl[:, 2]
    # normalise vectors
    l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
    rot_1 = col_1 / l
    rot_2 = col_2 / l
    translation = col_3 / l
    # compute the orthonormal basis
    c = rot_1 + rot_2
    p = np.cross(rot_1, rot_2)
    d = np.cross(c, p)
    rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_3 = np.cross(rot_1, rot_2)
    # finally, compute the 3D projection matrix from the model to the current frame
    projection = np.stack((rot_1, rot_2, rot_3, translation)).T

    return np.dot(camera, projection)


def set_camera_matrix(fc1, fc2, cc1, cc2, alpha):
    camera = np.zeros(9)
    camera = camera.reshape(3, 3)
    camera[0, 0] = fc1
    camera[0, 1] = alpha*fc1
    camera[0, 2] = cc1
    camera[1, 1] = fc2
    camera[1, 2] = cc2
    camera[2, 2] = 1

    return camera


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    h_len = len(hex_color)
    
    return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))


def render(img, obj, projection, model, color=False):
    vertices = obj.vertices
    scale_matrix = np.eye(3)
    h, w = model.shape

    for face in obj.faces:
        face_vertices = face[0]
        points = np.array([vertices[vertex - 1] for vertex in face_vertices])
        points = np.dot(points, scale_matrix)
        points = np.array([[p[0] + w / 2, p[1] + h / 2, p[2]] for p in points])
        dst = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection)
        imgpts = np.int32(dst)
        cv2.fillConvexPoly(img, imgpts, (137, 27, 211))

        return img


Camera = set_camera_matrix(fc1=1433.98343, fc2=1433.13694, cc1=660.35007, cc2=322.92345, alpha=0)
model = cv2.imread('model3.jpg', 0)
obj = OBJ("cow.obj", swapyz=True)
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
kp_model, des_model = orb.detectAndCompute(model, None)

h, w = model.shape
pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

cap = cv2.VideoCapture(2)
cap.set(3,1280)
cap.set(4,720)

while(True):
    ret, frame = cap.read()
    get_homography(des_model, frame, Camera)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


