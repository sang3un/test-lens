import cv2

import streamlit as st

from streamlit_back_camera_input import back_camera_input
from PIL import Image


if "scanning" not in st.session_state:
    st.session_state.scanning = False
if "picture" not in st.session_state:
    st.session_state.picture = False


def initiate_camera_scan():
    st.session_state.scanning = True
    st.session_state.camera = cv2.VideoCapture(0)


def capture_photo():
    if "camera" in st.session_state and st.session_state.camera.isOpened():
        ret, frame = st.session_state.camera.read()
        if ret:
            st.image(frame, channels="BGR")
        else:
            st.write("unable to capture photo")
    else:
        st.error("Could not open camera.")


def close_camera():
    if "camera" in st.session_state and st.session_state.camera.isOpened():
        st.session_state.camera.release()
        st.session_state.scanning = False
    else:
        st.error("camera is already closed")


def get_camera_input():
    if "scanning" not in st.session_state or not st.session_state.scanning:
        if st.button("  📷  ", use_container_width=True, key="start_camera"):
            initiate_camera_scan()
    if "scanning" in st.session_state and st.session_state.scanning:
        camera = st.session_state.camera
        ret, frame = camera.read()

        if ret:
            st.image(frame, channels="BGR", caption="실시간 카메라")

        # 캡처 이미지 버튼
        if st.button("capture image"):
            capture_photo()

        # 카메라 종료 버튼
        if st.button("카메라 종료"):
            close_camera()
    # else:
    #     if st.button("capture image", key="capture_image"):
    #         capture_photo()
    #     if st.button("close camera", key="close_camera"):
    #         close_camera()
    # if st.session_state.get("scanning", False):
    #     return process_camera_input()


def process_camera_input() -> str:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        st.write("Error: Could not open camera.")
        return

    captured_image = None

    while True:
        # Read a frame (capture the image)
        ret, frame = camera.read()

        if ret:
            st.image(frame, channels="BGR")
            if st.button('capture photo'):
                captured_image = frame
                break

    # If a photo was captured, save it and display success
    if captured_image is not None:
        st.image(captured_image, caption="Captured Image", channels="BGR")

    # Release the camera
    camera.release()


def main():
    get_camera_input()


if __name__ == "__main__":
    # main()
    if st.button("  📷  ", use_container_width=True, key="start_camera"):
        image = back_camera_input()

    if image:
        st.image(image)

