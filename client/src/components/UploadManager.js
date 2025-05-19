import React, { useState, useEffect } from 'react';

function UploadManager() {
  const [thinker, setThinker] = useState('');
  const [allThinkers, setAllThinkers] = useState([]);
  const [quoteFile, setQuoteFile] = useState(null);
  const [images, setImages] = useState([]);
  const [status, setStatus] = useState('');
  const [progress, setProgress] = useState(0);
  const [mode, setMode] = useState('new'); // 'new' or 'add'

  useEffect(() => {
    fetch("http://10.100.102.8:5000/thinkers")
      .then(res => res.json())
      .then(data => setAllThinkers(data));
  }, []);

  const uploadContent = async () => {
    if (!thinker) return alert("אנא הזן שם הוגה");
    if (mode === 'new' && (!quoteFile || images.length === 0)) {
      return alert("יש להעלות גם קובץ JSON וגם תמונות");
    }

    setProgress(0);
    let uploadedImages = 0;

    // Upload quote file (as-is)
    if (mode === 'new') {
      const formData = new FormData();
      formData.append("file", quoteFile);
      const res = await fetch(`http://10.100.102.8:5000/upload/quote-file/${thinker}`, {
        method: 'POST',
        body: formData
      });
      if (!res.ok) return alert("שגיאה בהעלאת קובץ הציטוטים");
    }

    // Upload images
    for (let i = 0; i < images.length; i++) {
      const formData = new FormData();
      formData.append("image", images[i]);
      await fetch(`http://10.100.102.8:5000/upload/image/${thinker}`, {
        method: 'POST',
        body: formData
      });
      uploadedImages++;
      const total = images.length;
      setProgress(Math.round((uploadedImages / total) * 100));
    }

    setStatus(`הועלו ${uploadedImages} תמונות עבור ${thinker}`);
    setProgress(0);
    setThinker('');
    setQuoteFile(null);
    setImages([]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setImages([...images, ...Array.from(e.dataTransfer.files)]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="upload-manager">
      <h2>העלאה</h2>

      <div className="tab-buttons">
        <button className={mode === 'new' ? 'active' : ''} onClick={() => setMode('new')}>➕ הוסף הוגה חדש</button>
        <button className={mode === 'add' ? 'active' : ''} onClick={() => setMode('add')}>📸 הוסף תמונות להוגה קיים</button>
      </div>

      <label>בחר הוגה קיים או כתוב שם חדש:</label>
      <select value={thinker} onChange={e => setThinker(e.target.value)}>
        <option value="">-- בחר הוגה --</option>
        {allThinkers.map((t, i) => (
          <option key={i} value={t}>{t}</option>
        ))}
      </select>
      <input type="text" placeholder="או כתוב שם חדש" value={thinker} onChange={e => setThinker(e.target.value)} />

      {mode === 'new' && (
        <>
          <label htmlFor="quote-upload" className="upload-btn">📄 בחר קובץ JSON</label>
          <input
            id="quote-upload"
            type="file"
            accept=".json"
            onChange={e => setQuoteFile(e.target.files[0])}
            style={{ display: 'none' }}
          />
          {quoteFile && <p>קובץ נבחר: {quoteFile.name}</p>}
        </>
      )}

      <label>גרור תמונות או בחר קבצים:</label>
      <div className="drop-zone" onDrop={handleDrop} onDragOver={handleDragOver}>
        שחרר כאן קבצי תמונה
      </div>
      <label htmlFor="image-upload" className="upload-btn">🖼️ בחר תמונות</label>
      <input
        id="image-upload"
        type="file"
        multiple
        accept="image/*"
        onChange={e => setImages(Array.from(e.target.files))}
        style={{ display: 'none' }}
      />
      {images.length > 0 && <p>{images.length} קבצי תמונה נבחרו</p>}

      <button onClick={uploadContent}>העלה {mode === 'new' ? 'הוגה חדש' : 'תמונות'}</button>

      {progress > 0 && (
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
      )}
      {status && <p>{status}</p>}
    </div>
  );
}

export default UploadManager;
