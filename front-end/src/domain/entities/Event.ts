import type { Venue } from './Venue'

export interface Event {
  id: string
  title: string
  date: Date
  venue: Venue
  lowestPrice: number
  distance: number
  vendorSource: string
}

export function createEvent(params: {
  id: string
  title: string
  date: Date
  venue: Venue
  lowestPrice: number
  distance: number
  vendorSource: string
}): Event {
  return {
    id: params.id,
    title: params.title,
    date: params.date,
    venue: params.venue,
    lowestPrice: params.lowestPrice,
    distance: params.distance,
    vendorSource: params.vendorSource,
  }
}

export function sortEventsByPriceAndDistance(events: Event[]): Event[] {
  return [...events].sort((a, b) => {
    // Primary sort: lowest price first
    if (a.lowestPrice !== b.lowestPrice) {
      return a.lowestPrice - b.lowestPrice
    }
    // Secondary sort: shortest distance first
    return a.distance - b.distance
  })
}


