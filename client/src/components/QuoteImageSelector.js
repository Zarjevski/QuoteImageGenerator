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

  useEffect(() => {
    if (!thinker || !language) return;

    const fileKey = thinker.toLowerCase().replace(/ /g, "_");

    getQuotes(language, fileKey)
      .then((res) => {
        const data = res.data;
        const jsonKey = Object.keys(data)[0];
        setDisplayName(jsonKey); // Set "ברק אובמה" etc.
        setQuotes(data[jsonKey]);
      })
      .catch(() => {
        setQuotes([]);
        setDisplayName(null);
      });

    if (imageFolder) {
      getImages(imageFolder)
        .then((res) => setImages(res.data))
        .catch(() => setImages([]));
    }

    setSelectedQuote(null);
  }, [thinker, language, imageFolder]);

  const handleQuoteSelect = (quote) => {
    setSelectedQuote(quote);
    onQuoteSelect(quote);
  };

  const handleImageSelect = (img) => {
    onImageSelect(img);
  };

  return (
    <div className="selector-container">
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
  );
}

export default QuoteImageSelector;
