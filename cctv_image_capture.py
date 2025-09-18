import cv2
import time
import subprocess
import os
import sys

# Optional: Uncomment if you want to support full Unicode in terminal
# sys.stdout.reconfigure(encoding='utf-8')

def capture_image(camera_index, output_path):
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("[ERROR] Could not open camera.")
        return False
    
    ret, frame = cap.read()
    
    if not ret:
        print("[ERROR] Could not read frame from camera.")
        return False

    # Flip image vertically and horizontally to correct orientation
    corrected_frame = cv2.flip(frame, -1)

    # Save flipped image
    cv2.imwrite(output_path, corrected_frame)
    cap.release()
    print("[INFO] Image captured and saved as", output_path)
    return True

def enhance_image_with_esrgan(input_path, output_path):
    esrgan_path = r"C:\Users\Asus\Downloads\Smart-Adaptive-Traffic-Management-System-main\Smart-Adaptive-Traffic-Management-System-main\ESRGAN"
    
    model_path = os.path.join(esrgan_path, "models", "RRDB_PSNR_x4.pth")
    if not os.path.exists(model_path):
        print(f"[ERROR] Model not found: {model_path}")
        return

    command = [
        "python", "test.py",
        "--input", input_path,
        "--output", output_path,
        "--model_path", model_path
    ]

    print("[INFO] Enhancing image with ESRGAN...")
    print("Command:", ' '.join(command))
    print("Working directory:", esrgan_path)

    try:
        result = subprocess.run(command, cwd=esrgan_path, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print("[INFO] Enhanced image saved as", output_path)
        else:
            print("[ERROR] ESRGAN failed with error:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("[ERROR] ESRGAN process timed out after 60 seconds.")
    except Exception as e:
        print("[ERROR] An unexpected error occurred while running ESRGAN:", str(e))

def main():
    camera_index = 0
    interval_seconds = 5

    while True:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        image_filename = f"captured_image_{timestamp}.jpg"
        enhanced_filename = f"enhanced_image_{timestamp}.jpg"

        if capture_image(camera_index, image_filename):
            enhance_image_with_esrgan(image_filename, enhanced_filename)
        
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
