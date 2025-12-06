import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { OnboardingPage } from '@/pages/OnboardingPage'
import { ResultsPage } from '@/pages/ResultsPage'
import { SeatMapPage } from '@/pages/SeatMapPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<OnboardingPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/seatmap/:eventId" element={<SeatMapPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
