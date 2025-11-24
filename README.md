---

# 🌤️ **Vayu – Weather Forecast Dashboard**

A modern, fast, and interactive weather dashboard built with **Streamlit** and **WeatherAPI**, providing real-time weather updates with a clean UI, autocomplete search, loading skeletons, and dynamic data display.

---

## 📌 **Live Demo**

👉 **[Open the Live App](https://weather-forecast-dashboard-8xnaskborlr9juynhvjqjr.streamlit.app/)**

---

## 🟩 **CI/CD Status**

![CI](https://github.com/kirtanshah24/weather-forecast-dashboard/actions/workflows/ci.yml/badge.svg)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://weather-forecast-dashboard-8xnaskborlr9juynhvjqjr.streamlit.app/)

The app uses:

* **GitHub Actions** for Continuous Integration
* **Streamlit Cloud** for Continuous Deployment

Every push to the `main` branch automatically triggers:

* Code checks & dependency installs
* Test execution
* Streamlit Cloud auto-redeployment

---

# 🌟 **Features**

### 🔍 Smart City Search with Autocomplete

Search cities worldwide with instant suggestions using WeatherAPI’s search endpoint.

### 🌦 Real-Time Weather Data

Displays:

* Temperature
* Humidity
* Feels Like
* Wind Speed
* Weather Condition
* Icons

### ⚡ Loading Skeletons for Better UX

Beautiful placeholders while fetching data.

### ♻ Refresh & Clear Search Options

Instantly reload weather data or reset the search.

### 🎨 Clean UI + Smooth Interactions

Powered by **Streamlit** with a minimal, modern design.

---

# 🧱 **Tech Stack**

### **Frontend / UI**

* Streamlit

### **Backend**

* Python
* WeatherAPI (External API)

### **DevOps / CI/CD**

* GitHub Actions
* Streamlit Cloud Deployment

---

# 🚀 **Project Structure**

```
weather-forecast-dashboard/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── utils/
│   ├── api.py
│   └── __init__.py
└── .github/
    └── workflows/
        └── ci.yml
```

---

# 🔧 **Installation & Setup (Local Development)**

### **1. Clone the repository**

```bash
git clone https://github.com/kirtanshah24/weather-forecast-dashboard.git
cd weather-forecast-dashboard
```

### **2. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Add your API key**

Create a `.env` file (local only):

```
WEATHER_API_KEY=your_api_key_here
```

### **5. Run the app**

```bash
streamlit run app.py
```

---

# 🔒 **Environment Variables (for deployment)**

In **Streamlit Cloud**, add this in:

`Settings → Secrets`

```
WEATHER_API_KEY = "your_real_api_key"
```

---

# 🔁 **CI/CD Pipeline Overview**

### ✔ **Continuous Integration (GitHub Actions)**

* Workflow located at `.github/workflows/ci.yml`
* Runs on every push or PR to `main`
* Installs dependencies
* Runs basic tests
* Ensures the app builds successfully

### ✔ **Continuous Deployment (Streamlit Cloud)**

* Automatically deploys on every push to main
* Uses `runtime.txt` to pin Python version
* Secrets stored securely via Streamlit Secrets Manager

---

# 🧪 **Running Tests** (optional)

A basic test file:

```
tests/test_basic.py
```

Example:

```python
def test_app_imports():
    import app
    assert True
```

Run tests:

```bash
pytest
```

---

# 👨‍💻 **Author**

**Kirtan Shah & Vraj Patel**

---
