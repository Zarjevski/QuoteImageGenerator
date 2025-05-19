import React from 'react';

function Spinner({ size = 40 }) {
  return (
    <div className="spinner-container">
      <div className="spinner" style={{ width: size, height: size }}></div>
    </div>
  );
}

export default Spinner;
