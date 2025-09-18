from flask import Flask, render_template, request, redirect, url_for
import subprocess
import signal
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store CCTV process PID
cctv_process_pid_file = "cctv_pid.txt"

# Set the absolute path to your scripts directory
SCRIPT_DIR = r'C:\Users\Asus\OneDrive\Desktop\college\Smart-Adaptive-Traffic-Management-System-main\Smart-Adaptive-Traffic-Management-System-main'

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = request.args.get('image_url', None)
    result = request.args.get('result', '')
    message = request.args.get('message', '')

    if request.method == 'POST' and 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(file_path)
            image_url = f'/static/uploads/{filename}'
            return redirect(url_for('index', image_url=image_url))

    return render_template('index.html', image_url=image_url, result=result, message=message)

def run_script(script_path, success_msg, fail_msg, save_pid=False):
    try:
        process = subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        if save_pid:
            with open(cctv_process_pid_file, 'w') as f:
                f.write(str(process.pid))

        output, error = process.communicate()
        if process.returncode == 0:
            return success_msg, output.decode("utf-8")
        else:
            return fail_msg, error.decode("utf-8")
    except Exception as e:
        return fail_msg, str(e)

@app.route('/run-script/<script>', methods=['POST'])
def run_script_route(script):
    script_map = {
        "vehicle": (
            os.path.join(SCRIPT_DIR, "vehicle_detection.py"),
            "Vehicle Detection Completed.",
            "Vehicle Detection Failed.",
            False
        ),
        "green": (
            os.path.join(SCRIPT_DIR, "green_time_signal.py"),
            "Green Time Signal Completed.",
            "Green Time Signal Failed.",
            False
        ),
        "cctv": (
            os.path.join(SCRIPT_DIR, "cctv_image_capture.py"),
            "CCTV Image Capture Started.",
            "CCTV Capture Failed.",
            True
        ),
        "analyze": (
            os.path.join(SCRIPT_DIR, "scripts", "analyze_vehicle_data.py"),
            "Data Analysis Completed.",
            "Data Analysis Failed.",
            False
        ),
        "graph": (
            os.path.join(SCRIPT_DIR, "scripts", "generate_knowledge_graph.py"),
            "Knowledge Graph Generated.",
            "Knowledge Graph Failed.",
            False
        ),
        "nlp": (
            os.path.join(SCRIPT_DIR, "scripts", "generate_nlp_summary.py"),
            "NLP Summary Generated.",
            "NLP Summary Failed.",
            False
        ),
    }

    if script in script_map:
        script_file, success_msg, fail_msg, save_pid = script_map[script]
        message, result = run_script(script_file, success_msg, fail_msg, save_pid)
        return redirect(url_for("index", result=result, message=message))

    return redirect(url_for("index"))

@app.route('/stop-cctv', methods=['POST'])
def stop_cctv():
    try:
        if os.path.exists(cctv_process_pid_file):
            with open(cctv_process_pid_file, 'r') as f:
                pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            os.remove(cctv_process_pid_file)
            return redirect(url_for("index", message="CCTV Image Capture Stopped."))
        else:
            return render_template("index.html", message="No CCTV process running.", result="", image_url=None)
    except Exception as e:
        return render_template("index.html", message="Error stopping CCTV.", result=str(e), image_url=None)

if __name__ == '__main__':
    app.run(debug=True)
