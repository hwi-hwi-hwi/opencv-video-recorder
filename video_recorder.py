import cv2 as cv


def main():
    # 카메라 영상 읽기
    video = cv.VideoCapture(0)
    # 카메라 정상 작동 확인
    if not video.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("카메라가 작동합니다.")
    # 영상 정보 얻기
    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)
    # 안전장치(Fallback): 값을 제대로 못 읽어왔을 경우(fps == 0.0), 웹캠의 가장 표준적인 프레임 속도인 30.0으로 값을 강제 고정
    if fps <= 0.0:
        fps = 30.0

    # 동영상 파일로 저장하기 위한 VideoWriter 객체 생성
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    target = cv.VideoWriter('output.avi', fourcc, fps, (width, height))

    is_recording = False
    is_flipped = False  # 추가 기능: 좌우 반전 상태 변수

    print("Space: 녹화 시작/중지 | 'F': 좌우 반전 필터 | ESC: 종료")

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # 추가 기능: 'F' 키를 누르면 좌우 반전 (Flip)
        if is_flipped:
            frame = cv.flip(frame, 1)

        # 저장용 원본 프레임과 화면 표시용 프레임을 분리 -> 녹화 파일에는 빨간 원이 들어가지 않도록 하기 위함
        display_frame = frame.copy()

        # Preview와 Record 모드 제어
        if is_recording:  # 녹화 중일 때만
            target.write(frame)  # 파일에 쓰기

            # 화면 우측 상단에 <REC + 빨간색 원> 표시
            # cv.circle(img, center, radius, color, thickness)
            # cv.putText(img, text, position, font, scale, color)
            cv.circle(display_frame, (90, 30), 10, (0, 0, 255), -1)
            # 검정 글씨 ("REC") 먼저 쓰기 -> 글씨 그림자처럼 보이게 (글씨가 이미지 때문에 안 보일 때, 글씨("REC")가 보일 수 있게 하기 위함)
            cv.putText(display_frame, "REC", (20, 40),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.9, (0, 0, 0), 6)
            # 검정 글씨 위에 빨간 글씨 ("REC")
            cv.putText(display_frame, "REC", (20, 40),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 0, 255), 2)

        # 화면 출력
        cv.imshow('Video Recorder', display_frame)

        # 키보드 이벤트 처리 (ESC, Space)
        # cf) key = cv.waitKey(int(1000 / fps)): 원본 영상의 초당 프레임 수(FPS)를 계산해 다음 프레임까지 정확한 시간(예: 30fps면 약 33ms)을 기다림
        # -> 인위적인 대기 시간(int(1000/fps))을 추가하면 화면이 점점 밀리거나 뚝뚝 끊기는 현상이 발생 가능
        key = cv.waitKey(1)  # ms(0.001초)만 짧게 대기하고 즉시 다음 코드를 실행 -> 장점: 실시간 웹캠은 기기 하드웨어 자체가 프레임 속도를 조절

        if key == 27:  # ESC 키: 종료
            break
        elif key == ord(' '):  # Space(ASCII 값): 모드 변환
            is_recording = not is_recording  # 녹화 O <-> 녹화 X
            if is_recording:
                print("녹화 시작")
            else:
                print("녹화 중지")
        elif key == ord('f') or key == ord('F'):  # 추가 기능: 'F' 키를 누르면 좌우 반전 (Flip)
            is_flipped = not is_flipped  # 좌우 반전

    # 자원 해제
    print("카메라가 종료됩니다.")
    video.release()
    target.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()