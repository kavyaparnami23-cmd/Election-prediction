import { useState } from 'react'
import './Navbar.css'

const NAV_ITEMS = [
  { label: '🏠 Home',          href: '#home',         active: true  },
  { label: '🔮 Predict',       href: '#predict',      active: false },
  { label: '📈 Time Series',   href: '#time-series',  active: false },
  { label: '📊 Results',       href: '#stats',        active: false },
  { label: 'ℹ️ About',         href: '#about',        active: false },
]

export default function Navbar() {
  const [activeIdx, setActiveIdx] = useState(0)

  return (
    <nav className="navbar">
      <div className="navbar-inner container">
        {/* Brand */}
        <a href="#home" className="navbar-brand">
          <div className="brand-logo">🗳️</div>
          <div>
            <div className="brand-text-main">ElectionPulse AI</div>
            <div className="brand-text-sub">Lok Sabha Prediction Engine</div>
          </div>
        </a>

        {/* Nav Links */}
        <ul className="nav-links">
          {NAV_ITEMS.map((item, i) => (
            <li key={item.label}>
              <a
                href={item.href}
                className={`nav-link ${i === activeIdx ? 'active' : ''}`}
                onClick={() => setActiveIdx(i)}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Search */}
        <div className="navbar-search">
          <input
            type="text"
            placeholder="Search constituency..."
            id="nav-search-input"
            aria-label="Search constituency"
          />
          <button className="search-btn" aria-label="Search">Search</button>
        </div>

        {/* Hamburger */}
        <button className="hamburger" aria-label="Open menu">
          <span /><span /><span />
        </button>
      </div>
    </nav>
  )
}
