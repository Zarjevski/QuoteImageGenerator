import React from "react";
import Spinner from "./Spinner";

function QuotePreview({ loading, previewUrl, filename, quote }) {
  const handleDownload = () => {
    window.open(`http://10.100.102.8:5000/download/${filename}`, "_blank");
  };

  if (!quote) return null;

  return (
    <div className="preview">
      <h2>תצוגה מקדימה</h2>
      {loading && <Spinner />}
      {!loading && previewUrl && (
        <>
          <img src={previewUrl} alt="preview" />
          <button onClick={handleDownload}>הורד תמונה</button>
        </>
      )}
    </div>
  );
}

export default QuotePreview;
