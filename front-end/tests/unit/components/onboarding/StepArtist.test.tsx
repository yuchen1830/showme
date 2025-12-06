import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { StepArtist } from '@/components/onboarding/StepArtist'

describe('StepArtist', () => {
  it('renders artist/event input field', () => {
    render(<StepArtist value="" onChange={() => {}} onNext={() => {}} />)
    
    expect(screen.getByLabelText(/artist or event/i)).toBeInTheDocument()
  })

  it('displays the current value', () => {
    render(<StepArtist value="Taylor Swift" onChange={() => {}} onNext={() => {}} />)
    
    const input = screen.getByLabelText(/artist or event/i) as HTMLInputElement
    expect(input.value).toBe('Taylor Swift')
  })

  it('calls onChange when user types', async () => {
    const user = userEvent.setup()
    const handleChange = vi.fn()
    
    render(<StepArtist value="" onChange={handleChange} onNext={() => {}} />)
    
    const input = screen.getByLabelText(/artist or event/i)
    await user.type(input, 'Coldplay')
    
    expect(handleChange).toHaveBeenCalled()
  })

  it('disables continue button when value is empty', () => {
    render(<StepArtist value="" onChange={() => {}} onNext={() => {}} />)
    
    const button = screen.getByRole('button', { name: /continue/i })
    expect(button).toBeDisabled()
  })

  it('enables continue button when value is provided', () => {
    render(<StepArtist value="Beyoncé" onChange={() => {}} onNext={() => {}} />)
    
    const button = screen.getByRole('button', { name: /continue/i })
    expect(button).not.toBeDisabled()
  })

  it('calls onNext when continue button is clicked', async () => {
    const user = userEvent.setup()
    const handleNext = vi.fn()
    
    render(<StepArtist value="Drake" onChange={() => {}} onNext={handleNext} />)
    
    const button = screen.getByRole('button', { name: /continue/i })
    await user.click(button)
    
    expect(handleNext).toHaveBeenCalled()
  })

  it('displays step indicator showing step 1 of 4', () => {
    render(<StepArtist value="" onChange={() => {}} onNext={() => {}} />)
    
    expect(screen.getByText(/step 1 of 4/i)).toBeInTheDocument()
  })
})

