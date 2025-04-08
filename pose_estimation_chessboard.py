import cv2
import numpy as np

# 영상 경로 및 출력 파일명
video_file = 'recorded_video.mp4'
out_file = 'pose_output.mp4'

# 카메라 파라미터
K = np.array([[954.16431808, 0, 628.52580128],
              [0, 941.38014155, 349.91132073],
              [0, 0, 1]])
dist_coeff = np.array([-0.57718832, 0.00269906, 0.00406432, 0.00878291, -0.02297618])

# 체스보드 설정
board_pattern = (10, 7)
board_cellsize = 0.025  # 2.5cm

# 3D 박스 정의 (슬라이드 참고)
box_lower = board_cellsize * np.array([[4, 2, 0], [5, 2, 0], [5, 4, 0], [4, 4, 0]], dtype=np.float32)
box_upper = board_cellsize * np.array([[4, 2, -1], [5, 2, -1], [5, 4, -1], [4, 4, -1]], dtype=np.float32)

# 체스보드의 3D 좌표 생성 (슬라이드 참고)
obj_points = board_cellsize * np.array(
    [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])], dtype=np.float32
)

# 영상 열기
video = cv2.VideoCapture(video_file)
fps = video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 출력 영상 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(out_file, fourcc, fps, (width, height))

while True:
    valid, img = video.read()
    if not valid:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    board_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    found, corners = cv2.findChessboardCorners(gray, board_pattern, board_criteria)

    if found:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), board_criteria)
        ret, rvec, tvec = cv2.solvePnP(obj_points, corners, K, dist_coeff)

        line_lower, _ = cv2.projectPoints(box_lower, rvec, tvec, K, dist_coeff)
        line_upper, _ = cv2.projectPoints(box_upper, rvec, tvec, K, dist_coeff)

        cv2.polylines(img, [np.int32(line_lower)], True, (255, 0, 0), 2)
        cv2.polylines(img, [np.int32(line_upper)], True, (0, 0, 255), 2)

        for b, t in zip(line_lower, line_upper):
            cv2.line(img, np.int32(b).flatten(), np.int32(t).flatten(), (0, 255, 0), 2)

        # 카메라 위치 출력
        R, _ = cv2.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f"XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]"
        cv2.putText(img, info, (10, 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow('Camera Pose Estimation', img)
    out.write(img)

    key = cv2.waitKey(int(1000 // fps)) & 0xFF
    if key == 27:
        break

video.release()
out.release()
cv2.destroyAllWindows()
