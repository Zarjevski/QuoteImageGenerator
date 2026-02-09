import React, { useEffect, useState } from "react";
import QuoteSelector from "./QuoteSelector";
import ImageSlider from "./ImageSlider";
import { getQuotes, getImages } from "../api/api";

function QuoteImageSelector({
  thinker, // File name (e.g., "barack_obama")
  imageFolder, // Folder name (e.g., "Barack Obama")
  language,
  selectedImage,
  onQuoteSelect,
  onImageSelect,
  setDisplayName,
}) {
  const [quotes, setQuotes] = useState([]);
  const [images, setImages] = useState([]);
  const [selectedQuote, setSelectedQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!thinker || !language) return;

    setLoading(true);
    setError(null);
    const fileKey = thinker.toLowerCase().replace(/ /g, "_");

    Promise.all([
      getQuotes(language, fileKey)
        .then((res) => {
          const data = res.data;
          if (data && typeof data === "object") {
            const jsonKey = Object.keys(data)[0];
            setDisplayName(jsonKey); // Set "ברק אובמה" etc.
            setQuotes(Array.isArray(data[jsonKey]) ? data[jsonKey] : []);
          } else {
            setQuotes([]);
            setDisplayName(null);
          }
        })
        .catch((err) => {
          setError("שגיאה בטעינת הציטוטים");
          setQuotes([]);
          setDisplayName(null);
        }),
      imageFolder
        ? getImages(imageFolder)
            .then((res) => setImages(Array.isArray(res.data) ? res.data : []))
            .catch((err) => {
              setError("שגיאה בטעינת התמונות");
              setImages([]);
            })
        : Promise.resolve(),
    ]).finally(() => {
      setLoading(false);
    });

    setSelectedQuote(null);
  }, [thinker, language, imageFolder, setDisplayName]);

  const handleQuoteSelect = (quote) => {
    setSelectedQuote(quote);
    onQuoteSelect(quote);
  };

  const handleImageSelect = (img) => {
    onImageSelect(img);
  };

  if (loading) {
    return (
      <div className="selector-container">
        <p style={{ opacity: 0.6 }}>טוען...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="selector-container">
        <p style={{ color: "#ff6b6b" }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="selector-container">
      <div className="quotes-images-wrapper">
        <QuoteSelector
          quotes={quotes}
          selectedQuote={selectedQuote}
          onSelect={handleQuoteSelect}
        />
        <ImageSlider
          images={images}
          selectedImage={selectedImage}
          onSelect={handleImageSelect}
          thinker={imageFolder} // Use English folder name
        />
      </div>
    </div>
  );
}

export default QuoteImageSelector;
