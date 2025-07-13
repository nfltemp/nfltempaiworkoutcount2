import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import threading
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
from exercise_utils import (
    EXERCISES,
    analyze_pushup,
    analyze_squat,
    analyze_curl,
    analyze_plank,
    analyze_pullup,
    analyze_lunge,
    analyze_press,
    analyze_row,
    analyze_goblet_squat,
    analyze_lateral_raise,
    analyze_tricep_extension,
    analyze_front_raise,
    analyze_deadlift,
    analyze_overhead_squat
)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class PoseTransformer(VideoTransformerBase):
    def __init__(self):
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.exercise_state = 'ready'
        self.last_rep_time = time.time()
        self.rep_count = 0
        self.total_reps = 0
        self.form_score = 100
        self.feedback = ''
        self.selected_exercise = 'pushup'
        self.confidence_threshold = 0.5
        self.feedback_sensitivity = 0.5
        
        # Improved state detection variables
        self.previous_state = 'ready'
        self.state_stable_frames = 0
        self.last_state_change_time = time.time()
        self.state_confidence = 0.0
        
        # Analysis functions mapping
        self.analysis_funcs = {
            'pushup': analyze_pushup,
            'squat': analyze_squat,
            'curl': analyze_curl,
            'plank': analyze_plank,
            'pullup': analyze_pullup,
            'lunge': analyze_lunge,
            'press': analyze_press,
            'row': analyze_row,
            'goblet_squat': analyze_goblet_squat,
            'lateral_raise': analyze_lateral_raise,
            'tricep_extension': analyze_tricep_extension,
            'front_raise': analyze_front_raise,
            'deadlift': analyze_deadlift,
            'overhead_squat': analyze_overhead_squat
        }

    def transform(self, frame):
        # Convert frame to RGB
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.pose.process(img_rgb)
        
        if results.pose_landmarks:
            # Draw skeleton
            mp_drawing.draw_landmarks(
                img_rgb,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            # Analyze exercise
            landmarks = results.pose_landmarks.landmark
            
            if self.selected_exercise in self.analysis_funcs:
                new_state, form_score, feedback = self.analysis_funcs[self.selected_exercise](landmarks)
                current_time = time.time()
                
                # Improved state detection logic
                if new_state == self.previous_state:
                    self.state_stable_frames += 1
                else:
                    self.state_stable_frames = 0
                    self.previous_state = new_state
                
                # Calculate state confidence based on stability
                self.state_confidence = min(self.state_stable_frames / 3.0, 1.0)
                
                # More flexible state change conditions
                min_stable_frames = 1 if new_state in ['up', 'down'] else 2
                
                if self.state_stable_frames >= min_stable_frames:
                    # Allow state change if it's been stable enough
                    if new_state != self.exercise_state:
                        # Check for valid rep transition with improved logic
                        if new_state == 'up' and self.exercise_state == 'down':
                            # More forgiving timing - allow faster reps
                            if current_time - self.last_rep_time > 0.4:
                                self.rep_count += 1
                                self.total_reps += 1
                                self.last_rep_time = current_time
                        
                        # Update state and track change time
                        self.exercise_state = new_state
                        self.last_state_change_time = current_time
                
                # Handle edge cases for better reliability
                # If we've been in 'ready' state too long and detect motion, transition
                if (self.exercise_state == 'ready' and 
                    new_state in ['up', 'down'] and 
                    self.state_stable_frames >= 1):
                    self.exercise_state = new_state
                
                # If we detect 'down' state clearly, transition even if not fully stable
                if (new_state == 'down' and 
                    self.exercise_state == 'ready' and 
                    self.state_stable_frames >= 1):
                    self.exercise_state = new_state
                
                self.form_score = form_score
                self.feedback = feedback
        
        # Convert back to BGR for display
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        # Add exercise state indicator with confidence
        cv2.putText(img_bgr, f"State: {self.exercise_state.upper()}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img_bgr, f"Reps: {self.rep_count}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img_bgr, f"Score: {self.form_score}%", 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(img_bgr, f"Conf: {self.state_confidence:.1f}", 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        
        return img_bgr

def main():
    st.set_page_config(
        page_title="AI Fitness Trainer",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'rep_count' not in st.session_state:
        st.session_state.rep_count = 0
    if 'set_count' not in st.session_state:
        st.session_state.set_count = 1
    if 'total_reps' not in st.session_state:
        st.session_state.total_reps = 0
    if 'exercise_state' not in st.session_state:
        st.session_state.exercise_state = 'ready'
    if 'form_score' not in st.session_state:
        st.session_state.form_score = 100
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ''
    if 'last_rep_time' not in st.session_state:
        st.session_state.last_rep_time = time.time()
    if 'avg_rep_time' not in st.session_state:
        st.session_state.avg_rep_time = 0
    if 'is_tracking' not in st.session_state:
        st.session_state.is_tracking = False

    # App header
    st.title("💪 AI Fitness Trainer")
    st.markdown("Real-time pose estimation and form correction using MediaPipe")
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎥 Live Camera Feed")
        
        # Exercise selection with categories
        exercise_options = {}
        for key, value in EXERCISES.items():
            category = value['category']
            if category not in exercise_options:
                exercise_options[category] = []
            exercise_options[category].append((key, f"{value['name']} ({category})"))
        
        # Create selectbox with grouped exercises
        selected_category = st.selectbox(
            "Select Exercise Category",
            list(exercise_options.keys())
        )
        
        selected_exercise = st.selectbox(
            "Select Exercise",
            [ex[0] for ex in exercise_options[selected_category]],
            format_func=lambda x: EXERCISES[x]['name']
        )
        
        # Settings
        with st.expander("⚙️ Settings", expanded=False):
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=0.1,
                max_value=1.0,
                value=0.5,
                step=0.1,
                help="Minimum confidence for pose detection"
            )
            
            feedback_sensitivity = st.slider(
                "Feedback Sensitivity",
                min_value=0.1,
                max_value=1.0,
                value=0.5,
                step=0.1,
                help="Sensitivity of form feedback"
            )
        
        # WebRTC streamer
        webrtc_ctx = webrtc_streamer(
            key="pose-detection",
            video_transformer_factory=PoseTransformer,
            rtc_configuration=RTCConfiguration({
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            }),
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        if webrtc_ctx.state.playing:
            st.session_state.is_tracking = True
        else:
            st.session_state.is_tracking = False
    
    with col2:
        st.subheader("📊 Progress Tracking")
        
        # Rep and Set counters
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Reps", st.session_state.rep_count, delta=None)
        with col_b:
            st.metric("Sets", st.session_state.set_count, delta=None)
        
        # Form Score
        st.subheader("🎯 Form Score")
        st.progress(st.session_state.form_score / 100)
        st.metric("Score", f"{st.session_state.form_score}%")
        
        # Feedback
        st.subheader("💬 Real-time Feedback")
        if st.session_state.feedback:
            if st.session_state.form_score >= 85:
                st.success(st.session_state.feedback)
            elif st.session_state.form_score >= 70:
                st.warning(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
        else:
            st.info("Ready to start! Select an exercise and begin.")
        
        # Session Statistics
        st.subheader("📈 Session Stats")
        st.metric("Total Reps", st.session_state.total_reps)
        st.metric("Avg Rep Time", f"{st.session_state.avg_rep_time:.1f}s")
        st.metric("Current Exercise", EXERCISES[selected_exercise]['name'])
        
        # Control buttons
        st.subheader("🎮 Controls")
        col_c, col_d = st.columns(2)
        
        with col_c:
            if st.button("🔄 Reset Workout", use_container_width=True):
                st.session_state.rep_count = 0
                st.session_state.set_count = 1
                st.session_state.total_reps = 0
                st.session_state.exercise_state = 'ready'
                st.session_state.form_score = 100
                st.session_state.feedback = ''
                st.rerun()
        
        with col_d:
            if st.button("✅ Complete Set", use_container_width=True):
                st.session_state.set_count += 1
                st.session_state.rep_count = 0
                st.session_state.exercise_state = 'ready'
                st.rerun()
    
    # Exercise instructions
    st.subheader("📋 Exercise Instructions")
    exercise_info = EXERCISES[selected_exercise]
    st.info(f"**{exercise_info['name']}** - {exercise_info['category']}")
    
    # Exercise-specific tips
    exercise_tips = {
        'pushup': "Keep your back straight, lower until arms are at 90 degrees",
        'squat': "Keep knees aligned, lower until thighs are parallel to ground",
        'curl': "Maintain even motion, full range of movement",
        'plank': "Keep back straight and hips level",
        'pullup': "Pull until chin is over the bar, maintain even arm movement",
        'lunge': "Keep hips level, lower until back knee nearly touches ground",
        'press': "Press weights straight overhead with even arm movement",
        'row': "Maintain straight back while pulling weights toward chest",
        'goblet_squat': "Hold dumbbell close to chest, squat until thighs are parallel",
        'lateral_raise': "Raise arms to shoulder level, keep slight bend in elbows",
        'tricep_extension': "Extend arms fully behind head, keep elbows close",
        'front_raise': "Raise arms to shoulder level, control the movement",
        'deadlift': "Hinge at hips, keep back straight, stand tall",
        'overhead_squat': "Keep arms overhead, squat until thighs are parallel"
    }
    
    if selected_exercise in exercise_tips:
        st.write(f"💡 **Tip:** {exercise_tips[selected_exercise]}")
    
    # Status indicator
    if st.session_state.is_tracking:
        st.success("✅ Camera active - Pose detection running")
    else:
        st.warning("⚠️ Camera inactive - Click 'Start' to begin tracking")

if __name__ == "__main__":
    main() 