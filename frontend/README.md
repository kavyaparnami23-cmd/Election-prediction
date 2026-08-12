# ElectionPulse AI — Full-Stack Web App

> **React JS + FastAPI** — ECI-inspired election winner prediction app

---

## 🚀 Quick Start

### 1. Start the FastAPI Backend
```powershell
# From project root (d:\Election prediction)
uvicorn api:app --reload --port 8000
```
API docs available at **http://localhost:8000/docs**

### 2. Start the React Frontend
```powershell
# In a second terminal
cd frontend
npm run dev
```
App available at **http://localhost:3000**

---

## 📁 Project Structure

```
Election prediction/
├── api.py                          ← FastAPI backend
├── frontend/
│   ├── src/
│   │   ├── main.jsx                ← React entry point
│   │   ├── App.jsx                 ← Root component
│   │   ├── index.css               ← Global design system
│   │   └── components/
│   │       ├── TopBar.jsx/css      ← ECI top bar
│   │       ├── Navbar.jsx/css      ← Sticky navbar
│   │       ├── HeroCarousel.jsx/css← Auto-rotating hero
│   │       ├── QuickLinks.jsx/css  ← ECI-style tab bar
│   │       ├── CategoryIcons.jsx/css ← 6 circular icons
│   │       ├── PredictionSection.jsx/css ← Prediction form
│   │       ├── StatsSection.jsx/css ← Stats & bar chart
│   │       └── Footer.jsx/css      ← 4-col footer
│   └── vite.config.js              ← Dev proxy → :8000
├── src/                            ← ML model code
└── artifacts/models/               ← Trained .pkl files
```

## 🎨 Design

- **Color palette**: Navy `#0f1b4c` · Purple `#6b21a8` · Orange `#f97316` · Teal `#0d9488`
- **Typography**: Poppins (headings) + Noto Sans (body)
- **Features**: Hero carousel, ECI category circles, prediction form with result card, stats bar chart
