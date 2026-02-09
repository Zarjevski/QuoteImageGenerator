import React, { useState } from "react";
import ThinkerSelector from "../components/ThinkerSelector";
import QuoteImageSelector from "../components/QuoteImageSelector";
import QuotePreview from "../components/QuotePreview";
import { generatePreview } from "../api/api";
import { baseURL } from "../constants";

function CreatePage({ language }) {
  const [selectedThinker, setSelectedThinker] = useState(null); // file name (e.g., barack_obama)
  const [imageFolder, setImageFolder] = useState(null); // folder name (e.g., Barack Obama)
  const [displayName, setDisplayName] = useState(""); // Hebrew or English name inside JSON
  const [selectedQuote, setSelectedQuote] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [previewFilename, setPreviewFilename] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);

  const handleGenerate = async (thinker, quote, image) => {
    setLoadingPreview(true);
    try {
      const res = await generatePreview({
        thinker: displayName,       // used on the image
        quote,
        image,
        imageFolder,                // used for image lookup
      });
      const data = res.data;
      setPreviewUrl(`${baseURL}/${data.preview_url}`);
      setPreviewFilename(data.filename);
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || "שגיאה ביצירת התמונה";
      alert(`שגיאה: ${errorMessage}`);
    } finally {
      setLoadingPreview(false);
    }
  };

  const handleSelection = (quote, image) => {
    setSelectedQuote(quote);
    setSelectedImage(image);
    if (selectedThinker && quote && image) {
      handleGenerate(selectedThinker, quote, image);
    }
  };

  return (
    <div className="container">
      <ThinkerSelector
        language={language}
        onSelect={(thinkerDisplayName) => {
          // Convert display name (e.g., "Barack Obama") to file key (e.g., "barack_obama")
          const fileKey = thinkerDisplayName.toLowerCase().replace(/\s+/g, "_");
          const folderName = thinkerDisplayName; // Use display name as folder name

          setSelectedThinker(fileKey);
          setImageFolder(folderName);
          setDisplayName(""); // Will be set by QuoteImageSelector when quotes load
          setSelectedQuote(null);
          setSelectedImage(null);
          setPreviewUrl(null);
        }}
      />

      {selectedThinker && (
        <QuoteImageSelector
          thinker={selectedThinker}
          imageFolder={imageFolder}
          language={language}
          selectedImage={selectedImage}
          onQuoteSelect={(quote) => handleSelection(quote, selectedImage)}
          onImageSelect={(image) => handleSelection(selectedQuote, image)}
          setDisplayName={setDisplayName}
        />
      )}

      <QuotePreview
        loading={loadingPreview}
        setLoading={setLoadingPreview}
        previewUrl={previewUrl}
        filename={previewFilename}
        quote={selectedQuote}
      />
    </div>
  );
}

export default CreatePage;
