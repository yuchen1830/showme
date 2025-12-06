import { createEvent } from '@/domain/entities/Event'
import type { Event } from '@/domain/entities/Event'
import type { SearchCriteria } from '@/domain/entities/SearchCriteria'

// Mock API - will be replaced with real API integration
export class TicketApi {
  async searchEvents(criteria: SearchCriteria): Promise<Event[]> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Mock data - in real app, this would call actual ticket APIs
    const mockEvents: Event[] = [
      createEvent({
        id: 'evt-001',
        title: `${criteria.query} | Summer Tour 2025`,
        date: new Date('2025-07-15T19:30:00'),
        venue: {
          id: 'ven-001',
          name: 'Madison Square Garden',
          address: '4 Pennsylvania Plaza, New York, NY 10001',
          lat: 40.7505,
          lng: -73.9934,
        },
        lowestPrice: 185,
        distance: 2.5,
        vendorSource: 'ticketmaster',
      }),
      createEvent({
        id: 'evt-002',
        title: `${criteria.query} - Special Performance`,
        date: new Date('2025-07-20T20:00:00'),
        venue: {
          id: 'ven-002',
          name: 'Barclays Center',
          address: '620 Atlantic Ave, Brooklyn, NY 11217',
          lat: 40.6826,
          lng: -73.9754,
        },
        lowestPrice: 225,
        distance: 8.3,
        vendorSource: 'stubhub',
      }),
      createEvent({
        id: 'evt-003',
        title: `${criteria.query} Live in Concert`,
        date: new Date('2025-07-25T19:00:00'),
        venue: {
          id: 'ven-003',
          name: 'Prudential Center',
          address: '25 Lafayette St, Newark, NJ 07102',
          lat: 40.7335,
          lng: -74.1711,
        },
        lowestPrice: 150,
        distance: 12.1,
        vendorSource: 'seatgeek',
      }),
      createEvent({
        id: 'evt-004',
        title: `${criteria.query} World Tour`,
        date: new Date('2025-08-01T18:30:00'),
        venue: {
          id: 'ven-004',
          name: 'MetLife Stadium',
          address: '1 MetLife Stadium Dr, East Rutherford, NJ 07073',
          lat: 40.8128,
          lng: -74.0742,
        },
        lowestPrice: 275,
        distance: 15.7,
        vendorSource: 'ticketmaster',
      }),
    ]

    // Filter by price
    return mockEvents.filter((event) => event.lowestPrice <= criteria.maxPrice)
  }
}

