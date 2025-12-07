import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { StepLocation } from '@/components/onboarding/StepLocation'

describe('StepLocation', () => {
  it('renders location input field', () => {
    render(
      <StepLocation
        value=""
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    expect(screen.getByLabelText(/location/i)).toBeInTheDocument()
  })

  it('displays the current location value', () => {
    render(
      <StepLocation
        value="New York, NY"
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    const input = screen.getByLabelText(/location/i) as HTMLInputElement
    expect(input.value).toBe('New York, NY')
  })

  it('calls onChange when user types', async () => {
    const user = userEvent.setup()
    const handleChange = vi.fn()
    
    render(
      <StepLocation
        value=""
        onChange={handleChange}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    const input = screen.getByLabelText(/location/i)
    await user.type(input, 'Los Angeles')
    
    expect(handleChange).toHaveBeenCalled()
  })

  it('shows "Use my location" button', () => {
    render(
      <StepLocation
        value=""
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    expect(screen.getByRole('button', { name: /use my location/i })).toBeInTheDocument()
  })

  it('calls onUseGeolocation when button is clicked', async () => {
    const user = userEvent.setup()
    const handleUseGeolocation = vi.fn()
    
    render(
      <StepLocation
        value=""
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={handleUseGeolocation}
      />
    )
    
    const button = screen.getByRole('button', { name: /use my location/i })
    await user.click(button)
    
    expect(handleUseGeolocation).toHaveBeenCalled()
  })

  it('disables continue button when location is empty', () => {
    render(
      <StepLocation
        value=""
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /continue/i })
    expect(button).toBeDisabled()
  })

  it('enables continue button when location is provided', () => {
    render(
      <StepLocation
        value="Chicago, IL"
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    const button = screen.getByRole('button', { name: /continue/i })
    expect(button).not.toBeDisabled()
  })

  it('displays loading state when fetching geolocation', () => {
    render(
      <StepLocation
        value=""
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
        isLoadingLocation={true}
      />
    )
    
    expect(screen.getByText(/getting your location/i)).toBeInTheDocument()
  })

  it('displays step indicator showing step 3 of 4', () => {
    render(
      <StepLocation
        value=""
        onChange={() => {}}
        onNext={() => {}}
        onBack={() => {}}
        onUseGeolocation={() => {}}
      />
    )
    
    expect(screen.getByText(/step 3 of 4/i)).toBeInTheDocument()
  })
})


