import React from 'react';

function QuoteSelector({ quotes, selectedQuote, onSelect }) {
  console.log(quotes)
  return (
    <div className="quotes">
      {quotes.map((quote, idx) => (
        <div
          key={idx}
          className={`quote ${selectedQuote === quote ? 'active' : ''}`}
          onClick={() => onSelect(quote)}
        >
          {quote}
        </div>
      ))}
    </div>
  );
}

export default QuoteSelector;
