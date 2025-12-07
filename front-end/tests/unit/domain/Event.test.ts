import { describe, it, expect } from 'vitest'
import { 
  Event, 
  createEvent, 
  sortEventsByPriceAndDistance 
} from '@/domain/entities/Event'

describe('Event', () => {
  describe('createEvent', () => {
    it('creates an event with all required fields', () => {
      const event = createEvent({
        id: 'evt-123',
        title: 'Taylor Swift | The Eras Tour',
        date: new Date('2025-06-15T19:00:00'),
        venue: {
          id: 'ven-456',
          name: 'Madison Square Garden',
          address: '4 Pennsylvania Plaza, New York, NY 10001',
          lat: 40.7505,
          lng: -73.9934,
        },
        lowestPrice: 250,
        distance: 5.2,
        vendorSource: 'ticketmaster',
      })

      expect(event.id).toBe('evt-123')
      expect(event.title).toBe('Taylor Swift | The Eras Tour')
      expect(event.venue.name).toBe('Madison Square Garden')
      expect(event.lowestPrice).toBe(250)
      expect(event.distance).toBe(5.2)
    })
  })

  describe('sortEventsByPriceAndDistance', () => {
    const events: Event[] = [
      createEvent({
        id: '1',
        title: 'Event A',
        date: new Date('2025-06-15'),
        venue: { id: 'v1', name: 'Venue 1', address: 'Addr 1', lat: 0, lng: 0 },
        lowestPrice: 300,
        distance: 10,
        vendorSource: 'stubhub',
      }),
      createEvent({
        id: '2',
        title: 'Event B',
        date: new Date('2025-06-16'),
        venue: { id: 'v2', name: 'Venue 2', address: 'Addr 2', lat: 0, lng: 0 },
        lowestPrice: 200,
        distance: 20,
        vendorSource: 'ticketmaster',
      }),
      createEvent({
        id: '3',
        title: 'Event C',
        date: new Date('2025-06-17'),
        venue: { id: 'v3', name: 'Venue 3', address: 'Addr 3', lat: 0, lng: 0 },
        lowestPrice: 200,
        distance: 5,
        vendorSource: 'seatgeek',
      }),
    ]

    it('sorts events by price (ascending) first', () => {
      const sorted = sortEventsByPriceAndDistance(events)
      
      expect(sorted[0].lowestPrice).toBe(200)
      expect(sorted[1].lowestPrice).toBe(200)
      expect(sorted[2].lowestPrice).toBe(300)
    })

    it('sorts events by distance (ascending) when prices are equal', () => {
      const sorted = sortEventsByPriceAndDistance(events)
      
      // Both Event B and C have price 200, but C has shorter distance (5 vs 20)
      expect(sorted[0].id).toBe('3') // Event C - $200, 5mi
      expect(sorted[1].id).toBe('2') // Event B - $200, 20mi
      expect(sorted[2].id).toBe('1') // Event A - $300, 10mi
    })

    it('returns empty array when given empty array', () => {
      expect(sortEventsByPriceAndDistance([])).toEqual([])
    })

    it('does not mutate original array', () => {
      const original = [...events]
      sortEventsByPriceAndDistance(events)
      
      expect(events).toEqual(original)
    })
  })
})


