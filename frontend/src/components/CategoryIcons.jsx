import './CategoryIcons.css'

const CATEGORIES = [
  {
    icon:   '🗳️',
    label:  'Electors',
    color:  'teal',
    href:   '#electors',
  },
  {
    icon:   '🏛️',
    label:  'Political Parties / Candidates',
    color:  'purple',
    href:   '#parties',
  },
  {
    icon:   '📋',
    label:  'Election Management',
    color:  'orange',
    href:   '#management',
  },
  {
    icon:   '📚',
    label:  'Media & Publications',
    color:  'blue',
    href:   '#media',
  },
  {
    icon:   '🎓',
    label:  'Voter Education',
    color:  'gold',
    href:   '#education',
  },
  {
    icon:   '📱',
    label:  'ICT Apps & Prediction',
    color:  'rose',
    href:   '#predict',
  },
]

export default function CategoryIcons() {
  return (
    <section className="category-section">
      <div className="container">
        <h2 className="section-title">Explore ElectionPulse AI</h2>
        <p className="section-subtitle">
          Discover tools, data and insights for every aspect of Lok Sabha elections
        </p>

        <div className="categories-grid">
          {CATEGORIES.map(({ icon, label, color, href }) => (
            <a key={label} href={href} className="category-card" aria-label={label}>
              <div className={`cat-circle ${color}`}>
                <div className="cat-circle-inner">{icon}</div>
              </div>
              <div className={`cat-bar ${color}`} />
              <span className="cat-label">{label}</span>
            </a>
          ))}
        </div>
      </div>
    </section>
  )
}
