import { useOnboarding } from '@/application/useOnboarding'
import { StepArtist } from './StepArtist'
import { StepDateRange } from './StepDateRange'
import { StepLocation } from './StepLocation'
import { StepMaxPrice } from './StepMaxPrice'

export function OnboardingWizard() {
  const {
    step,
    query,
    setQuery,
    startDate,
    endDate,
    handleDateChange,
    location,
    setLocation,
    handleUseGeolocation,
    isLoadingLocation,
    maxPrice,
    setMaxPrice,
    nextStep,
    prevStep,
    handleSubmit,
  } = useOnboarding()

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="w-full">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">ShowMe AI</h1>
          <p className="text-slate-300">Find your perfect tickets</p>
        </div>

        {step === 1 && (
          <div className="flex justify-center">
            <StepArtist value={query} onChange={setQuery} onNext={nextStep} />
          </div>
        )}

        {step === 2 && (
          <div className="flex justify-center">
            <StepDateRange
              startDate={startDate}
              endDate={endDate}
              onChange={handleDateChange}
              onNext={nextStep}
              onBack={prevStep}
            />
          </div>
        )}

        {step === 3 && (
          <div className="flex justify-center">
            <StepLocation
              value={location}
              onChange={setLocation}
              onNext={nextStep}
              onBack={prevStep}
              onUseGeolocation={handleUseGeolocation}
              isLoadingLocation={isLoadingLocation}
            />
          </div>
        )}

        {step === 4 && (
          <div className="flex justify-center">
            <StepMaxPrice
              value={maxPrice}
              onChange={setMaxPrice}
              onSubmit={handleSubmit}
              onBack={prevStep}
            />
          </div>
        )}
      </div>
    </div>
  )
}

