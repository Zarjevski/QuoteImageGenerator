import React, { memo } from 'react';
import api from '../api/api';

function ImageSlider({ images, selectedImage, onSelect, thinker }) {
  if (!images || images.length === 0) {
    return (
      <div className="image-slider">
        <label style={{ marginBottom: "12px", fontSize: "14px", fontWeight: 500 }}>בחר תמונה:</label>
        <hr style={{ margin: "0 0 12px 0" }}></hr>
        <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <p style={{ opacity: 0.6, padding: "1rem", textAlign: "center" }}>לא נמצאו תמונות</p>
        </div>
      </div>
    );
  }

  return (
    <div className="image-slider" role="list" aria-label="בחר תמונה">
      <label style={{ marginBottom: "12px", fontSize: "14px", fontWeight: 500 }}>בחר תמונה:</label>
      <hr style={{ margin: "0 0 12px 0" }}></hr>
      <div style={{ flex: 1, overflowY: "auto", minHeight: 0 }}>
        {images.map((img, idx) => (
          <img
            key={idx}
            src={`${api.defaults.baseURL}/images/${thinker}/${img}`}
            alt={`תמונה ${idx + 1}: ${img}`}
            className={`thumbnail ${selectedImage === img ? 'active' : ''}`}
            onClick={() => onSelect(img)}
            role="listitem"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelect(img);
              }
            }}
            aria-label={selectedImage === img ? `נבחר: ${img}` : `בחר תמונה: ${img}`}
            loading="lazy"
          />
        ))}
      </div>
    </div>
  );
}

export default memo(ImageSlider);
