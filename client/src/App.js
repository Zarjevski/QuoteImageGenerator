import React, { useState } from "react";
import ThinkerSelector from "./components/ThinkerSelector";
import QuoteImageSelector from "./components/QuoteImageSelector";
import QuotePreview from "./components/QuotePreview";
import UploadManager from "./components/UploadManager";
import HistoryManager from "./components/HistoryManager";
import "./styles/App.css";

function App() {
  const [tab, setTab] = useState("create");
  const [selectedThinker, setSelectedThinker] = useState(null);
  const [selectedQuote, setSelectedQuote] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [previewFilename, setPreviewFilename] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);

  const generatePreview = async (thinker, quote, image) => {
    setLoadingPreview(true);
    try {
      const res = await fetch("http://10.100.102.8:5000/generate-preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thinker, quote, image }),
      });
      const data = await res.json();
      setPreviewUrl(`http://10.100.102.8:5000${data.preview_url}`);
      setPreviewFilename(data.filename);
    } catch (err) {
      console.error("Preview generation failed:", err);
    } finally {
      setLoadingPreview(false);
    }
  };

  const handleSelection = (quote, image) => {
    setSelectedQuote(quote);
    setSelectedImage(image);
    if (quote && image && selectedThinker) {
      generatePreview(selectedThinker, quote, image);
    }
  };

  return (
    <div className="App">
      <div className="tab-buttons">
        <button
          className={tab === "create" ? "active" : ""}
          onClick={() => setTab("create")}
        >
          ✏️ צור ציטוט
        </button>
        <button
          className={tab === "upload" ? "active" : ""}
          onClick={() => setTab("upload")}
        >
          📤 העלה תוכן
        </button>
      </div>

      {tab === "create" && (
        <>
          <ThinkerSelector
            onSelect={(thinker) => {
              setSelectedThinker(thinker);
              setSelectedQuote(null);
              setSelectedImage(null);
              setPreviewUrl(null);
            }}
          />

          <div className="container">
            {selectedThinker && (
              <QuoteImageSelector
                thinker={selectedThinker}
                selectedImage={selectedImage}
                onQuoteSelect={(quote) => handleSelection(quote, selectedImage)}
                onImageSelect={(image) => handleSelection(selectedQuote, image)}
              />
            )}

            <QuotePreview
              loading={loadingPreview}
              previewUrl={previewUrl}
              filename={previewFilename}
              quote={selectedQuote}
            />
          </div>
        </>
      )}

      {tab === "upload" && (
        <div className="container">
          <UploadManager />
          <HistoryManager />
        </div>
      )}
    </div>
  );
}

export default App;
