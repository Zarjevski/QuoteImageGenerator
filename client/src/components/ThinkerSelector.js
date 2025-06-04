import React, { useEffect, useState } from "react";
import { getThinkers } from "../api/api";

function ThinkerSelector({ language, onSelect }) {
  const [thinkers, setThinkers] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!language) return;

    getThinkers(language)
      .then((res) => {
        setThinkers(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [language]);

  const handleSelect = (thinker) => {
    setSelected(thinker);
    onSelect(thinker);
  };

  return (
    <div className="thinker-selector">
      <label>בחר הוגה:</label>
      {loading ? (
        <p>טוען...</p>
      ) : (
        <div className="quotes">
          {thinkers.map((thinker, idx) => (
            <div
              key={idx}
              className={`quote ${selected === thinker ? "active" : ""}`}
              onClick={() => handleSelect(thinker)}
            >
              {thinker}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ThinkerSelector;
