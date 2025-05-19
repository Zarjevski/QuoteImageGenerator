import React, { useEffect, useState } from 'react';

function QuoteImageSelector({ thinker, onQuoteSelect, onImageSelect, selectedImage }) {
  const [quotes, setQuotes] = useState([]);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch(`http://10.100.102.8:5000/quotes/${thinker}`).then(res => res.json()),
      fetch(`http://10.100.102.8:5000/images/${thinker}`).then(res => res.json())
    ]).then(([q, i]) => {
      setQuotes(q);
      setImages(i);
      setLoading(false);
    }).catch(err => {
      console.error("Failed to load quotes/images", err);
      setLoading(false);
    });
  }, [thinker]);

  return (
    <div className="selector-container">
      {loading ? <p>טוען ציטוטים ותמונות...</p> : (
        <>
          <div className="quotes">
            <h2>בחר ציטוט</h2>
            {quotes.map((q, idx) => (
              <p key={idx} onClick={() => onQuoteSelect(q)} className="quote">
                “{q}”
              </p>
            ))}
          </div>

          <div className="images">
            <h2>בחר תמונה</h2>
            {images.map((img, idx) => (
              <img
                key={idx}
                src={`http://10.100.102.8:5000/images/${thinker}/${img}`}
                alt={`img-${idx}`}
                className={`thumbnail ${img === selectedImage ? 'active' : ''}`}
                onClick={() => onImageSelect(img)}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default QuoteImageSelector;
