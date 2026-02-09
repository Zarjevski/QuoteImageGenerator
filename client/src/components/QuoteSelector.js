import React, { memo } from 'react';

function QuoteSelector({ quotes, selectedQuote, onSelect }) {
  if (!quotes || quotes.length === 0) {
    return (
      <div className="quotes">
        <p style={{ opacity: 0.6, padding: "1rem" }}>לא נמצאו ציטוטים</p>
      </div>
    );
  }

  return (
    <div className="quotes quote-selector">
      <label>בחר ציטוט:</label>
      <hr></hr>
      <div className="quotes-content">
        {quotes.map((quote, idx) => (
          <div
            key={idx}
            className={`quote ${selectedQuote === quote ? 'active' : ''}`}
            onClick={() => onSelect(quote)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelect(quote);
              }
            }}
            aria-label={`בחר ציטוט: ${quote.substring(0, 50)}...`}
          >
            {quote}
          </div>
        ))}
      </div>
    </div>
  );
}

export default memo(QuoteSelector);
