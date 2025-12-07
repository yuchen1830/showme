import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { LoadingState } from '@/components/results/LoadingState'

describe('LoadingState', () => {
  it('renders loading message', () => {
    render(<LoadingState />)
    
    expect(screen.getByText(/searching for events/i)).toBeInTheDocument()
  })

  it('displays loading indicator', () => {
    render(<LoadingState />)
    
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('shows animated spinner or skeleton', () => {
    const { container } = render(<LoadingState />)
    
    // Should have visual loading indicator (spinner/skeleton)
    const loadingElement = container.querySelector('[data-loading]') || 
                          container.querySelector('.animate-spin') ||
                          container.querySelector('.animate-pulse')
    
    expect(loadingElement).toBeInTheDocument()
  })

  it('provides accessible aria-label', () => {
    render(<LoadingState />)
    
    const status = screen.getByRole('status')
    expect(status).toHaveAttribute('aria-label')
  })
})


