import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { ResultsView } from '@/components/results/ResultsView'
import type { Event } from '@/domain/entities/Event'

describe('ResultsView', () => {
  const mockEvents: Event[] = [
    {
      id: '1',
      title: 'Event A',
      date: new Date('2025-06-15'),
      venue: {
        id: 'v1',
        name: 'Venue 1',
        address: 'Address 1',
        lat: 40.7128,
        lng: -74.006,
      },
      lowestPrice: 300,
      distance: 10,
      vendorSource: 'ticketmaster',
    },
    {
      id: '2',
      title: 'Event B',
      date: new Date('2025-06-16'),
      venue: {
        id: 'v2',
        name: 'Venue 2',
        address: 'Address 2',
        lat: 40.7589,
        lng: -73.9851,
      },
      lowestPrice: 200,
      distance: 20,
      vendorSource: 'stubhub',
    },
    {
      id: '3',
      title: 'Event C',
      date: new Date('2025-06-17'),
      venue: {
        id: 'v3',
        name: 'Venue 3',
        address: 'Address 3',
        lat: 40.7614,
        lng: -73.9776,
      },
      lowestPrice: 200,
      distance: 5,
      vendorSource: 'seatgeek',
    },
  ]

  it('renders all event cards', () => {
    render(<ResultsView events={mockEvents} onEventClick={() => {}} />)
    
    expect(screen.getByText('Event A')).toBeInTheDocument()
    expect(screen.getByText('Event B')).toBeInTheDocument()
    expect(screen.getByText('Event C')).toBeInTheDocument()
  })

  it('sorts events by price first (ascending)', () => {
    render(<ResultsView events={mockEvents} onEventClick={() => {}} />)
    
    const cards = screen.getAllByRole('article')
    
    // Event C and B both have $200 (cheapest), Event A has $300
    // So first two cards should be Event C or B
    expect(cards).toHaveLength(3)
  })

  it('sorts events by distance when prices are equal', () => {
    render(<ResultsView events={mockEvents} onEventClick={() => {}} />)
    
    const titles = screen.getAllByRole('heading', { level: 3 })
    
    // Event C ($200, 5mi) should come before Event B ($200, 20mi)
    expect(titles[0]).toHaveTextContent('Event C')
    expect(titles[1]).toHaveTextContent('Event B')
    expect(titles[2]).toHaveTextContent('Event A')
  })

  it('displays results count', () => {
    render(<ResultsView events={mockEvents} onEventClick={() => {}} />)
    
    expect(screen.getByText(/3 events found/i)).toBeInTheDocument()
  })

  it('renders in grid layout', () => {
    const { container } = render(
      <ResultsView events={mockEvents} onEventClick={() => {}} />
    )
    
    const grid = container.querySelector('.grid')
    expect(grid).toBeInTheDocument()
  })

  it('shows empty state when no events', () => {
    render(<ResultsView events={[]} onEventClick={() => {}} />)
    
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
  })
})


