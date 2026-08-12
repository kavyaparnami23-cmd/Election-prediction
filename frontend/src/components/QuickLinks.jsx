import './QuickLinks.css'

const LINKS = [
  { icon: '💡', label: 'Myth Vs Reality',    href: '#myth',    cls: 'primary' },
  { icon: '📊', label: 'Election Results',   href: '#results', cls: '' },
  { icon: '📰', label: 'Press Releases',     href: '#press',   cls: '' },
  { icon: '📅', label: 'Election Calendar',  href: '#calendar',cls: '' },
  { icon: '📋', label: 'Model Report',       href: '#stats',   cls: '' },
  { icon: '🗺️', label: 'State-wise Map',     href: '#map',     cls: '' },
]

export default function QuickLinks() {
  return (
    <div className="quicklinks">
      <div className="container">
        <div className="quicklinks-inner">
          {LINKS.map(({ icon, label, href, cls }) => (
            <a key={label} href={href} className={`ql-item ${cls}`}>
              <span className="ql-icon">{icon}</span>
              {label}
            </a>
          ))}
          <div className="ql-progress">
            <div className="ql-progress-bar" />
          </div>
        </div>
      </div>
    </div>
  )
}
