import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { MapPin, Calendar, DollarSign } from 'lucide-react'
import type { Event } from '@/domain/entities/Event'

interface EventCardProps {
  event: Event
  onClick: (event: Event) => void
}

export function EventCard({ event, onClick }: EventCardProps) {
  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    }).format(date)
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(price)
  }

  return (
    <article
      onClick={() => onClick(event)}
      className="cursor-pointer transition-transform hover:scale-105"
    >
      <Card className="h-full bg-slate-800 border-slate-700 hover:border-purple-500">
        <CardHeader>
          <h3 className="text-lg font-semibold text-white line-clamp-2">
            {event.title}
          </h3>
          <p className="text-sm text-slate-400">{event.venue.name}</p>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <Calendar className="h-4 w-4 text-purple-400" />
            {formatDate(event.date)}
          </div>

          <div className="flex items-center gap-2 text-sm text-slate-300">
            <MapPin className="h-4 w-4 text-purple-400" />
            <div className="flex-1">
              <p className="line-clamp-1">{event.venue.address}</p>
              <p className="text-xs text-slate-500">{event.distance} mi away</p>
            </div>
          </div>

          <div className="flex items-center justify-between pt-3 border-t border-slate-700">
            <div className="flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-green-400" />
              <div>
                <p className="text-xs text-slate-400">from</p>
                <p className="text-xl font-bold text-white">
                  {formatPrice(event.lowestPrice)}
                </p>
              </div>
            </div>
            <div className="text-xs text-slate-500 capitalize">
              {event.vendorSource}
            </div>
          </div>
        </CardContent>
      </Card>
    </article>
  )
}

