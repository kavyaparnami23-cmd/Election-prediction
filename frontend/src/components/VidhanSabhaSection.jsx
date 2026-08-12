import { useState } from 'react'
import './VidhanSabhaSection.css'

const VS_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
  'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra',
  'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
  'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
  'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
]

const PARTIES = [
  'BJP', 'Congress', 'AAP', 'SP', 'BSP', 'TMC', 'DMK', 'AIADMK',
  'TRS', 'YSR Congress', 'JDU', 'RJD', 'NCP', 'Shiv Sena', 'Other',
]

/* Party colour map */
const PARTY_COLORS = {
  BJP:        { bg: '#FF6B35', light: 'rgba(255,107,53,0.12)', border: 'rgba(255,107,53,0.4)' },
  Congress:   { bg: '#0070C0', light: 'rgba(0,112,192,0.12)',  border: 'rgba(0,112,192,0.4)' },
  AAP:        { bg: '#0093DD', light: 'rgba(0,147,221,0.12)',  border: 'rgba(0,147,221,0.4)' },
  SP:         { bg: '#E84040', light: 'rgba(232,64,64,0.12)',  border: 'rgba(232,64,64,0.4)' },
  BSP:        { bg: '#2563EB', light: 'rgba(37,99,235,0.12)',  border: 'rgba(37,99,235,0.4)' },
  TMC:        { bg: '#1DB954', light: 'rgba(29,185,84,0.12)',  border: 'rgba(29,185,84,0.4)' },
  DMK:        { bg: '#E31E25', light: 'rgba(227,30,37,0.12)',  border: 'rgba(227,30,37,0.4)' },
  AIADMK:    { bg: '#00C400', light: 'rgba(0,196,0,0.12)',    border: 'rgba(0,196,0,0.4)'   },
  TRS:        { bg: '#FF69B4', light: 'rgba(255,105,180,0.12)', border: 'rgba(255,105,180,0.4)' },
  'YSR Congress': { bg: '#FFCC00', light: 'rgba(255,204,0,0.12)', border: 'rgba(255,204,0,0.4)' },
  JDU:        { bg: '#00B4D8', light: 'rgba(0,180,216,0.12)', border: 'rgba(0,180,216,0.4)' },
  RJD:        { bg: '#F72585', light: 'rgba(247,37,133,0.12)', border: 'rgba(247,37,133,0.4)' },
  NCP:        { bg: '#7B2D8B', light: 'rgba(123,45,139,0.12)', border: 'rgba(123,45,139,0.4)' },
  'Shiv Sena': { bg: '#FF8C00', light: 'rgba(255,140,0,0.12)', border: 'rgba(255,140,0,0.4)' },
  Other:      { bg: '#64748B', light: 'rgba(100,116,139,0.12)', border: 'rgba(100,116,139,0.4)' },
}

function getColor(party) {
  return PARTY_COLORS[party] || PARTY_COLORS.Other
}

/* Simulated prediction for a party in a Vidhan Sabha seat */
function simulatePrediction(party, state, constituency, electors) {
  /* Deterministic pseudo-random based on inputs */
  const seed = (party.charCodeAt(0) + state.charCodeAt(0) + constituency.length + electors) % 100
  const base = (seed * 7 + 23) % 100
  const winProb = Math.min(Math.max(base / 100, 0.05), 0.95)
  const votes = Math.round(electors * winProb * (0.4 + Math.random() * 0.2))
  return { winProb, votes }
}

function ProbBarVS({ value, color }) {
  return (
    <div className="vs-prob-bar">
      <div
        className="vs-prob-bar-fill"
        style={{ width: `${value * 100}%`, background: color }}
      />
    </div>
  )
}

function PartyCard({ party, data, isWinner }) {
  const col = getColor(party)
  return (
    <div
      className={`vs-party-card ${isWinner ? 'winner' : ''}`}
      style={{ borderColor: isWinner ? col.bg : 'transparent', background: col.light }}
    >
      {isWinner && (
        <div className="vs-winner-badge" style={{ background: col.bg }}>
          👑 LIKELY TO WIN
        </div>
      )}
      <div className="vs-party-header">
        <div className="vs-party-dot" style={{ background: col.bg }} />
        <div className="vs-party-name">{party}</div>
        {!isWinner && <div className="vs-not-win-tag">NOT LIKELY TO WIN</div>}
      </div>

      <div className="vs-party-stats">
        <div className="vs-stat-row">
          <span className="vs-stat-label">Win Probability</span>
          <span className="vs-stat-value" style={{ color: col.bg }}>
            {(data.winProb * 100).toFixed(1)}%
          </span>
        </div>
        <ProbBarVS value={data.winProb} color={col.bg} />
        <div className="vs-stat-row" style={{ marginTop: 12 }}>
          <span className="vs-stat-label">Predicted Votes</span>
          <span className="vs-stat-value">{data.votes.toLocaleString()}</span>
        </div>
      </div>
    </div>
  )
}

const DEFAULT_VS = {
  state: 'Rajasthan',
  constituency: 'Jaipur',
  electors: '180000',
  party1: 'BJP',
  party2: 'Congress',
}

export default function VidhanSabhaSection() {
  const [form, setForm] = useState(DEFAULT_VS)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) =>
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const handlePredict = async (e) => {
    e.preventDefault()
    setLoading(true)

    await new Promise(r => setTimeout(r, 800))   // simulate API call

    const electors = parseInt(form.electors) || 180000
    const p1 = simulatePrediction(form.party1, form.state, form.constituency, electors)
    const p2 = simulatePrediction(form.party2, form.state, form.constituency, electors + 1)

    /* normalise so probs add to 1 */
    const total = p1.winProb + p2.winProb
    const r1 = { ...p1, winProb: p1.winProb / total }
    const r2 = { ...p2, winProb: p2.winProb / total }

    const winner = r1.winProb >= r2.winProb ? form.party1 : form.party2
    setResults({ p1: r1, p2: r2, winner, party1: form.party1, party2: form.party2, state: form.state, constituency: form.constituency })
    setLoading(false)
  }

  return (
    <section className="vs-section" id="vidhan-sabha">
      <div className="container">
        {/* Header */}
        <div className="vs-header">
          <div className="vs-header-badge">🏛️ Vidhan Sabha</div>
          <h2 className="section-title">Vidhan Sabha Party Predictor</h2>
          <p className="section-subtitle">
            Compare two parties head-to-head in any state assembly constituency
          </p>
        </div>

        <div className="vs-layout">
          {/* ── Input Form ─────────────────────── */}
          <div className="vs-form-card">
            <div className="vs-form-header">
              <div className="vs-form-icon">🏛️</div>
              <div>
                <div className="vs-form-title">Constituency Details</div>
                <div className="vs-form-subtitle">Vidhan Sabha — 2029 Prediction</div>
              </div>
            </div>

            <form onSubmit={handlePredict} id="vs-prediction-form">
              <div className="vs-form-grid">

                {/* State */}
                <div className="vs-form-group full">
                  <label className="form-label" htmlFor="vs-state">🗺️ State</label>
                  <select
                    id="vs-state"
                    name="state"
                    className="form-control"
                    value={form.state}
                    onChange={handleChange}
                  >
                    {VS_STATES.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>

                {/* Constituency */}
                <div className="vs-form-group full">
                  <label className="form-label" htmlFor="vs-const">🏘️ Constituency Name</label>
                  <input
                    id="vs-const"
                    name="constituency"
                    type="text"
                    className="form-control"
                    value={form.constituency}
                    onChange={handleChange}
                    placeholder="e.g. Jaipur, Lucknow, Patna"
                    required
                  />
                </div>

                {/* Party 1 */}
                <div className="vs-form-group">
                  <label className="form-label" htmlFor="vs-party1">🔵 Party 1</label>
                  <select
                    id="vs-party1"
                    name="party1"
                    className="form-control"
                    value={form.party1}
                    onChange={handleChange}
                  >
                    {PARTIES.map(p => <option key={p} value={p}>{p}</option>)}
                  </select>
                </div>

                {/* Party 2 */}
                <div className="vs-form-group">
                  <label className="form-label" htmlFor="vs-party2">🔴 Party 2</label>
                  <select
                    id="vs-party2"
                    name="party2"
                    className="form-control"
                    value={form.party2}
                    onChange={handleChange}
                  >
                    {PARTIES.filter(p => p !== form.party1).map(p => (
                      <option key={p} value={p}>{p}</option>
                    ))}
                  </select>
                </div>

                {/* Electors */}
                <div className="vs-form-group full">
                  <label className="form-label" htmlFor="vs-electors">🧑‍🤝‍🧑 Total Registered Electors</label>
                  <input
                    id="vs-electors"
                    name="electors"
                    type="number"
                    min="1000"
                    className="form-control"
                    value={form.electors}
                    onChange={handleChange}
                    placeholder="e.g. 180000"
                    required
                  />
                </div>

              </div>

              <button
                type="submit"
                className="btn-predict"
                disabled={loading}
                id="vs-predict-btn"
                style={{ marginTop: 28 }}
              >
                {loading ? (
                  <><span className="spinner" /> Analysing Parties...</>
                ) : (
                  <>🏛️ Compare Parties — 2029 Prediction</>
                )}
              </button>
            </form>
          </div>

          {/* ── Results ─────────────────────────── */}
          <div className="vs-results">
            {results ? (
              <>
                {/* Model Summary banner */}
                <div className="vs-model-banner">
                  <div className="vs-model-banner-label">MODEL PREDICTION</div>
                  <div className="vs-model-row">
                    <span className="vs-model-key">State</span>
                    <span className="vs-model-val">{results.state}</span>
                  </div>
                  <div className="vs-model-row">
                    <span className="vs-model-key">Constituency</span>
                    <span className="vs-model-val">{results.constituency}</span>
                  </div>
                  <div className="vs-divider" />
                  <div className="vs-model-row">
                    <span className="vs-model-key">Predicted Winner</span>
                    <span className="vs-model-winner"
                      style={{ color: getColor(results.winner).bg }}>
                      {results.winner}
                    </span>
                  </div>
                  <div className="vs-model-row">
                    <span className="vs-model-key">Confidence</span>
                    <span className="vs-model-winner">
                      {(Math.max(results.p1.winProb, results.p2.winProb) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="vs-disclaimer">
                    ⚠️ This is a <em>model prediction</em>, not a guaranteed election result.
                  </div>
                </div>

                {/* Party cards */}
                <div className="vs-cards">
                  <PartyCard
                    party={results.party1}
                    data={results.p1}
                    isWinner={results.winner === results.party1}
                  />
                  <PartyCard
                    party={results.party2}
                    data={results.p2}
                    isWinner={results.winner === results.party2}
                  />
                </div>
              </>
            ) : (
              <div className="vs-placeholder">
                <div className="vs-placeholder-icon">🏛️</div>
                <div className="vs-placeholder-title">Awaiting Party Comparison</div>
                <div className="vs-placeholder-desc">
                  Select state, constituency and two parties, then click <strong>"Compare Parties"</strong> to see the 2029 prediction.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
