import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { MapPin } from 'lucide-react'

interface StepLocationProps {
  value: string
  onChange: (value: string) => void
  onNext: () => void
  onBack: () => void
  onUseGeolocation: () => void
  isLoadingLocation?: boolean
}

export function StepLocation({
  value,
  onChange,
  onNext,
  onBack,
  onUseGeolocation,
  isLoadingLocation = false,
}: StepLocationProps) {
  return (
    <div className="w-full max-w-md space-y-6">
      <div className="text-center space-y-2">
        <p className="text-sm text-slate-400">Step 3 of 4</p>
        <h2 className="text-2xl font-bold text-white">Where are you located?</h2>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="location" className="text-white">
            Location
          </Label>
          <Input
            id="location"
            type="text"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder="e.g., New York, NY or 10001"
            className="bg-slate-800 border-slate-700 text-white"
            disabled={isLoadingLocation}
          />
        </div>

        <Button
          onClick={onUseGeolocation}
          variant="outline"
          className="w-full"
          disabled={isLoadingLocation}
        >
          <MapPin className="mr-2 h-4 w-4" />
          {isLoadingLocation ? 'Getting your location...' : 'Use my location'}
        </Button>
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="outline" className="flex-1">
          Back
        </Button>
        <Button
          onClick={onNext}
          disabled={!value.trim() || isLoadingLocation}
          className="flex-1"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}

