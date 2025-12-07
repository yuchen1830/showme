import { useParams } from 'react-router-dom'

export function SeatMapPage() {
  const { eventId } = useParams<{ eventId: string }>()
  
  return (
    <div className="min-h-screen bg-slate-900 p-6">
      <h1 className="text-2xl font-bold text-white mb-4">Seat Map</h1>
      <p className="text-slate-400">Event ID: {eventId}</p>
      <p className="text-slate-400">Seat map viewer coming soon...</p>
    </div>
  )
}


