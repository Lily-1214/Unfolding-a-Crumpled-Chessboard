import cv2
import numpy as np

# 영상 파일 및 보정 파라미터
video_file = 'recorded_video.mp4'
out_file = 'rectified_output.mp4'
K = np.array([[954.16,   0,   628.53],
              [  0,    941.38, 349.91],
              [  0,      0,     1   ]])
dist_coeff = np.array([-0.577, 0.0027, 0.0041, 0.0088, -0.0230])

# 영상 열기
video = cv2.VideoCapture(video_file)
fps = video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 출력 영상 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(out_file, fourcc, fps, (width, height))

show_rectify = True
map1, map2 = None, None

while True:
    valid, img = video.read()
    if not valid:
        break

    display = img.copy()

    if show_rectify:
        if map1 is None or map2 is None:
            map1, map2 = cv2.initUndistortRectifyMap(K, dist_coeff, None, None, (width, height), cv2.CV_32FC1)
        display = cv2.remap(display, map1, map2, interpolation=cv2.INTER_LINEAR)
        info = "Rectified"
    else:
        info = "Original"

    # 텍스트 오버레이 및 영상 출력
    cv2.putText(display, info, (10, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 1)
    cv2.imshow('Distortion Correction', display)

    # 보정된 프레임 저장
    if show_rectify:
        out.write(display)

    key = cv2.waitKey(int(1000 // fps)) & 0xFF
    if key == 27:
        break
    elif key == ord(' '):
        show_rectify = not show_rectify

video.release()
out.release()
cv2.destroyAllWindows()
