import { sortEventsByPriceAndDistance } from '@/domain/entities/Event'
import type { Event } from '@/domain/entities/Event'
import { EventCard } from './EventCard'

interface ResultsViewProps {
  events: Event[]
  onEventClick: (event: Event) => void
}

export function ResultsView({ events, onEventClick }: ResultsViewProps) {
  const sortedEvents = sortEventsByPriceAndDistance(events)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">
          {events.length} {events.length === 1 ? 'event' : 'events'} found
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedEvents.map((event) => (
          <EventCard key={event.id} event={event} onClick={onEventClick} />
        ))}
      </div>
    </div>
  )
}


