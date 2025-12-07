/**
 * Adapter to convert backend responses to frontend domain entities
 */
import { createEvent, type Event } from '@/domain/entities/Event'
import type { Venue } from '@/domain/entities/Venue'

interface BackendEvent {
  id: string
  name: string
  artist: string
  venue_name: string
  date: string
  location: string
  latitude: number
  longitude: number
  min_price: number
  max_price: number
  vendor: string
  vendor_url: string
}

/**
 * Calculate distance between two coordinates using Haversine formula
 * Returns distance in miles
 */
function calculateDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 3959 // Earth's radius in miles
  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLon = ((lon2 - lon1) * Math.PI) / 180
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

/**
 * Convert backend event to frontend Event entity
 */
export function adaptBackendEvent(
  backendEvent: BackendEvent,
  userLocation: { lat: number; lng: number }
): Event {
  // Create venue object
  const venue: Venue = {
    id: `venue-${backendEvent.venue_name.toLowerCase().replace(/\s+/g, '-')}`,
    name: backendEvent.venue_name,
    address: backendEvent.location,
    lat: backendEvent.latitude,
    lng: backendEvent.longitude,
  }

  // Calculate distance from user location
  const distance = calculateDistance(
    userLocation.lat,
    userLocation.lng,
    backendEvent.latitude,
    backendEvent.longitude
  )

  // Create and return event
  return createEvent({
    id: backendEvent.id,
    title: backendEvent.name,
    date: new Date(backendEvent.date),
    venue: venue,
    lowestPrice: backendEvent.min_price,
    distance: Math.round(distance * 10) / 10, // Round to 1 decimal
    vendorSource: backendEvent.vendor,
  })
}

/**
 * Convert array of backend events to frontend events
 */
export function adaptBackendEvents(
  backendEvents: BackendEvent[],
  userLocation: { lat: number; lng: number }
): Event[] {
  return backendEvents.map((event) => adaptBackendEvent(event, userLocation))
}

