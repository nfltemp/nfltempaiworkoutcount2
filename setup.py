from setuptools import setup, find_packages

setup(
    name="nfltempaiworkoutcount",
    version="1.0.0",
    description="AI Fitness Trainer with MediaPipe",
    python_requires=">=3.8,<3.12",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "streamlit-webrtc", 
        "numpy",
        "opencv-python",
        "mediapipe",
        "av"
    ],
) 