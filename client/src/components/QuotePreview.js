import React from "react";
import { downloadImage } from "../api/api";

function QuotePreview({ loading, previewUrl, filename, quote }) {
  const handleDownload = async () => {
    if (!filename) return;

    try {
      const res = await downloadImage(filename);
      const blob = new Blob([res.data], { type: "image/png" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "quote.png";
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
    }
  };

  return (
    <div className="preview">
      <h2>הצגה מקדימה</h2>

      {loading && <p>טוען...</p>}

      {!loading && !previewUrl && (
        <p style={{ opacity: 0.6, fontStyle: "italic" }}>
          בחר תמונה וציטוט להצגה מקדימה
        </p>
      )}

      {!loading && previewUrl && (
        <>
          <img src={previewUrl} alt="preview" />
          <button onClick={handleDownload}>📥 הורד</button>
        </>
      )}
    </div>
  );
}

export default QuotePreview;
