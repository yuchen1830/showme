import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { GeolocationService } from '@/domain/services/GeolocationService'
import type { SearchCriteria, Location } from '@/domain/entities/SearchCriteria'

export function useOnboarding() {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [query, setQuery] = useState('')
  const [startDate, setStartDate] = useState<Date | null>(null)
  const [endDate, setEndDate] = useState<Date | null>(null)
  const [location, setLocation] = useState('')
  const [locationCoords, setLocationCoords] = useState<{ lat: number; lng: number } | null>(null)
  const [maxPrice, setMaxPrice] = useState(0)
  const [isLoadingLocation, setIsLoadingLocation] = useState(false)

  const geolocationService = new GeolocationService()

  const handleDateChange = (field: 'start' | 'end', date: Date) => {
    if (field === 'start') {
      setStartDate(date)
    } else {
      setEndDate(date)
    }
  }

  const handleUseGeolocation = async () => {
    setIsLoadingLocation(true)
    try {
      const coords = await geolocationService.getCurrentPosition()
      setLocationCoords(coords)
      setLocation(`${coords.lat.toFixed(4)}, ${coords.lng.toFixed(4)}`)
    } catch (error) {
      console.error('Failed to get location:', error)
      // User can still enter manually
    } finally {
      setIsLoadingLocation(false)
    }
  }

  const handleSubmit = () => {
    if (!startDate || !endDate) return

    const searchCriteria: SearchCriteria = {
      query,
      startDate,
      endDate,
      location: locationCoords
        ? { type: 'coords', lat: locationCoords.lat, lng: locationCoords.lng }
        : { type: 'text', value: location },
      maxPrice,
    }

    // Store in sessionStorage for results page
    sessionStorage.setItem('searchCriteria', JSON.stringify(searchCriteria))
    
    // Navigate to results
    navigate('/results')
  }

  const nextStep = () => setStep((prev) => Math.min(prev + 1, 4))
  const prevStep = () => setStep((prev) => Math.max(prev - 1, 1))

  return {
    step,
    query,
    setQuery,
    startDate,
    endDate,
    handleDateChange,
    location,
    setLocation,
    handleUseGeolocation,
    isLoadingLocation,
    maxPrice,
    setMaxPrice,
    nextStep,
    prevStep,
    handleSubmit,
  }
}

