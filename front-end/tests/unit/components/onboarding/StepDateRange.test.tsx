import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { StepDateRange } from '@/components/onboarding/StepDateRange'

describe('StepDateRange', () => {
  const today = new Date('2025-06-01')

  it('renders start and end date inputs', () => {
    render(
      <StepDateRange
        startDate={null}
        endDate={null}
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
      />
    )
    
    expect(screen.getByLabelText(/start date/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/end date/i)).toBeInTheDocument()
  })

  it('displays current date values', () => {
    const startDate = new Date('2025-06-01')
    const endDate = new Date('2025-06-30')
    
    render(
      <StepDateRange
        startDate={startDate}
        endDate={endDate}
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
      />
    )
    
    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement
    
    expect(startInput.value).toBe('2025-06-01')
    expect(endInput.value).toBe('2025-06-30')
  })

  it('calls onChange when dates are selected', async () => {
    const user = userEvent.setup()
    const handleChange = vi.fn()
    
    render(
      <StepDateRange
        startDate={null}
        endDate={null}
        onChange={handleChange}
        onNext={() => {}}
        onBack={() => {}}
      />
    )
    
    const startInput = screen.getByLabelText(/start date/i)
    await user.type(startInput, '2025-07-01')
    
    expect(handleChange).toHaveBeenCalled()
  })

  it('disables continue button when dates are not selected', () => {
    render(
      <StepDateRange
        startDate={null}
        endDate={null}
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /continue/i })
    expect(button).toBeDisabled()
  })

  it('enables continue button when both dates are selected', () => {
    render(
      <StepDateRange
        startDate={new Date('2025-06-01')}
        endDate={new Date('2025-06-30')}
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /continue/i })
    expect(button).not.toBeDisabled()
  })

  it('calls onBack when back button is clicked', async () => {
    const user = userEvent.setup()
    const handleBack = vi.fn()
    
    render(
      <StepDateRange
        startDate={null}
        endDate={null}
        onChange={() => {}}
        onNext={() => {}}
        onBack={handleBack}
      />
    )
    
    const button = screen.getByRole('button', { name: /back/i })
    await user.click(button)
    
    expect(handleBack).toHaveBeenCalled()
  })

  it('displays step indicator showing step 2 of 4', () => {
    render(
      <StepDateRange
        startDate={null}
        endDate={null}
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
      />
    )
    
    expect(screen.getByText(/step 2 of 4/i)).toBeInTheDocument()
  })
})


