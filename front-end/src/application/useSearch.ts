import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { TicketApi } from '@/infrastructure/api/ticketApi'
import type { Event } from '@/domain/entities/Event'
import type { SearchCriteria } from '@/domain/entities/SearchCriteria'

export function useSearch() {
  const navigate = useNavigate()
  const [events, setEvents] = useState<Event[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchCriteria, setSearchCriteria] = useState<SearchCriteria | null>(null)

  const ticketApi = new TicketApi()

  useEffect(() => {
    loadSearchCriteria()
  }, [])

  const loadSearchCriteria = async () => {
    try {
      const stored = sessionStorage.getItem('searchCriteria')
      if (!stored) {
        // No search criteria, redirect to onboarding
        navigate('/')
        return
      }

      const criteria: SearchCriteria = JSON.parse(stored)
      // Parse dates back from strings
      criteria.startDate = new Date(criteria.startDate)
      criteria.endDate = new Date(criteria.endDate)
      
      setSearchCriteria(criteria)
      await performSearch(criteria)
    } catch (err) {
      setError('Failed to load search criteria')
      setIsLoading(false)
    }
  }

  const performSearch = async (criteria: SearchCriteria) => {
    setIsLoading(true)
    setError(null)

    try {
      const results = await ticketApi.searchEvents(criteria)
      setEvents(results)
    } catch (err) {
      setError('Failed to search events. Please try again.')
      setEvents([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleEventClick = (event: Event) => {
    navigate(`/seatmap/${event.id}`)
  }

  const handleModifySearch = () => {
    navigate('/')
  }

  return {
    events,
    isLoading,
    error,
    searchCriteria,
    handleEventClick,
    handleModifySearch,
  }
}

