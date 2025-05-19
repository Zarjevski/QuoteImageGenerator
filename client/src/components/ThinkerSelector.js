import React, { useEffect, useState } from 'react';

function ThinkerSelector({ onSelect }) {
  const [thinkers, setThinkers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://10.100.102.8:5000/thinkers')
      .then(res => res.json())
      .then(data => {
        setThinkers(data);
        setLoading(false);
      });
  }, []);

  return (
    <div className="thinker-selector">
      <label>בחר הוגה:</label>
      {loading ? <p>טוען...</p> : (
        <select onChange={(e) => onSelect(e.target.value)}>
          <option value="">--</option>
          {thinkers.map((thinker) => (
            <option key={thinker} value={thinker}>{thinker}</option>
          ))}
        </select>
      )}
    </div>
  );
}

export default ThinkerSelector;
