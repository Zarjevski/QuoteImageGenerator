import React, { useEffect, useState } from "react";
import { getThinkers } from "../api/api";
import Spinner from "./Spinner";

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
    <div className="quotes thinker-selector">
      <label htmlFor="thinker-selector">בחר הוגה:</label>
      <hr></hr>
      <div className="quotes-content">
        {loading ? (
          <Spinner />
        ) : thinkers.length === 0 ? (
          <p style={{ opacity: 0.6, padding: "1rem" }}>לא נמצאו הוגים</p>
        ) : (
          thinkers.map((thinker, idx) => (
            <div
              key={idx}
              className={`quote ${selected === thinker ? "active" : ""}`}
              onClick={() => handleSelect(thinker)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  handleSelect(thinker);
                }
              }}
              aria-label={`בחר ${thinker}`}
            >
              {thinker}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ThinkerSelector;
