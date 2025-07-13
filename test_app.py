#!/usr/bin/env python3
"""
Test script to verify all dependencies and basic functionality
"""

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import streamlit: {e}")
        return False
    
    try:
        from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
        print("✅ streamlit-webrtc imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import streamlit-webrtc: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import numpy: {e}")
        return False
    
    try:
        import cv2
        print("✅ opencv-python imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import opencv-python: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✅ mediapipe imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import mediapipe: {e}")
        return False
    
    try:
        import av
        print("✅ av imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import av: {e}")
        return False
    
    return True

def test_exercise_utils():
    """Test that exercise utilities can be imported and work"""
    try:
        from exercise_utils import EXERCISES, calculate_angle
        print("✅ exercise_utils imported successfully")
        
        # Test exercise definitions
        expected_exercises = ['pushup', 'squat', 'curl', 'plank', 'pullup', 'lunge', 'press', 'row']
        for exercise in expected_exercises:
            if exercise in EXERCISES:
                print(f"✅ Exercise '{exercise}' found")
            else:
                print(f"❌ Exercise '{exercise}' missing")
                return False
        
        # Test angle calculation
        class MockLandmark:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        a = MockLandmark(0, 0)
        b = MockLandmark(1, 0)
        c = MockLandmark(1, 1)
        
        angle = calculate_angle(a, b, c)
        if 80 < angle < 100:  # Should be approximately 90 degrees
            print("✅ Angle calculation working correctly")
        else:
            print(f"❌ Angle calculation failed: got {angle}, expected ~90")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import exercise_utils: {e}")
        return False

def test_mediapipe_pose():
    """Test that MediaPipe pose detection can be initialized"""
    try:
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✅ MediaPipe pose detection initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize MediaPipe pose: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing AI Fitness Trainer Dependencies")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Exercise Utilities", test_exercise_utils),
        ("MediaPipe Pose", test_mediapipe_pose),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app should work correctly.")
        print("\n🚀 To run the app:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("\n💡 Try installing missing dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main() 