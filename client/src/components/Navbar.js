import React from "react";
import { NavLink } from "react-router-dom";

function Navbar({ language, onLanguageChange }) {
  return (
    <nav className="navbar">
      <div className="logo">
        <span style={{ fontSize: '1.2em', marginRight: '4px' }}>🧠</span>
        StoicQuotes
      </div>

      <div className="nav-links">
        <NavLink to="/" className={({ isActive }) => (isActive ? "active" : "")}>
          צור ציטוט
        </NavLink>
        <NavLink to="/upload" className={({ isActive }) => (isActive ? "active" : "")}>
          העלה תוכן
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => (isActive ? "active" : "")}>
          היסטוריה
        </NavLink>
      </div>

      <div className="language-selector">
        <select value={language} onChange={(e) => onLanguageChange(e.target.value)}>
          <option value="he">עברית</option>
          <option value="en">English</option>
        </select>
      </div>
    </nav>
  );
}

export default Navbar;
