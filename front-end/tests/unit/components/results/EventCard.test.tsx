import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { EventCard } from '@/components/results/EventCard'
import type { Event } from '@/domain/entities/Event'

describe('EventCard', () => {
  const mockEvent: Event = {
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
  }

  it('renders event title', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText('Taylor Swift | The Eras Tour')).toBeInTheDocument()
  })

  it('renders venue name', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText('Madison Square Garden')).toBeInTheDocument()
  })

  it('renders formatted date', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    // Should display date in a readable format
    expect(screen.getByText(/Jun 15, 2025/i)).toBeInTheDocument()
  })

  it('renders formatted price', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText(/\$250/)).toBeInTheDocument()
  })

  it('renders distance from user', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText(/5.2 mi away/i)).toBeInTheDocument()
  })

  it('renders venue address', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText(/4 Pennsylvania Plaza/i)).toBeInTheDocument()
  })

  it('calls onClick when card is clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    
    render(<EventCard event={mockEvent} onClick={handleClick} />)
    
    const card = screen.getByRole('article')
    await user.click(card)
    
    expect(handleClick).toHaveBeenCalledWith(mockEvent)
  })

  it('shows "from" label for lowest price', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText(/from/i)).toBeInTheDocument()
  })

  it('renders vendor source', () => {
    render(<EventCard event={mockEvent} onClick={() => {}} />)
    
    expect(screen.getByText(/ticketmaster/i)).toBeInTheDocument()
  })
})

