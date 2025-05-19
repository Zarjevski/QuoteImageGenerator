import React, { useEffect, useState } from 'react';

function HistoryManager() {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState('');

  const fetchHistory = async () => {
    const res = await fetch('http://10.100.102.8:5000/history');
    const data = await res.json();
    setFiles(data.files || []);
  };

  const clearHistory = async () => {
    const res = await fetch('http://10.100.102.8:5000/history', {
      method: 'DELETE'
    });
    const data = await res.json();
    setMessage(data.message);
    fetchHistory();
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="history-manager">
      <h2>היסטוריית תמונות</h2>
      <button onClick={clearHistory}>נקה את תיקיית התמונות</button>
      {message && <p>{message}</p>}
      <ul>
        {files.map((file, idx) => (
          <li key={idx}>{file}</li>
        ))}
      </ul>
    </div>
  );
}

export default HistoryManager;
