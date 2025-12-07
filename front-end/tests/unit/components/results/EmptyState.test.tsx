import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { EmptyState } from '@/components/results/EmptyState'

describe('EmptyState', () => {
  it('renders empty state message', () => {
    render(<EmptyState onModifySearch={() => {}} />)
    
    expect(screen.getByText(/no events found/i)).toBeInTheDocument()
  })

  it('shows suggestion to modify search', () => {
    render(<EmptyState onModifySearch={() => {}} />)
    
    expect(screen.getByText(/try adjusting your search criteria/i)).toBeInTheDocument()
  })

  it('displays modify search button', () => {
    render(<EmptyState onModifySearch={() => {}} />)
    
    expect(screen.getByRole('button', { name: /modify search/i })).toBeInTheDocument()
  })

  it('calls onModifySearch when button is clicked', async () => {
    const user = userEvent.setup()
    const handleModifySearch = vi.fn()
    
    render(<EmptyState onModifySearch={handleModifySearch} />)
    
    const button = screen.getByRole('button', { name: /modify search/i })
    await user.click(button)
    
    expect(handleModifySearch).toHaveBeenCalled()
  })

  it('shows helpful tips', () => {
    render(<EmptyState onModifySearch={() => {}} />)
    
    expect(screen.getByText(/increase your budget/i)).toBeInTheDocument()
    expect(screen.getByText(/expand your date range/i)).toBeInTheDocument()
  })

  it('renders search icon or illustration', () => {
    const { container } = render(<EmptyState onModifySearch={() => {}} />)
    
    // Should have some visual element (icon/svg)
    const svg = container.querySelector('svg')
    expect(svg).toBeInTheDocument()
  })
})


