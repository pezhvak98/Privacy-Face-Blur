#!/bin/bash


print_bold() {
    echo -e "\e[1m$1\e[0m"
}


print_bold "Updating package list and upgrading all packages..."
sudo apt update && sudo apt upgrade -y

print_bold "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

print_bold "Installing OpenCV dependencies..."
sudo apt install -y libsm6 libxext6 libxrender-dev libglib2.0-0

print_bold "Installing required Python packages..."
pip3 install streamlit opencv-python dlib numpy streamlit-drawable-canvas pillow

print_bold "All prerequisites have been installed. You can now run the Privacy-Face-Blur app."
