# 🕵️ Anomaly Control

**Secure. Contain. Protect.**  
A fullstack web application for managing and exploring anomalies inspired by the SCP Foundation universe.  
Users can browse classified files, view containment procedures, and access restricted data based on their clearance level.  

---

## 📖 About

**Anomaly Control** is a fictional database system designed to simulate how a secret organization might track and manage dangerous or mysterious anomalies.  

The app combines **Django (backend)** and optionally **FastAPI / React (frontend)** to provide:  
- A secure anomaly archive  
- Clearance-based access restrictions  
- An immersive experience for fans of mysterious phenomena  

Core focus:  
- **Secure** anomalies in a structured system  
- **Contain** them with detailed procedures  
- **Protect** humanity by limiting access through clearance levels  

---

## 🚀 Features (MVP)

- 🔑 User authentication & clearance levels (1–5)  
- 📂 Anomaly entries with:
  - ID (e.g., AC-173)  
  - Classification (Safe, Euclid, Keter, etc.)  
  - Containment procedures  
  - Description  
  - Optional media (images, documents)  
- 🛠️ Admin dashboard for managing anomalies  
- 🌐 REST API endpoints for anomaly data  

---

## 🌟 Future Features

- 📜 Incident Reports linked to anomalies  
- 👤 Personnel management (researchers, agents, security staff)  
- 🧪 Experiment logs & ethics reviews  
- 🏢 Facility/Site database with assigned anomalies  
- 🕵️ Groups of Interest (GoIs) and anomaly conflicts  
- 🎲 “File of the Day” anomaly spotlight  
- 🔒 Classified sections that unlock with higher clearance  

---

## 🗂️ Data Models (MVP)

### User
- `id` (int, PK)  
- `username` (string)  
- `email` (string)  
- `password` (hashed)  
- `clearance_level` (int: 1–5)  

### Classification
- `id` (int, PK)  
- `name` (string: Safe, Euclid, Keter, Neutralized, etc.)  
- `description` (text)  

### Anomaly
- `id` (int, PK)  
- `anomaly_id` (string, e.g., AC-001)  
- `name` (string)  
- `classification_id` (FK → Classification)  
- `containment_procedures` (text)  
- `description` (text)  
- `image` (file, optional)  
- `status` (string: Active, Neutralized, Pending)  

---

## 🛠️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/anomaly-control.git
   cd anomaly-control
