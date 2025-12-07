import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import type { Event } from '@/domain/entities/Event'
import type { SearchCriteria } from '@/domain/entities/SearchCriteria'
import { sortEventsByPriceAndDistance } from '@/domain/entities/Event'
import { backendApi } from '@/infrastructure/api/backendApi'
import { adaptBackendEvents } from '@/infrastructure/api/backendAdapter'

export function useSearch() {
  const [events, setEvents] = useState<Event[]>([])
  const [isLoading, setIsLoading] = useState(true) // Start true to show loading immediately
  const [error, setError] = useState<string | null>(null)
  const [searchCriteria, setSearchCriteria] = useState<SearchCriteria | null>(null)
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  // Parse search criteria from URL on mount
  useEffect(() => {
    const query = searchParams.get('query')
    const location = searchParams.get('location')
    const startDate = searchParams.get('startDate')
    const endDate = searchParams.get('endDate')
    const maxPrice = searchParams.get('maxPrice')
    const lat = searchParams.get('lat')
    const lng = searchParams.get('lng')

    if (query && location) {
      const criteria: SearchCriteria = {
        query,
        location: lat && lng
          ? { type: 'coords', lat: parseFloat(lat), lng: parseFloat(lng) }
          : { type: 'text', value: location },
        startDate: startDate ? new Date(startDate) : new Date(),
        endDate: endDate ? new Date(endDate) : new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        maxPrice: maxPrice ? parseInt(maxPrice) : 500,
      }
      setSearchCriteria(criteria)

      // Execute search
      executeSearch(criteria)
    } else {
      setIsLoading(false)
      setError('No search criteria provided')
    }
  }, [searchParams])

  const executeSearch = async (criteria: SearchCriteria) => {
    setIsLoading(true)
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

      // Call backend API - this takes 3-5 minutes for AI agent search
      console.log('[useSearch] Starting AI agent search - this may take several minutes...')
      const response = await backendApi.searchEvents({
        query: criteria.query,
        location: location,
        locationText: locationText,
        startDate: criteria.startDate,
        endDate: criteria.endDate,
        maxPrice: criteria.maxPrice,
      })

      console.log('[useSearch] Search complete, got', response.events.length, 'events')

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
      console.error('[useSearch] Search error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleEventClick = (eventId: string) => {
    navigate(`/event/${eventId}`)
  }

  const handleModifySearch = () => {
    navigate('/')
  }

  return {
    events,
    isLoading,
    loading: isLoading, // Alias for compatibility
    error,
    searchCriteria,
    handleEventClick,
    handleModifySearch,
    search: executeSearch,
    clearError: () => setError(null),
  }
}

