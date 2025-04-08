#체스보드 구겼다가 펴기

체스보드 출력은 아이패드로 대체,
핸드폰 카메라의 왜곡도가 낮아서 FishEyeVideo 앱을 이용해 고의적으로 왜곡된 비디오를 얻었습니다.

camera_calibration.py를 통해  Camera matrix (K)를 얻고, 이 값을 바탕으로
distortion_correction.py를 통해 왜곡 보정된 비디오를 얻습니다.
pose_estimation_chessboard.py에서는 원본 영상에 AR박스를 그립니다.
