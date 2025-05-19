# 🧠 Stoic Quote Image Generator

A full-stack app to generate and manage quote images from famous thinkers and philosophers — with support for Hebrew, JSON uploads, image previews, and Instagram-ready exports.

---

## ✨ Features

- 🖼️ Upload quote JSON + images per thinker
- 🌍 Hebrew & RTL text rendering support
- 📤 Upload manager with drag & drop + progress
- 📁 Manage output history (view + clean)
- 📸 Preview + download final quote image
- 🔥 Modular Flask backend with React frontend
- 🐳 Docker-ready for deployment

---

## 🛠️ Technologies

- **Frontend**: React (JSX), CSS
- **Backend**: Flask + Pillow
- **Image Drawing**: PIL (ImageFont, ImageDraw)
- **Extras**: Docker, unittest

---

## 🚀 Getting Started

### Backend

```bash
cd server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install flask flask-cors pillow
python app.py
```

### Frontend

```bash
cd client
npm install
npm start
```

---

## 🐳 Docker Setup

```bash
cd server
docker build -t stoic-quotes-app .
docker run -p 5000:5000 stoic-quotes-app
```

---

## 📂 Folder Structure

```
server/
├── app.py
├── config.py
├── routes/
│   ├── quote_routes.py
│   ├── generate.py
│   └── manage.py
├── services/
│   └── image_service.py
├── utils/
│   └── text_utils.py
├── data/
│   ├── quotes/
│   └── images/
├── fonts/
├── assets/
├── output/
```

---

## 🔬 Testing

```bash
cd server
python -m unittest discover tests
```

---

## 🧪 Example JSON Format

**Modern Format (Preferred):**
```json
{
  "סנקה": [
    "העושר האמיתי הוא תוכן עצמי.",
    "אדם חזק יותר מהגורל."
  ]
}
```

**Legacy Format (also supported):**
```json
[
  "quote 1",
  "quote 2"
]
```

---

## 📝 License

MIT — feel free to use and modify!
