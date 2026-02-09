# 🧠 Stoic Quote Image Generator

A full-stack app to generate and manage quote images from famous thinkers and philosophers — with support for Hebrew, JSON uploads, image previews, and Instagram-ready exports.

---

## ✨ Features

- 🖼️ Upload quote JSON + images per thinker
- 🌍 Hebrew & RTL text rendering support
- 📤 Upload manager with drag & drop + progress
- 📁 Manage output history (view + clean)
- 📸 Preview + download final quote image
- 🎥 Video generation for social media
- 🔒 Security improvements (input validation, path traversal protection)
- ♿ Accessibility features (keyboard navigation, ARIA labels)
- 🐳 Docker-ready for deployment
- ⚙️ Environment variable configuration

---

## 🛠️ Technologies

- **Frontend**: React (JSX), CSS
- **Backend**: Flask + Pillow
- **Image Drawing**: PIL (ImageFont, ImageDraw)
- **Extras**: Docker, unittest

---

## 🚀 Getting Started

### Quick Start (Recommended)

**For Linux/macOS:**
```bash
./scripts/start-dev.sh
```

**For Windows (PowerShell):**
```powershell
.\scripts\start-dev.ps1
```

**For Windows (Command Prompt):**
```cmd
scripts\start-dev.bat
```

**Using npm (Cross-Platform):**
```bash
npm install  # Install concurrently (first time only)
npm run dev  # Start both servers
```

The scripts will automatically:
- ✅ Check for Python and Node.js
- ✅ Create virtual environment if needed
- ✅ Install dependencies if missing
- ✅ Start both backend and frontend servers

> 📖 See [DEV_SCRIPTS.md](DEV_SCRIPTS.md) for detailed documentation and troubleshooting.

### Manual Setup

#### Backend

1. **Set up virtual environment:**
```bash
cd server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables (optional):**
Create a `.env` file in the `server` directory:
```env
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
OPENAI_API_KEY=your_key_here  # Optional, for AI features
```

4. **Run the server:**
```bash
python app.py
```

#### Frontend

1. **Install dependencies:**
```bash
cd client
npm install
```

2. **Configure API URL (optional):**
Create a `.env` file in the `client` directory:
```env
REACT_APP_API_URL=http://127.0.0.1:5000
```

3. **Start the development server:**
```bash
npm start
```

---

## 🐳 Docker Setup

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

This will start both the backend (port 5055) and frontend (port 3300).

### Manual Docker Setup

**Backend:**
```bash
cd server
docker build -t stoic-quotes-app .
docker run -p 5000:5000 stoic-quotes-app
```

**Frontend:**
```bash
cd client
docker build -t stoic-quotes-client .
docker run -p 3000:3000 stoic-quotes-client
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
