import streamlit as st
import cv2
import dlib
import numpy as np
from streamlit_drawable_canvas import st_canvas
from PIL import Image


st.title("Privacy Face Blur")
st.markdown("### Upload an image and choose how to blur faces.")
st.write("""
- **Automatic Mode**: Automatically blur faces, then manually select additional faces to blur.
- **Manual Mode**: Allows you to manually select faces to blur.
""")

# State reset function
def reset_state():
    if 'original_image' in st.session_state:
        del st.session_state['original_image']
    if 'processed_image' in st.session_state:
        del st.session_state['processed_image']
    if 'auto_blur_done' in st.session_state:
        del st.session_state['auto_blur_done']
    if 'manual_blur' in st.session_state:
        del st.session_state['manual_blur']
    if 'additional_blur' in st.session_state:
        del st.session_state['additional_blur']


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], on_change=reset_state)

if uploaded_file is not None:
    # Read image
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    st.session_state['original_image'] = image

# Handle the case when no image is uploaded
if 'original_image' not in st.session_state:
    st.stop()

if 'original_image' in st.session_state:
    image = st.session_state['original_image']

   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    
    st.image(image, channels="BGR", caption="Uploaded Image", use_container_width=True)

    # Option to choose blurring mode
    blur_mode = st.radio("Select Blurring Mode", ("Automatic", "Manual"))

    if st.button("Process Image"):
        if blur_mode == "Automatic":
            # Face detection using dlib
            detector = dlib.get_frontal_face_detector()
            faces = detector(gray)
            face_rects = [(rect.left(), rect.top(), rect.width(), rect.height()) for rect in faces]

            for (x, y, w, h) in face_rects:
                # Ensure coordinates are within the image boundaries
                if x >= 0 and y >= 0 and (x + w) <= image.shape[1] and (y + h) <= image.shape[0]:
                    # Blur face region with smooth edges
                    face_region = image[y:y+h, x:x+w]
                    if face_region.size > 0:  # Check if face_region is not empty
                        mask = np.zeros((h, w), np.uint8)
                        mask = cv2.rectangle(mask, (0, 0), (w, h), (255, 255, 255), -1)
                        blurred_face = cv2.GaussianBlur(face_region, (15, 15), 30)  # Softer blurring
                        face_region = cv2.seamlessClone(blurred_face, face_region, mask, (w//2, h//2), cv2.NORMAL_CLONE)
                        image[y:y+h, x:x+w] = face_region

            st.session_state['processed_image'] = image
            st.session_state['auto_blur_done'] = True

        elif blur_mode == "Manual":
            st.session_state['manual_blur'] = True

    if 'auto_blur_done' in st.session_state and st.session_state['auto_blur_done']:
        image = st.session_state['processed_image']
        st.image(image, channels="BGR", caption="Automatically Blurred Faces", use_container_width=True)

        additional_blur = st.radio("Are there any faces left unblurred?", ("", "Yes", "No"))

        if additional_blur == "No":
            _, buffer = cv2.imencode('.png', image)
            st.download_button(
                label="Download Processed Image",
                data=buffer.tobytes(),
                file_name="blurred_image.png",
                mime="image/png"
            )
        elif additional_blur == "Yes":
            st.session_state['manual_blur'] = True

    if 'manual_blur' in st.session_state and st.session_state['manual_blur'] and additional_blur == "Yes":
        image = st.session_state['processed_image']
        annotated_image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Create a canvas for user interaction
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 255, 0.5)",  
            stroke_width=3,
            background_image=annotated_image_pil,
            update_streamlit=True,
            height=image.shape[0],
            width=image.shape[1],
            drawing_mode="rect",
            key="canvas",
        )

        # Check for user-drawn rectangles
        user_faces = []
        if canvas_result.json_data is not None:
            for obj in canvas_result.json_data["objects"]:
                if obj["type"] == "rect":
                    x = int(obj["left"])
                    y = int(obj["top"])
                    w = int(obj["width"])
                    h = int(obj["height"])
                    user_faces.append((x, y, w, h))

        if st.button("Blur Selected Faces"):
            with st.spinner("Blurring faces..."):
                for (x, y, w, h) in user_faces:
                    # Ensure coordinates are within the image boundaries
                    if x >= 0 and y >= 0 and (x + w) <= image.shape[1] and (y + h) <= image.shape[0]:
                        # Blur face region with smooth edges
                        face_region = image[y:y+h, x:x+w]
                        if face_region.size > 0:  # Check if face_region is not empty
                            mask = np.zeros((h, w), np.uint8)
                            mask = cv2.rectangle(mask, (0, 0), (w, h), (255, 255, 255), -1)
                            blurred_face = cv2.GaussianBlur(face_region, (15, 15), 30)  # Softer blurring
                            face_region = cv2.seamlessClone(blurred_face, face_region, mask, (w//2, h//2), cv2.NORMAL_CLONE)
                            image[y:y+h, x:x+w] = face_region

                
                st.image(image, channels="BGR", caption="Processed Image", use_container_width=True)

                
                _, buffer = cv2.imencode('.png', image)
                st.download_button(
                    label="Download Processed Image",
                    data=buffer.tobytes(),
                    file_name="blurred_image.png",
                    mime="image/png"
                )

