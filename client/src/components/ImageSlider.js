import React from 'react';
import api from '../api/api';

function ImageSlider({ images, selectedImage, onSelect, thinker }) {
  return (
    <div className="image-slider">
      {images.map((img, idx) => (
        <img
          key={idx}
          src={`${api.defaults.baseURL}/images/${thinker}/${img}`}
          alt={`thumb-${idx}`}
          className={`thumbnail ${selectedImage === img ? 'active' : ''}`}
          onClick={() => onSelect(img)}
        />
      ))}
    </div>
  );
}

export default ImageSlider;
