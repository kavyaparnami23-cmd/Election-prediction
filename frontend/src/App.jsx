import { useState } from 'react'
import TopBar from './components/TopBar'
import Navbar from './components/Navbar'
import HeroCarousel from './components/HeroCarousel'
import QuickLinks from './components/QuickLinks'
import CategoryIcons from './components/CategoryIcons'
import PredictionSection from './components/PredictionSection'
import TimeSeriesSection from './components/TimeSeriesSection'
import StatsSection from './components/StatsSection'
import Footer from './components/Footer'
import './App.css'

function App() {
  return (
    <div className="app-root">
      <TopBar />
      <Navbar />
      <main>
        <HeroCarousel />
        <QuickLinks />
        <CategoryIcons />
        <PredictionSection />
        <TimeSeriesSection />
        <StatsSection />
      </main>
      <Footer />
    </div>
  )
}

export default App
