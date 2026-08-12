import './Footer.css'

const LINKS_1 = [
  { label: '🔮 Predict Winner',    href: '#predict'  },
  { label: '📊 Election Results',  href: '#results'  },
  { label: '🗺️ Constituency Map',  href: '#map'      },
  { label: '📚 About the Model',   href: '#about'    },
]

const LINKS_2 = [
  { label: 'Lok Sabha 2024',   href: '#' },
  { label: 'Lok Sabha 2019',   href: '#' },
  { label: 'Lok Sabha 2014',   href: '#' },
  { label: 'State Elections',  href: '#' },
]

const LINKS_3 = [
  { label: '📖 Documentation', href: '#' },
  { label: '💻 GitHub Repo',   href: '#' },
  { label: '📧 Contact Us',    href: '#' },
  { label: '🔒 Privacy Policy',href: '#' },
]

const SOCIAL = ['f', '𝕏', '▶', '📷']

export default function Footer() {
  return (
    <footer className="footer" id="about">
      <div className="container">
        <div className="footer-grid">
          {/* Brand col */}
          <div>
            <div className="footer-brand">
              <div className="footer-logo">🗳️</div>
              <div className="footer-name">ElectionPulse AI</div>
            </div>
            <p className="footer-tagline">
              An AI-powered Lok Sabha election winner prediction system.
              Built with advanced predictive analytics on real Indian election data.
            </p>
            <div className="footer-social">
              {SOCIAL.map((s, i) => (
                <a key={i} href="#" aria-label={`Social link ${i}`}>{s}</a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <div className="footer-col-title">Quick Links</div>
            <ul className="footer-links">
              {LINKS_1.map(({ label, href }) => (
                <li key={label}><a href={href}>{label}</a></li>
              ))}
            </ul>
          </div>

          {/* Elections */}
          <div>
            <div className="footer-col-title">Elections</div>
            <ul className="footer-links">
              {LINKS_2.map(({ label, href }) => (
                <li key={label}><a href={href}>{label}</a></li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <div className="footer-col-title">Resources</div>
            <ul className="footer-links">
              {LINKS_3.map(({ label, href }) => (
                <li key={label}><a href={href}>{label}</a></li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="footer-bottom">
          <p className="footer-copy">
            © 2024 <span>ElectionPulse AI</span> by Kavya Parnami. Built with ❤️ using React + FastAPI.
          </p>
          <div className="footer-pills">
            <a href="#" className="footer-pill">Privacy</a>
            <a href="#" className="footer-pill">Terms</a>
            <a href="#" className="footer-pill">Accessibility</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
