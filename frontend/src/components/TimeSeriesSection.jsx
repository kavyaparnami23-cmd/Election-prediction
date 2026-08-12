import { useState, useRef, useEffect } from 'react'
import {
  ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, ReferenceLine, Area
} from 'recharts'
import './TimeSeriesSection.css'

/* ─── Real historical data from ECI (ind-lok-sabha.csv aggregated) ─── */
const HISTORICAL = [
  { year: 1977, votes: 188917504, electors: 321174327, turnout: 58.8 },
  { year: 1980, votes: 197824274, electors: 356205329, turnout: 55.5 },
  { year: 1984, votes: 249583543, electors: 400375333, turnout: 62.3 },
  { year: 1989, votes: 300713862, electors: 498906129, turnout: 60.3 },
  { year: 1991, votes: 278218849, electors: 511533598, turnout: 54.4 },
  { year: 1996, votes: 334327592, electors: 592572288, turnout: 56.4 },
  { year: 1998, votes: 367952396, electors: 605880192, turnout: 60.7 },
  { year: 1999, votes: 363694693, electors: 619536847, turnout: 58.7 },
  { year: 2004, votes: 389779784, electors: 671487930, turnout: 58.1 },
  { year: 2009, votes: 417158672, electors: 716676063, turnout: 58.2 },
  { year: 2014, votes: 553802946, electors: 834082814, turnout: 66.4 },
]

/* Linear regression: slope = 8.71M/yr, intercept computed from data */
const SLOPE = 8712561  // votes per year
const INTERCEPT = -17154677217  // computed from polyfit

function linForecast(year) {
  return Math.round(SLOPE * year + INTERCEPT)
}

/* ─── Build chart data: historical + forecasts ─── */
const FORECAST_YEARS = [2019, 2024, 2029, 2034, 2039]
const FORECAST_VALUES = {
  2019: 543260029,
  2024: 586802682,
  2029: 630345335,
  2034: 673887988,
  2039: 717430641,
}

const CHART_DATA = [
  ...HISTORICAL.map(h => ({
    year: String(h.year),
    actual: h.votes,
    fitted: linForecast(h.year),
    turnout: h.turnout,
    type: 'historical',
  })),
  ...FORECAST_YEARS.map(y => ({
    year: String(y) + (y >= 2029 ? '*' : ''),
    actual: null,
    fitted: FORECAST_VALUES[y],
    forecast: FORECAST_VALUES[y],
    turnout: null,
    type: 'forecast',
  })),
]

function fmtVotes(v) {
  if (v >= 1e8) return (v / 1e8).toFixed(1) + 'Cr'
  if (v >= 1e7) return (v / 1e7).toFixed(1) + 'Cr'
  return (v / 1e6).toFixed(0) + 'M'
}

function fmtFull(v) {
  return v?.toLocaleString('en-IN') ?? '—'
}

/* Custom Tooltip */
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  const isForecast = label?.includes('*') || payload[0]?.payload?.type === 'forecast'
  return (
    <div className="ts-tooltip">
      <div className="ts-tooltip-header">
        {label} {isForecast && <span className="ts-forecast-tag">ML Forecast</span>}
      </div>
      {payload.map(p => p.value != null && (
        <div key={p.name} className="ts-tooltip-row">
          <span className="ts-tooltip-dot" style={{ background: p.color }} />
          <span className="ts-tooltip-name">{p.name === 'actual' ? 'Actual Votes' : p.name === 'fitted' ? 'Model Fit' : 'Forecast'}</span>
          <span className="ts-tooltip-val" style={{ color: p.color }}>
            {fmtFull(p.value)}
          </span>
        </div>
      ))}
    </div>
  )
}

/* Animated counter */
function AnimCount({ target, duration = 1800 }) {
  const [val, setVal] = useState(0)
  const ref = useRef(null)
  useEffect(() => {
    const observer = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        const start = performance.now()
        function tick(now) {
          const t = Math.min((now - start) / duration, 1)
          setVal(Math.round(t * target))
          if (t < 1) requestAnimationFrame(tick)
        }
        requestAnimationFrame(tick)
        observer.disconnect()
      }
    }, { threshold: 0.5 })
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target])
  return <span ref={ref}>{val.toLocaleString('en-IN')}</span>
}

const TABS = [
  { id: 'votes',   label: '🗳️ Total Votes Polled' },
  { id: 'turnout', label: '📊 Voter Turnout %' },
]

export default function TimeSeriesSection() {
  const [tab, setTab] = useState('votes')

  /* Turnout chart data */
  const turnoutData = HISTORICAL.map(h => ({
    year: String(h.year),
    turnout: h.turnout,
  }))

  return (
    <section className="ts-section" id="time-series">
      <div className="container">

        {/* Header */}
        <div className="ts-header-badge">📈 Time-Series Forecast</div>
        <h2 className="section-title">Total Votes Polled — Historical &amp; Forecast</h2>
        <p className="section-subtitle">
          Historical Lok Sabha election data → Linear time-series model → Future election forecast
        </p>

        {/* Flow banner */}
        <div className="ts-flow-banner">
          <div className="ts-flow-step">📂 Historical ECI Data<br /><span>1977 – 2014</span></div>
          <div className="ts-flow-arrow">→</div>
          <div className="ts-flow-step">📈 Time-Series Model<br /><span>Linear regression fit</span></div>
          <div className="ts-flow-arrow">→</div>
          <div className="ts-flow-step">🔮 Future Forecast<br /><span>2029 · 2034 · 2039</span></div>
        </div>

        {/* Tab switcher */}
        <div className="ts-tabs">
          {TABS.map(t => (
            <button
              key={t.id}
              className={`ts-tab ${tab === t.id ? 'active' : ''}`}
              onClick={() => setTab(t.id)}
              id={`ts-tab-${t.id}`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Chart card */}
        <div className="ts-chart-card">

          {tab === 'votes' && (
            <>
              <div className="ts-chart-title">Total Votes Polled per Lok Sabha Election</div>
              <div className="ts-chart-desc">
                Actual votes (bars) vs linear model fit &amp; forecast (line). Stars (*) indicate ML projections.
              </div>
              <ResponsiveContainer width="100%" height={380}>
                <ComposedChart data={CHART_DATA} margin={{ top: 10, right: 30, left: 20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%"   stopColor="#6b21a8" stopOpacity={0.85} />
                      <stop offset="100%" stopColor="#9333ea" stopOpacity={0.45} />
                    </linearGradient>
                    <linearGradient id="fcastGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%"   stopColor="#f97316" stopOpacity={0.8} />
                      <stop offset="100%" stopColor="#f97316" stopOpacity={0.3} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" />
                  <XAxis
                    dataKey="year"
                    tick={{ fontSize: 11, fill: '#64748b' }}
                    angle={-30}
                    textAnchor="end"
                    height={48}
                  />
                  <YAxis
                    tick={{ fontSize: 11, fill: '#64748b' }}
                    tickFormatter={v => fmtVotes(v)}
                    width={60}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend
                    wrapperStyle={{ paddingTop: 16 }}
                    formatter={n =>
                      n === 'actual' ? 'Actual Votes' :
                      n === 'fitted' ? 'Model Fit / Forecast' : n
                    }
                  />
                  {/* Divider between historical and forecast */}
                  <ReferenceLine
                    x="2019"
                    stroke="#f97316"
                    strokeDasharray="6 3"
                    label={{ value: '← Forecast →', fill: '#f97316', fontSize: 10, position: 'insideTopRight' }}
                  />
                  <Bar dataKey="actual" name="actual" fill="url(#barGrad)" radius={[4,4,0,0]} maxBarSize={28} />
                  <Line
                    dataKey="fitted"
                    name="fitted"
                    type="monotone"
                    stroke="#f97316"
                    strokeWidth={2.5}
                    dot={(props) => {
                      const { cx, cy, payload } = props
                      if (!cx || !cy) return null
                      const isFcast = payload.type === 'forecast'
                      return (
                        <circle
                          key={`dot-${payload.year}`}
                          cx={cx} cy={cy} r={isFcast ? 6 : 4}
                          fill={isFcast ? '#f97316' : '#fff'}
                          stroke="#f97316"
                          strokeWidth={2}
                        />
                      )
                    }}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </>
          )}

          {tab === 'turnout' && (
            <>
              <div className="ts-chart-title">Voter Turnout % per Lok Sabha Election</div>
              <div className="ts-chart-desc">
                Percentage of registered electors who voted in each general election (1977–2014)
              </div>
              <ResponsiveContainer width="100%" height={380}>
                <ComposedChart data={turnoutData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="turnoutGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#0d9488" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#0d9488" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" />
                  <XAxis dataKey="year" tick={{ fontSize: 12, fill: '#64748b' }} />
                  <YAxis tick={{ fontSize: 12, fill: '#64748b' }} unit="%" domain={[45, 75]} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="turnout"
                    name="Voter Turnout"
                    stroke="#0d9488"
                    strokeWidth={2.5}
                    fill="url(#turnoutGrad)"
                    dot={{ r: 5, fill: '#0d9488', strokeWidth: 2, stroke: '#fff' }}
                    activeDot={{ r: 7 }}
                    unit="%"
                  />
                  <ReferenceLine y={60} stroke="#f97316" strokeDasharray="4 3"
                    label={{ value: '60% mark', fill: '#f97316', fontSize: 11, position: 'insideTopRight' }} />
                </ComposedChart>
              </ResponsiveContainer>
            </>
          )}

          <div className="ts-note">
            📌 Source: Election Commission of India (ECI) — Lok Sabha results 1977–2014.{' '}
            <strong>2019*, 2024*, 2029*, 2034*, 2039* are ML model projections</strong> using linear regression (slope ≈ +8.7M votes/year).
          </div>
        </div>

        {/* ── Projected Total Votes Table ── */}
        <div className="ts-forecast-layout">

          {/* Table */}
          <div className="ts-forecast-table-card">
            <div className="ts-forecast-table-header">
              <div className="ts-forecast-badge">🔮 Projected Total Votes</div>
              <p className="ts-forecast-model-note">Linear time-series model</p>
            </div>
            <table className="ts-forecast-table">
              <thead>
                <tr>
                  <th>Election Year</th>
                  <th>Forecast Total Votes</th>
                  <th>Growth vs 2014</th>
                </tr>
              </thead>
              <tbody>
                {FORECAST_YEARS.map(y => {
                  const val = FORECAST_VALUES[y]
                  const growthPct = (((val - 553802946) / 553802946) * 100).toFixed(1)
                  return (
                    <tr key={y} className={y >= 2029 ? 'ts-future-row' : ''}>
                      <td className="ts-year-cell">
                        {y}
                        {y >= 2029 && <span className="ts-star">★</span>}
                      </td>
                      <td className="ts-votes-cell">{fmtFull(val)}</td>
                      <td className="ts-growth-cell">
                        <span className="ts-growth-pill">
                          +{growthPct}%
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
            <p className="ts-table-note">★ = ML model projection (not official results)</p>
          </div>

          {/* Projection Summary Cards */}
          <div className="ts-proj-cards">
            <div className="ts-proj-header">Projected Total Votes</div>
            {[
              { year: 2029, val: FORECAST_VALUES[2029], color: '#6b21a8' },
              { year: 2034, val: FORECAST_VALUES[2034], color: '#0d9488' },
              { year: 2039, val: FORECAST_VALUES[2039], color: '#f97316' },
            ].map(({ year, val, color }) => (
              <div key={year} className="ts-proj-card" style={{ borderLeftColor: color }}>
                <div className="ts-proj-year" style={{ color }}>{year} →</div>
                <div className="ts-proj-val">
                  <AnimCount target={val} />
                </div>
                <div className="ts-proj-short" style={{ color }}>
                  ≈ {fmtVotes(val)} votes
                </div>
              </div>
            ))}

            {/* Historical anchor */}
            <div className="ts-proj-anchor">
              <div className="ts-proj-anchor-title">📌 Base Year (2014)</div>
              <div className="ts-proj-anchor-val">553,802,946</div>
              <div className="ts-proj-anchor-sub">Last available ECI data</div>
            </div>
          </div>
        </div>

      </div>
    </section>
  )
}
