import React from "react";
import axios from "axios";
import Spinner from './Spinner'
import { baseURL } from "../constants";

function QuotePreview({ loading, setLoading, previewUrl, filename }) {
  const handleDownload = () => {
    if (!filename) return;
    const link = document.createElement("a");
    link.href = `${baseURL}/download/${filename}`;
    link.download = "quote.png";
    link.click();
  };

  const handleVideoDownload = async () => {
    if (!filename) return alert("📸 לא נוצרה תמונה עדיין");

    try {
      setLoading(true)
      // Request backend to generate video
      const res = await axios.post(`${baseURL}/generate-video`, {
        filename: filename,
      });

      const videoUrl = `${baseURL}:5000/${res.data.video_url}`;
      const link = document.createElement("a");
      link.href = videoUrl;
      link.download = "quote_reel.mp4";
      link.click();
    } catch (err) {
      console.error("❌ Video generation failed:", err);
      alert("⚠️ שגיאה ביצירת הווידאו");
    } finally {
      setLoading(false)
    }
  };

  return (
    <div className="preview">
      <h2>הצגה מקדימה</h2>

      {loading && <div><Spinner/></div>}

      {!loading && !previewUrl && (
        <p style={{ opacity: 0.6, fontStyle: "italic" }}>
          בחר תמונה וציטוט להצגה מקדימה
        </p>
      )}

      {!loading && previewUrl && (
        <>
          <img src={previewUrl} alt="preview" />
          <button onClick={handleDownload}>📥 הורד תמונה</button>
          <button onClick={handleVideoDownload}>🎥 יצירת וידאו והורדה</button>
        </>
      )}
    </div>
  );
}

export default QuotePreview;
