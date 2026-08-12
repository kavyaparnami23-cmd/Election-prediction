import './TopBar.css'

const SOCIAL_LINKS = [
  { icon: 'f', label: 'Facebook',  href: '#' },
  { icon: '𝕏', label: 'Twitter/X', href: '#' },
  { icon: '▶', label: 'YouTube',   href: '#' },
  { icon: '📷', label: 'Instagram', href: '#' },
]

export default function TopBar() {
  return (
    <div className="topbar">
      <div className="container topbar-inner">
        {/* Left */}
        <div className="topbar-left">
          <span className="topbar-phone">
            <span className="icon">📞</span>
            Toll Free — 1950
          </span>
          <div className="topbar-divider" />
          <a href="#" className="topbar-link">🏠 Home</a>
          <a href="#" className="topbar-link">Screen Reader Access</a>
          <a href="#" className="topbar-link">⏭ Skip to Main Content</a>
        </div>

        {/* Right */}
        <div className="topbar-right">
          <div className="social-icons">
            {SOCIAL_LINKS.map(({ icon, label, href }) => (
              <a key={label} href={href} aria-label={label} className="social-icon" title={label}>
                {icon}
              </a>
            ))}
          </div>
          <div className="topbar-divider" />
          <a href="#" className="topbar-btn">🇮🇳 हिंदी में देखें</a>
        </div>
      </div>
    </div>
  )
}
