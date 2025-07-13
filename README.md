# AI Fitness Trainer

A real-time fitness trainer application that uses computer vision to track exercises, count repetitions, and provide form feedback using MediaPipe and Streamlit.

## Features

- **Real-time pose estimation** using MediaPipe
- **Live webcam feed** with skeleton overlay
- **Support for 8 exercises**:
  - **Calisthenics**: Push-ups, Squats, Lunges
  - **Dumbbell**: Bicep Curls, Shoulder Press, Rows
  - **Core**: Plank Hold
  - **Bar**: Pull-ups
- **Automatic rep counting** with state detection
- **Real-time form feedback** with scoring system
- **Exercise state tracking** (ready, up, down, hold)
- **Session statistics** (total reps, average rep time)
- **Adjustable settings** for confidence threshold and feedback sensitivity
- **Modern UI** with emojis and clear visual feedback
- **Responsive design** that works on desktop and mobile

## Requirements

- Python 3.8+
- Webcam
- The required Python packages are listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-fitness-trainer.git
cd ai-fitness-trainer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Allow webcam access when prompted by your browser.

3. Select an exercise from the dropdown menu.

4. Adjust settings in the expandable settings panel if needed.

5. Click "Start" to begin pose detection.

6. Position yourself in front of the camera so your full body is visible.

7. Start exercising! The app will automatically:
   - Track your movements with skeleton overlay
   - Count repetitions
   - Provide real-time form feedback
   - Display your form score
   - Show exercise state (ready/up/down/hold)

## Exercise Instructions

### Calisthenics
- **Push-ups**: Keep your back straight, lower until arms are at 90 degrees
- **Squats**: Keep knees aligned, lower until thighs are parallel to ground
- **Lunges**: Keep hips level, lower until back knee nearly touches ground

### Dumbbell Exercises
- **Bicep Curls**: Maintain even motion, full range of movement
- **Shoulder Press**: Press weights straight overhead with even arm movement
- **Rows**: Maintain straight back while pulling weights toward chest

### Core & Bar
- **Plank Hold**: Keep back straight and hips level
- **Pull-ups**: Pull until chin is over the bar, maintain even arm movement

## Technical Details

### Dependencies
- `streamlit`: Web application framework
- `streamlit-webrtc`: Real-time webcam streaming
- `numpy`: Numerical computations
- `opencv-python`: Computer vision processing
- `mediapipe`: Pose estimation
- `av`: Audio/video processing

### Architecture
- **Frontend**: Streamlit with real-time video streaming
- **Pose Detection**: MediaPipe Pose for 33-point body landmark detection
- **Exercise Analysis**: Custom algorithms for each exercise type
- **State Management**: Streamlit session state for tracking progress

### Pose Detection
The app uses MediaPipe's pose estimation to detect 33 body landmarks:
- Head and face landmarks
- Upper body (shoulders, elbows, wrists)
- Lower body (hips, knees, ankles)
- Calculates joint angles for exercise analysis

## Extending the App

To add new exercises:

1. Add the exercise definition to `EXERCISES` in `exercise_utils.py`:
```python
'new_exercise': {'name': 'New Exercise', 'category': 'Category'}
```

2. Create an analysis function following the pattern:
```python
def analyze_new_exercise(landmarks):
    # Get relevant landmarks
    # Calculate angles
    # Determine state and provide feedback
    return state, form_score, feedback
```

3. Add the analysis function to the `analysis_funcs` dictionary in `app.py`

## Troubleshooting

- **Webcam not working**: Check browser camera permissions and ensure no other app is using the camera
- **Poor pose detection**: Ensure good lighting and clear view of your full body
- **Unstable tracking**: Adjust the confidence threshold in settings
- **Slow performance**: Close other applications using the camera

## Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [MediaPipe](https://mediapipe.dev/) for pose estimation
- Inspired by [FitGenie_BicepCurls](https://github.com/Pratik-Jodgudri/FitGenie_BicepCurls)
- Uses [Streamlit](https://streamlit.io/) for the web interface 