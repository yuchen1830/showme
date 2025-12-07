import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { StepMaxPrice } from '@/components/onboarding/StepMaxPrice'

describe('StepMaxPrice', () => {
  it('renders max price input field', () => {
    render(
      <StepMaxPrice
        value={0}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    expect(screen.getByLabelText(/maximum price/i)).toBeInTheDocument()
  })

  it('displays the current price value', () => {
    render(
      <StepMaxPrice
        value={500}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    const input = screen.getByLabelText(/maximum price/i) as HTMLInputElement
    expect(input.value).toBe('500')
  })

  it('calls onChange when user types a number', async () => {
    const user = userEvent.setup()
    const handleChange = vi.fn()
    
    render(
      <StepMaxPrice
        value={0}
        onChange={handleChange}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    const input = screen.getByLabelText(/maximum price/i)
    await user.type(input, '300')
    
    expect(handleChange).toHaveBeenCalled()
  })

  it('disables search button when price is zero', () => {
    render(
      <StepMaxPrice
        value={0}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /search tickets/i })
    expect(button).toBeDisabled()
  })

  it('enables search button when price is greater than zero', () => {
    render(
      <StepMaxPrice
        value={250}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /search tickets/i })
    expect(button).not.toBeDisabled()
  })

  it('calls onSubmit when search button is clicked', async () => {
    const user = userEvent.setup()
    const handleSubmit = vi.fn()
    
    render(
      <StepMaxPrice
        value={400}
        onChange={() => {}}
        onSubmit={handleSubmit}
        onBack={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /search tickets/i })
    await user.click(button)
    
    expect(handleSubmit).toHaveBeenCalled()
  })

  it('calls onBack when back button is clicked', async () => {
    const user = userEvent.setup()
    const handleBack = vi.fn()
    
    render(
      <StepMaxPrice
        value={0}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={handleBack}
      />
    )
    
    const button = screen.getByRole('button', { name: /back/i })
    await user.click(button)
    
    expect(handleBack).toHaveBeenCalled()
  })

  it('displays step indicator showing step 4 of 4', () => {
    render(
      <StepMaxPrice
        value={0}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    expect(screen.getByText(/step 4 of 4/i)).toBeInTheDocument()
  })

  it('only accepts positive numbers', () => {
    render(
      <StepMaxPrice
        value={100}
        onChange={() => {}}
        onSubmit={() => {}}
        onBack={() => {}}
      />
    )
    
    const input = screen.getByLabelText(/maximum price/i) as HTMLInputElement
    expect(input.type).toBe('number')
    expect(input.min).toBe('1')
  })
})


