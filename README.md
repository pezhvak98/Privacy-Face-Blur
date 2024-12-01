
# Privacy Face Blur

**Privacy Face Blur** is a user-friendly application designed to automatically and manually blur faces in images, ensuring privacy by anonymizing faces in photos.

## Features

-   **Automatic Face Blurring**:  Automatically blurs faces, then allows manual selection of additional faces..
    
-   **Manual Face Blurring**: Allows users to manually select faces or regions to blur.    
    

## Installation

### Clone the Repository

To get started, clone the repository to your local machine using the following command:
```bash
git clone https://github.com/pezhvak98/Privacy-Face-Blur.git
cd Privacy-Face-Blur
```
### Installation Script

To install this app and all the required dependencies after cloning, simply run the installation script:
```bash
chmod +x install.sh
./install.sh
```
The `install.sh` script will take care of installing all the prerequisites needed to run `PrivacyFaceBlur` on your system. Installation items are listed below:

-   **Python** 3.x
    
-   **pip** (Python package installer)

-   **Streamlit**: For building the web application interface.
    
-   **OpenCV**: For image processing and face detection.
    
-   **Dlib**: For face detection algorithms.
    
-   **Numpy**: For numerical operations on images.
    
-   **Streamlit-Drawable-Canvas**: For interactive canvas drawing in Streamlit.
    
-   **Pillow**: For image manipulation.

## Usage

To run the PrivacyFaceBlur app, execute the following command in your terminal:
```bash
streamlit app.py
```
You can now view your Streamlit app directly in your browser.

```bash
  Local URL: http://localhost:<Your-Local-Port>
  Network URL: http://<Your-IP>:<Your-Local-Port>
  ```
  ---


