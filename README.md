# 📸 AttendaFace - Face Recognition Attendance System

**AttendaFace** is a Python-based desktop application that uses **OpenCV** and **LBPH face recognition** to automate attendance tracking in classrooms, offices, or events. The application features a modern GUI with photo-based face registration, real-time recognition, attendance logging, and CSV export.

---

## 🚀 Features

- 🧠 **Real-time Face Recognition** using webcam
- 🔐 **LBPH Model Training & Persistence**
- 🖼️ **Add New Faces** with a photo
- 📝 **CSV Export** of attendance data
- 🔁 **No Duplicate Attendance** for the same person on the same day
- 🖥️ **Modern GUI** using Tkinter
- 📊 **Live Stats** for Registered Users and Today's Attendance
- 📂 Stores face data locally with a labeled directory structure

---

## 🛠️ Tech Stack

| Component        | Technology                |
|------------------|----------------------------|
| GUI              | Tkinter                    |
| Face Detection   | OpenCV Haar Cascades       |
| Face Recognition | OpenCV LBPH Face Recognizer|
| Image Handling   | Pillow (PIL)               |
| File Storage     | CSV and Local Filesystem   |
| Model Saving     | `.yml` and `.pkl` files    |

---
## 📁 Folder Structure

```
AttendaFace/
├── attend.py               # Main application
├── face_model.yml          # Trained face recognition model
├── label_names.pkl         # Pickled name-label mappings
├── faces_db/               # Directory of registered user face images
│   ├── Alice/
│   │   └── face_1.png
│   └── Bob/
│       └── face_1.png
├── attendance.csv          # Optional exported attendance log
└── README.md               # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dipenginedev7/AttendaFace.git
cd AttendaFace
```

### 2. Install Requirements

Install the required Python packages:

```bash
pip install opencv-python opencv-contrib-python pillow
```

> 💡 `opencv-contrib-python` is required to access `cv2.face.LBPHFaceRecognizer_create`.

---

## ▶️ Run the Application

```bash
python attend.py
```

The app will launch a GUI with buttons to start/stop the camera, register new users, and export attendance records.

---

## 👤 Register a New Person

1. Type the person's name in the "Name" field.
2. Click "Add Photo" and select a front-facing image.
3. The app detects and stores the face, updating the model automatically.
4. You’ll receive a confirmation message upon successful registration.

---

## 🧾 Attendance Logging

- Launch the camera by clicking "Start Camera".
- When a registered face is recognized:
  - Name, Date, and Time are logged.
  - Duplicate entries are prevented for the same day.
- Click "Export CSV" to save attendance records.

**CSV Format Example:**
```csv
name,date,time,status
Alice,2025-06-26,10:05:23,Present
Bob,2025-06-26,10:12:01,Present
```

---

## 📊 GUI Stats

At the bottom of the control panel, the GUI shows:
- **Registered:** Total registered users
- **Today:** Attendance count for today

---

## 🧩 Future Roadmap

- Webcam-based face registration
- Face dataset augmentation
- Role-based access or admin login
- Calendar-based attendance filtering
- Cloud/DB integration (SQLite, Firebase, etc.)
- Export as Excel or PDF

---

## 🧰 Troubleshooting

- **"cv2.face" module not found?**
  - Make sure you installed `opencv-contrib-python` and not just `opencv-python`.
- **Face not detected during registration?**
  - Ensure the image is well-lit, clear, and front-facing.
- **GUI not launching?**
  - Ensure you're running Python 3 and all dependencies are installed.

---

## 📜 License

This project is licensed under the MIT License.  
Feel free to use, modify, and distribute it with attribution.

---

## 🙌 Acknowledgements

- OpenCV
- Pillow
- The Python community 💙

Built with 💻 Python and a vision to modernize attendance systems.



