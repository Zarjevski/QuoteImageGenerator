import React, { useState } from "react";
import ThinkerSelector from "./components/ThinkerSelector";
import QuoteImageSelector from "./components/QuoteImageSelector";
import QuotePreview from "./components/QuotePreview";
import UploadManager from "./components/UploadManager";
import HistoryManager from "./components/HistoryManager";
import api, {
  generatePreview as apiGeneratePreview,
  getThinkers,
  getQuotes,
  getImages,
} from "./api/api";
import "./styles/App.css";

function App() {
  const [tab, setTab] = useState("create");
  const [language, setLanguage] = useState("he"); // 'he' or 'en'
  const [selectedThinker, setSelectedThinker] = useState(null); // fileKey (e.g. "barack_obama")
  const [imageFolder, setImageFolder] = useState(null); // folder name (e.g. "Barack Obama")
  const [selectedQuote, setSelectedQuote] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [previewFilename, setPreviewFilename] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [displayName, setDisplayName] = useState(null); // "ברק אובמה"

  const generatePreview = async (realAuthorName, quote, image, folder) => {
    setLoadingPreview(true);
    try {
      const res = await apiGeneratePreview({
        thinker: realAuthorName,
        quote,
        image,
        imageFolder: folder, // ✅ send folder name too
      });
      const data = res.data;
      setPreviewUrl(`${api.defaults.baseURL}${data.preview_url}`);
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
    if (quote && image && displayName && imageFolder) {
      generatePreview(displayName, quote, image, imageFolder); // ✅ pass folder name
    }
  };

  const handleRandomSelection = async () => {
    try {
      const thinkerListRes = await getThinkers(language);
      const thinkers = thinkerListRes.data;
      const randomThinker =
        thinkers[Math.floor(Math.random() * thinkers.length)];

      const fileKey = randomThinker.toLowerCase().replace(/ /g, "_");
      setSelectedThinker(fileKey);
      setImageFolder(randomThinker);

      const quoteRes = await getQuotes(language, fileKey);
      const quoteData = quoteRes.data;
      const displayName = Object.keys(quoteData)[0];
      const quoteList = quoteData[displayName];
      const randomQuote =
        quoteList[Math.floor(Math.random() * quoteList.length)];

      setDisplayName(displayName);
      setSelectedQuote(randomQuote);

      const imageRes = await getImages(randomThinker);
      const imageList = imageRes.data;
      const randomImage =
        imageList[Math.floor(Math.random() * imageList.length)];

      setSelectedImage(randomImage);
      generatePreview(displayName, randomQuote, randomImage, randomThinker);
    } catch (err) {
      console.error("Random selection failed:", err);
    }
  };

  return (
    <div className="App">
      <div style={{ marginBottom: "1rem" }}>
        <label>בחר שפה: </label>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="he">עברית</option>
          <option value="en">English</option>
        </select>
        <button className="random-btn" onClick={handleRandomSelection}>
          🎲 אקראי
        </button>
      </div>

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
          <div className="container">
            <ThinkerSelector
              language={language}
              onSelect={(thinkerName) => {
                const fileKey = thinkerName.toLowerCase().replace(/ /g, "_");
                setSelectedThinker(fileKey); // used for fetching quote JSON
                setImageFolder(thinkerName); // used for image folder
                setSelectedQuote(null);
                setSelectedImage(null);
                setPreviewUrl(null);
                setDisplayName(null);
              }}
            />
            {selectedThinker && imageFolder && (
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
