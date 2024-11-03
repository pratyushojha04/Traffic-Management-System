Here's the README content in plain text:

---

**Traffic Management System**

This project is an AI-powered Traffic Management System that uses YOLO (You Only Look Once), Convolutional Neural Networks (CNNs), and OpenCV to detect and manage traffic flow. The Django framework is used to provide a user interface (UI) for visualizing and managing traffic data, with real-time monitoring and adaptive traffic control.

---

**Table of Contents**

1. Introduction
2. Features
3. Tech Stack
4. Installation
5. Usage
6. Project Structure
7. Screenshots
8. License

---

**Introduction**

The Traffic Management System is designed to improve road efficiency by dynamically managing traffic lights based on real-time congestion detection and prioritizing emergency vehicles. This solution aims to help mitigate traffic congestion, reduce commute times, and improve safety at busy intersections.

Key objectives of the system:
- Monitor traffic density on multiple lanes.
- Detect vehicles, including emergency vehicles like ambulances or fire trucks.
- Optimize traffic light signals to allow smoother traffic flow based on real-time conditions.

---

**Features**

- Real-time vehicle detection using YOLO and CNN models.
- Dynamic traffic light control based on vehicle density.
- Emergency vehicle detection with priority-based traffic light adjustments.
- Django-based UI for monitoring traffic and vehicle counts in real-time.
- Data logging and visualization for traffic patterns.

---

**Tech Stack**

- **Frontend**: HTML, CSS, JavaScript (for Django templates)
- **Backend**: Django (Python)
- **Machine Learning / Computer Vision**: YOLOv8, CNN, OpenCV
- **Database**: SQLite (default with Django, configurable to other databases)
- **Deployment**: Compatible with Docker, Apache, or Nginx for production setup

---

**Installation**

**Prerequisites**:
- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)
- MongoDB (if using a different database, adjust settings accordingly)

**Steps**:

1. **Clone the repository**  
   `git clone https://github.com/pratyushojha04/traffic-management-system.git`  
   `cd traffic-management-system`

2. **Create a virtual environment**  
   `python3 -m venv venv`  
   `source venv/bin/activate`

3. **Install dependencies**  
   `pip install -r requirements.txt`

4. **Set up YOLO model files**  
   Download the YOLOv8 model weights and place them in the designated model folder.

5. **Run Migrations**  
   `python manage.py migrate`

6. **Start the Django Server**  
   `python manage.py runserver`

7. **Access the Application**  
   Open your web browser and go to `http://127.0.0.1:8000`.

---

**Usage**

1. **Starting the System**  
   Run the Django server to access the web interface.  
   The dashboard displays real-time video feeds and traffic conditions.

2. **Managing Traffic**  
   The system detects vehicles on each lane.  
   When an emergency vehicle is detected, traffic signals adjust to allow priority passage.

3. **Viewing Traffic Statistics**  
   Use the dashboard to review vehicle counts, congestion patterns, and traffic light timings.

---

**Project Structure**

```
traffic-management-system/
│
├── manage.py                # Django management script
├── traffic_management/      # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # Views for handling UI and backend logic
│   ├── templates/           # HTML templates for the Django frontend
│   └── static/              # Static files (CSS, JS)
│
├── detection/               # Traffic detection and YOLO integration
│   ├── yolo_model.py        # YOLO model and OpenCV integration
│   └── utils.py             # Helper functions for vehicle detection
│
└── README                   # Project README file
```

---


**License**

This project is licensed under the MIT License. See the LICENSE file for details.

---
