import React, { memo } from "react";
import axios from "axios";
import Spinner from './Spinner';
import { baseURL } from "../constants";

function QuotePreview({ loading, setLoading, previewUrl, filename, quote }) {
  const handleDownload = () => {
    if (!filename) {
      alert("📸 לא נוצרה תמונה עדיין");
      return;
    }
    
    try {
      const link = document.createElement("a");
      link.href = `${baseURL}/download/${filename}`;
      link.download = "quote.png";
      link.click();
    } catch (err) {
      alert("שגיאה בהורדת התמונה");
    }
  };

  const handleVideoDownload = async () => {
    if (!filename) {
      alert("📸 לא נוצרה תמונה עדיין");
      return;
    }

    try {
      setLoading(true);
      // Request backend to generate video
      const res = await axios.post(`${baseURL}/generate-video`, {
        filename: filename,
      });

      if (res.data?.video_url) {
        const videoUrl = `${baseURL}/${res.data.video_url}`;
        // Open video in a new tab instead of downloading
        window.open(videoUrl, '_blank', 'noopener,noreferrer');
      } else {
        throw new Error("No video URL in response");
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || "שגיאה ביצירת הווידאו";
      alert(`⚠️ ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="preview" role="region" aria-label="תצוגה מקדימה">
      <h2>הצגה מקדימה</h2>

      {loading && (
        <div role="status" aria-live="polite">
          <Spinner />
        </div>
      )}

      {!loading && !previewUrl && (
        <p style={{ opacity: 0.6, fontStyle: "italic" }} aria-live="polite">
          בחר תמונה וציטוט להצגה מקדימה
        </p>
      )}

      {!loading && previewUrl && (
        <>
          <img 
            src={previewUrl} 
            alt={quote ? `תצוגה מקדימה: ${quote.substring(0, 50)}...` : "תצוגה מקדימה של ציטוט"} 
            loading="lazy"
          />
          <div style={{ 
            display: "flex", 
            gap: "12px", 
            flexWrap: "wrap", 
            justifyContent: "center",
            width: "100%",
            marginTop: "8px"
          }}>
            <button 
              onClick={handleDownload}
              aria-label="הורד תמונה"
              style={{ flex: "1", minWidth: "140px" }}
            >
              📥 הורד תמונה
            </button>
            <button 
              onClick={handleVideoDownload}
              aria-label="יצירת וידאו וצפייה"
              disabled={loading}
              style={{ flex: "1", minWidth: "140px" }}
            >
              🎥 יצירת וידאו וצפייה
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default memo(QuotePreview);
