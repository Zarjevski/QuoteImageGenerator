import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import CreatePage from "./pages/CreatePage";
import UploadPage from "./pages/UploadPage";
import HistoryPage from "./pages/HistoryPage";
import "./styles/App.css";

function App() {
  const [language, setLanguage] = useState("he");

  return (
    <Router>
      <Navbar language={language} onLanguageChange={setLanguage} />
      <Routes>
        <Route path="/" element={<CreatePage language={language} />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
    </Router>
  );
}

export default App;
