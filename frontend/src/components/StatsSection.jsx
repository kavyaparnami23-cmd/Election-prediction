import { useEffect, useRef, useState } from 'react'
import './StatsSection.css'

const STATS = [
  { icon: '🗳️', value: '543',  label: 'Lok Sabha Seats',          cls: '' },
  { icon: '📊', value: '87%',  label: 'Forecast Accuracy',        cls: 'teal' },
  { icon: '🏛️', value: '41',   label: 'States & UTs Covered',     cls: '' },
  { icon: '⚡', value: '50+',  label: 'Electoral Indicators',     cls: 'teal' },
]

const BAR_DATA = [
  { label: 'Uttar Pradesh', winners: 80, total: 80, color: 'orange' },
  { label: 'Maharashtra',   winners: 48, total: 48, color: 'teal'   },
  { label: 'West Bengal',   winners: 42, total: 42, color: 'purple' },
  { label: 'Bihar',         winners: 40, total: 40, color: 'orange' },
  { label: 'Tamil Nadu',    winners: 39, total: 39, color: 'teal'   },
  { label: 'Rajasthan',     winners: 25, total: 25, color: 'purple' },
  { label: 'Karnataka',     winners: 28, total: 28, color: 'orange' },
  { label: 'Gujarat',       winners: 26, total: 26, color: 'teal'   },
]

const MAX_SEATS = 80

export default function StatsSection() {
  const sectionRef = useRef(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisible(true) },
      { threshold: 0.2 }
    )
    if (sectionRef.current) obs.observe(sectionRef.current)
    return () => obs.disconnect()
  }, [])

  return (
    <section className="stats-section" id="stats" ref={sectionRef}>
      <div className="container">
        <h2 className="section-title">📊 Dataset & Coverage Statistics</h2>
        <p className="section-subtitle">
          Key metrics from our Lok Sabha election forecast system
        </p>

        {/* Stat cards */}
        <div className="stats-grid">
          {STATS.map(({ icon, value, label, cls }) => (
            <div key={label} className="stat-card">
              <span className="stat-card-icon">{icon}</span>
              <div className={`stat-card-value ${cls}`}>{value}</div>
              <div className="stat-card-label">{label}</div>
            </div>
          ))}
        </div>

        {/* Bar chart */}
        <div className="chart-container">
          <div className="chart-title">
            📈 Constituencies by State (Top 8)
          </div>
          <div className="bar-chart">
            {BAR_DATA.map(({ label, winners, total, color }) => {
              const heightPct = visible ? (winners / MAX_SEATS) * 100 : 0
              return (
                <div key={label} className="bar-group">
                  <div className="bar-value">{winners}</div>
                  <div
                    className={`bar ${color}`}
                    style={{ height: `${heightPct}%`, transition: `height 1.2s cubic-bezier(0.4,0,0.2,1) ${Math.random() * 0.3}s` }}
                    title={`${label}: ${winners} seats`}
                  />
                  <div className="bar-label">{label.split(' ')[0]}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}
