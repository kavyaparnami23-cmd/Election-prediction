import { useState, useEffect, useCallback } from 'react'
import './HeroCarousel.css'

const SLIDES = [
  {
    badge:     'Live Prediction Engine',
    highlight: 'Powered by Election Intelligence',
    title:     <>Predict Lok Sabha <span>Election Winners</span> with AI</>,
    desc:      'ElectionPulse AI uses comprehensive Lok Sabha historical election data to predict if a candidate will win their constituency.',
    stat:      '543',
    statLabel: 'Lok Sabha Constituencies',
    btnLabel:  '🔮 Try Prediction',
    btnHref:   '#predict',
    emoji:     '🗳️',
  },
  {
    badge:     'Data-Driven Insights',
    highlight: 'Trained on Historical Election Data',
    title:     <>Constituency-Level <span>Vote Estimation</span> & Analysis</>,
    desc:      'Our advanced prediction engine estimates vote counts per candidate based on state, constituency, gender, and electorate size.',
    stat:      '87%',
    statLabel: 'Forecast Accuracy',
    btnLabel:  '📊 View Stats',
    btnHref:   '#stats',
    emoji:     '📊',
  },
  {
    badge:     'Multi-State Coverage',
    highlight: '41 Indian States & UTs Supported',
    title:     <>From <span>Rajasthan</span> to <span>West Bengal</span> — Full Coverage</>,
    desc:      'Supports all major Indian states and Union Territories for Lok Sabha election winner prediction and vote estimation.',
    stat:      '41',
    statLabel: 'States & UTs Covered',
    btnLabel:  '🗺️ Explore States',
    btnHref:   '#states',
    emoji:     '🇮🇳',
  },
]

export default function HeroCarousel() {
  const [current, setCurrent] = useState(0)
  const [animKey, setAnimKey] = useState(0)

  const goTo = useCallback((idx) => {
    setCurrent(idx)
    setAnimKey(k => k + 1)
  }, [])

  const next = useCallback(() => goTo((current + 1) % SLIDES.length), [current, goTo])
  const prev = useCallback(() => goTo((current - 1 + SLIDES.length) % SLIDES.length), [current, goTo])

  // Auto-rotate every 5 s
  useEffect(() => {
    const timer = setInterval(next, 5000)
    return () => clearInterval(timer)
  }, [next])

  const slide = SLIDES[current]

  return (
    <section className="hero" id="home">
      {/* Background blobs */}
      <div className="hero-blob hero-blob-1" />
      <div className="hero-blob hero-blob-2" />

      {/* Prev arrow */}
      <div className="hero-nav prev">
        <button className="hero-arrow" onClick={prev} aria-label="Previous slide">◀</button>
      </div>

      {/* Slide content */}
      <div className="container hero-inner" key={animKey}>
        <div className="hero-content">
          <div className="hero-badge">
            <span className="dot" />
            {slide.badge}
          </div>
          <p className="hero-highlight">{slide.highlight}</p>
          <h1 className="hero-title">{slide.title}</h1>
          <p className="hero-desc">{slide.desc}</p>
          <div className="hero-actions">
            <a href={slide.btnHref} className="btn-primary">{slide.btnLabel}</a>
            <a href="#about" className="btn-secondary">Learn More →</a>
          </div>
        </div>

        {/* Circular image / stat */}
        <div className="hero-image-frame" aria-hidden="true">
          <div className="hero-image-inner">
            <div className="hero-stat">{slide.stat}</div>
            <div className="hero-stat-label">{slide.statLabel}</div>
          </div>
        </div>
      </div>

      {/* Next arrow */}
      <div className="hero-nav next">
        <button className="hero-arrow" onClick={next} aria-label="Next slide">▶</button>
      </div>

      {/* Dot indicators */}
      <div className="hero-indicators">
        {SLIDES.map((_, i) => (
          <button
            key={i}
            className={`indicator ${i === current ? 'active' : ''}`}
            onClick={() => goTo(i)}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>
    </section>
  )
}
