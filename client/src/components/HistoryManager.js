import React, { useEffect, useState } from "react";
import { getHistory, deleteImage, downloadImage } from "../api/api";
import api from "../api/api";

function HistoryManager() {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");

  const fetchHistory = async () => {
    try {
      const res = await getHistory();
      setFiles(res.data.files || []);
    } catch (err) {
      setMessage("שגיאה בטעינת ההיסטוריה");
    }
  };

  const handleDelete = async (filename) => {
    try {
      await deleteImage(filename);
      setMessage(`התמונה נמחקה: ${filename}`);
      fetchHistory();
    } catch (err) {
      setMessage(`שגיאה במחיקת התמונה: ${filename}`);
    }
  };

  const handleDownload = async (filename) => {
    try {
      const res = await downloadImage(filename);
      const blob = new Blob([res.data], { type: "image/png" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setMessage(`שגיאה בהורדת התמונה: ${filename}`);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="history-manager">
      <h2>היסטוריית תמונות</h2>
      {message && <p>{message}</p>}
      <div className="history-grid">
        {files.map((file, idx) => (
          <div className="history-thumb" key={idx}>
            <img src={`${api.defaults.baseURL}/preview/${file}`} alt={file} />
            <div className="overlay">
              <button onClick={() => handleDownload(file)}>📥</button>
              <button onClick={() => handleDelete(file)}>🗑️</button>
            </div>
          </div>
        ))}
      </div>
      <button onClick={() => deleteImage().then(fetchHistory)}>
        נקה את תיקיית התמונות
      </button>
    </div>
  );
}

export default HistoryManager;
