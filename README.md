# 체스보드 구겼다가 펴기

체스보드 출력은 아이패드로 대체,

핸드폰 카메라의 왜곡도가 낮아서 FishEyeVideo 앱을 이용해 고의적으로 왜곡된 비디오를 얻었습니다.


<img width="311" alt="화면 캡처 2025-04-08 221332" src="https://github.com/user-attachments/assets/02b794cb-68b2-4230-8ba0-75a1ccb4f789" />


camera_calibration.py를 통해  Camera matrix (K)를 얻고,

이 값을 바탕으로 distortion_correction.py를 통해 왜곡 보정된 비디오를 얻습니다.

pose_estimation_chessboard.py에서는 원본 영상에 AR박스를 그립니다.



## 원본 영상

![recorded_video_640x360_10fps](https://github.com/user-attachments/assets/4e554d1a-d008-45cb-9f07-0035426ba16c)



## 캘리브레이션 결과

<img width="437" alt="1" src="https://github.com/user-attachments/assets/139c3ff7-10b0-4f41-86a1-af934aa96f44" />



## 렌즈 왜곡 보정 수행

![rectified_output_640x360_10fps](https://github.com/user-attachments/assets/4b4cdd91-7491-4114-b5f9-d3deed4af06f)



## AR박스 출력 영상

![pose_output_640x360_10fps](https://github.com/user-attachments/assets/151bc644-d21d-4bae-8b03-32c05fa9634f)
