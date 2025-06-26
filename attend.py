import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
import threading
import pickle
from PIL import Image, ImageTk
import tkinter.font as tkFont

class FaceRecognitionAttendance:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1100x750")
        self.root.configure(bg='#181A20')
        self.root.minsize(1000, 700)
        self.primary = '#00E0FF'
        self.secondary = '#23272F'
        self.accent = '#00FFA3'
        self.danger = '#FF4C60'
        self.warning = '#FFD600'
        self.font_main = tkFont.Font(family="Segoe UI", size=12)
        self.font_title = tkFont.Font(family="Segoe UI", size=28, weight="bold")
        self.font_subtitle = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.font_button = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.font_list = tkFont.Font(family="Consolas", size=11)
        
        # Initialize variables
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_samples = []
        self.face_labels = []
        self.label_names = {}
        self.next_label = 0
        self.attendance_records = []
        self.video_capture = None
        self.is_recording = False
        self.faces_dir = "faces_db"
        self.attendance_file = "attendance.csv"
        self.model_file = "face_model.yml"
        
        # Load existing faces and model
        self.load_faces()
        self.load_model()
        
        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        self.root.configure(bg=self.secondary)
        
        # Title
        title_label = tk.Label(self.root, text="AttendaFace📸", 
                              font=self.font_title, fg=self.primary, bg=self.secondary)
        title_label.pack(pady=25)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.secondary)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Left panel for video
        video_frame = tk.Frame(main_frame, bg=self.secondary, relief=tk.RAISED, bd=0, highlightbackground=self.primary, highlightthickness=2)
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 18), pady=10)
        
        video_label = tk.Label(video_frame, text="Camera Feed", 
                              font=self.font_subtitle, fg=self.accent, bg=self.secondary)
        video_label.pack(pady=10)
        
        self.video_label = tk.Label(video_frame, bg='#101215', width=60, height=20, relief=tk.FLAT, bd=0)
        self.video_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Video controls
        video_controls = tk.Frame(video_frame, bg=self.secondary)
        video_controls.pack(pady=10)
        
        self.start_button = tk.Button(video_controls, text="Start Camera", 
                                     command=self.start_camera, bg=self.primary, 
                                     fg='#181A20', font=self.font_button,
                                     width=14, height=2, bd=0, activebackground=self.accent,
                                     activeforeground='#181A20', relief=tk.FLAT, cursor="hand2")
        self.start_button.pack(side=tk.LEFT, padx=8)
        
        self.stop_button = tk.Button(video_controls, text="Stop Camera", 
                                    command=self.stop_camera, bg=self.danger, 
                                    fg='white', font=self.font_button,
                                    width=14, height=2, bd=0, activebackground='#FF7A8A',
                                    activeforeground='white', relief=tk.FLAT, cursor="hand2", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=8)
        
        # Right panel for controls and data
        control_frame = tk.Frame(main_frame, bg=self.secondary, relief=tk.RAISED, bd=0, highlightbackground=self.primary, highlightthickness=2)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(18, 0), pady=10)
        
        # Registration section
        reg_label = tk.Label(control_frame, text="Register New Person", 
                            font=self.font_subtitle, fg=self.primary, bg=self.secondary)
        reg_label.pack(pady=(30, 10))
        
        tk.Label(control_frame, text="Name:", fg="white", bg=self.secondary, 
                font=self.font_main).pack()
        self.name_entry = tk.Entry(control_frame, font=self.font_main, width=22, bg='#23272F', fg='white',
                                  insertbackground=self.primary, relief=tk.FLAT, highlightthickness=2,
                                  highlightbackground=self.primary, highlightcolor=self.accent)
        self.name_entry.pack(pady=7)
        
        self.register_button = tk.Button(control_frame, text="Add Photo", 
                                        command=self.register_face, bg=self.accent, 
                                        fg='#181A20', font=self.font_button,
                                        width=16, bd=0, activebackground=self.primary,
                                        activeforeground='#181A20', relief=tk.FLAT, cursor="hand2")
        self.register_button.pack(pady=7)
        
        # Attendance section
        att_label = tk.Label(control_frame, text="Attendance Records", 
                            font=self.font_subtitle, fg=self.primary, bg=self.secondary)
        att_label.pack(pady=(35, 10))
        
        # Attendance listbox with scrollbar
        list_frame = tk.Frame(control_frame, bg=self.secondary)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.attendance_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                           font=self.font_list, height=15, width=38, bg='#101215',
                                           fg=self.accent, selectbackground=self.primary,
                                           selectforeground='#181A20', relief=tk.FLAT, bd=0, highlightthickness=0)
        self.attendance_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.attendance_listbox.yview)
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg=self.secondary)
        button_frame.pack(pady=12)
        
        self.export_button = tk.Button(button_frame, text="Export CSV", 
                                      command=self.export_csv, bg=self.warning, 
                                      fg='#181A20', font=self.font_button,
                                      width=16, bd=0, activebackground='#FFF380',
                                      activeforeground='#181A20', relief=tk.FLAT, cursor="hand2")
        self.export_button.pack(pady=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear Records", 
                                     command=self.clear_records, bg=self.danger, 
                                     fg='white', font=self.font_button,
                                     width=16, bd=0, activebackground='#FF7A8A',
                                     activeforeground='white', relief=tk.FLAT, cursor="hand2")
        self.clear_button.pack(pady=5)
        
        # Stats
        stats_frame = tk.Frame(control_frame, bg=self.secondary)
        stats_frame.pack(pady=15)
        
        self.stats_label = tk.Label(stats_frame, text="Registered: 0 | Today: 0", 
                                   fg=self.accent, bg=self.secondary, font=self.font_main)
        self.stats_label.pack()
        
        self.update_stats()
        
    def load_faces(self):
        """Load face images and labels from faces_db directory"""
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
        label = 0
        for name in os.listdir(self.faces_dir):
            person_dir = os.path.join(self.faces_dir, name)
            if os.path.isdir(person_dir):
                self.label_names[label] = name
                for img_file in os.listdir(person_dir):
                    img_path = os.path.join(person_dir, img_file)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        self.face_samples.append(img)
                        self.face_labels.append(label)
                label += 1
        self.next_label = label

    def save_model(self):
        """Save the trained model"""
        if self.face_samples and self.face_labels:
            self.recognizer.train(self.face_samples, np.array(self.face_labels))
            self.recognizer.save(self.model_file)
            with open("label_names.pkl", "wb") as f:
                pickle.dump(self.label_names, f)

    def load_model(self):
        """Load the trained model if exists"""
        if os.path.exists(self.model_file):
            self.recognizer.read(self.model_file)
            if os.path.exists("label_names.pkl"):
                with open("label_names.pkl", "rb") as f:
                    self.label_names = pickle.load(f)

    def register_face(self):
        """Register a new face from photo"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return
            
        # Ask for photo file
        file_path = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not file_path:
            return
            
        try:
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                messagebox.showerror("Error", "No face detected in the image")
                return
            elif len(faces) > 1:
                messagebox.showwarning("Warning", "Multiple faces detected. Using the first one.")
            
            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            person_dir = os.path.join(self.faces_dir, name)
            if not os.path.exists(person_dir):
                os.makedirs(person_dir)
                label = self.next_label
                self.label_names[label] = name
                self.next_label += 1
            else:
                # Find label for this name
                label = [k for k, v in self.label_names.items() if v == name][0]
            img_count = len(os.listdir(person_dir))
            img_save_path = os.path.join(person_dir, f"face_{img_count+1}.png")
            cv2.imwrite(img_save_path, face_img)
            self.face_samples.append(face_img)
            self.face_labels.append(label)
            self.save_model()
            self.name_entry.delete(0, tk.END)
            self.update_stats()
            
            messagebox.showinfo("Success", f"Face registered successfully for {name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register face: {str(e)}")
            
    def start_camera(self):
        """Start the camera feed"""
        try:
            self.video_capture = cv2.VideoCapture(0)
            if not self.video_capture.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                return
                
            self.is_recording = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start video thread
            self.video_thread = threading.Thread(target=self.update_video)
            self.video_thread.daemon = True
            self.video_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            
    def stop_camera(self):
        """Stop the camera feed"""
        self.is_recording = False
        if self.video_capture:
            self.video_capture.release()
            
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Clear video display
        self.video_label.config(image='', text="Camera Stopped", fg='white')
        
    def update_video(self):
        """Update video feed and perform face recognition"""
        while self.is_recording:
            ret, frame = self.video_capture.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            face_names = []
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                label, confidence = self.recognizer.predict(face_img) if self.face_samples else (-1, 100)
                if label in self.label_names and confidence < 70:
                    name = self.label_names[label]
                    self.mark_attendance(name)
                else:
                    name = "Unknown"
                face_names.append((x, y, w, h, name))
            
            # Draw rectangles and names
            for (x, y, w, h, name) in face_names:
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (x + 6, y + h - 6), font, 0.6, (255, 255, 255), 1)
            
            # Convert to PIL format for tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_pil = frame_pil.resize((480, 360), Image.Resampling.LANCZOS)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            
            # Update GUI
            self.video_label.config(image=frame_tk, text='')
            self.video_label.image = frame_tk
            
    def mark_attendance(self, name):
        """Mark attendance for a person"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Check if already marked today
        today_records = [record for record in self.attendance_records 
                        if record['name'] == name and record['date'] == date_str]
        
        if not today_records:
            record = {
                'name': name,
                'date': date_str,
                'time': time_str,
                'status': 'Present'
            }
            self.attendance_records.append(record)
            
            # Update GUI
            display_text = f"{name} - {date_str} {time_str}"
            self.attendance_listbox.insert(0, display_text)
            self.update_stats()
            
            print(f"Attendance marked for {name} at {time_str}")
            
    def export_csv(self):
        """Export attendance records to CSV"""
        if not self.attendance_records:
            messagebox.showwarning("Warning", "No attendance records to export")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Attendance Report"
            )
            
            if file_path:
                with open(file_path, 'w', newline='') as csvfile:
                    fieldnames = ['name', 'date', 'time', 'status']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for record in self.attendance_records:
                        writer.writerow(record)
                        
                messagebox.showinfo("Success", f"Attendance exported to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")
            
    def clear_records(self):
        """Clear all attendance records"""
        result = messagebox.askyesno("Confirm", "Are you sure you want to clear all attendance records?")
        if result:
            self.attendance_records.clear()
            self.attendance_listbox.delete(0, tk.END)
            self.update_stats()
            
    def update_stats(self):
        """Update statistics display"""
        registered_count = len(self.label_names)
        today = datetime.now().strftime("%Y-%m-%d")
        today_count = len([r for r in self.attendance_records if r['date'] == today])
        
        self.stats_label.config(text=f"Registered: {registered_count} | Today: {today_count}")
        
    def run(self):
        """Start the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
            
    def on_closing(self):
        """Handle application closing"""
        if self.is_recording:
            self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    # Install required packages if not available
    try:
        import cv2
        from PIL import Image, ImageTk
    except ImportError as e:
        print("Missing required packages. Please install:")
        print("pip install opencv-python pillow")
        exit(1)
    
    app = FaceRecognitionAttendance()
    app.run()