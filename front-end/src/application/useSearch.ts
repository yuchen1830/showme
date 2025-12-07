import { useState } from 'react'
import type { Event } from '@/domain/entities/Event'
import type { SearchCriteria } from '@/domain/entities/SearchCriteria'
import { sortEventsByPriceAndDistance } from '@/domain/entities/Event'
import { backendApi } from '@/infrastructure/api/backendApi'
import { adaptBackendEvents } from '@/infrastructure/api/backendAdapter'

interface UseSearchReturn {
  events: Event[]
  loading: boolean
  error: string | null
  search: (criteria: SearchCriteria) => Promise<void>
  clearError: () => void
}

export function useSearch(): UseSearchReturn {
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const search = async (criteria: SearchCriteria) => {
    setLoading(true)
    setError(null)

    try {
      // Extract coordinates from location
      const location =
        criteria.location.type === 'coords'
          ? criteria.location
          : { lat: 40.7128, lng: -74.006 } // Default to NYC if text location

      const locationText =
        criteria.location.type === 'text'
          ? criteria.location.value
          : `${location.lat}, ${location.lng}`

      // Call backend API
      const response = await backendApi.searchEvents({
        query: criteria.query,
        location: location,
        locationText: locationText,
        startDate: criteria.startDate,
        endDate: criteria.endDate,
        maxPrice: criteria.maxPrice,
      })

      // Convert backend events to frontend entities
      const adaptedEvents = adaptBackendEvents(response.events, location)

      // Sort by price and distance (frontend domain logic)
      const sortedEvents = sortEventsByPriceAndDistance(adaptedEvents)

      setEvents(sortedEvents)
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to search events'
      setError(errorMessage)
      setEvents([])
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const clearError = () => {
    setError(null)
  }

  return {
    events,
    loading,
    error,
    search,
    clearError,
  }
}
