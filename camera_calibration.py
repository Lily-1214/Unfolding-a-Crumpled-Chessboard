import cv2
import numpy as np

def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10):
    video = cv2.VideoCapture(video_file)
    img_select = []

    while True:
        valid, img = video.read()
        if not valid:
            break

        display = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, board_pattern)

        if found:
            cv2.drawChessboardCorners(display, board_pattern, corners, found)
            cv2.imshow('Select Frames', display)
            key = cv2.waitKey(wait_msec) & 0xFF

            if select_all or key == ord(' '):
                img_select.append(img)
            elif key == 27:  # ESC to exit
                break

    video.release()
    cv2.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    obj_points = []

    # 3D 기준 좌표 만들기
    objp = np.zeros((board_pattern[0] * board_pattern[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_pattern[0], 0:board_pattern[1]].T.reshape(-1, 2)
    objp *= board_cellsize  # 스케일 적용

    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, board_pattern)
        if found:
            img_points.append(corners)  # shape (N, 1, 2)
            obj_points.append(objp.copy())  # shape (N, 3)

    assert len(img_points) > 0, 'No complete chessboard patterns were found.'

    # 이미지 크기
    img_size = gray.shape[::-1]
    ret, K, dist_coeff, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, img_size, K, dist_coeff, flags=calib_flags
    )
    return ret, K, dist_coeff, rvecs, tvecs

if __name__ == '__main__':
    board_pattern = (10, 7)
    board_cellsize = 0.025  # 예: 2.5cm
    video_file = 'recorded_video.mp4'

    print('Selecting images from video...')
    images = select_img_from_video(video_file, board_pattern)

    print('Running camera calibration...')
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(images, board_pattern, board_cellsize)

    print('RMS Error =', rms)
    print('Camera Matrix (K) =\n', K)
    print('Distortion Coefficients =', dist_coeff.ravel())
