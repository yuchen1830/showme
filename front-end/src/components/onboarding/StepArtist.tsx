import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface StepArtistProps {
  value: string
  onChange: (value: string) => void
  onNext: () => void
}

export function StepArtist({ value, onChange, onNext }: StepArtistProps) {
  return (
    <div className="w-full max-w-md space-y-6">
      <div className="text-center space-y-2">
        <p className="text-sm text-slate-400">Step 1 of 4</p>
        <h2 className="text-2xl font-bold text-white">Who do you want to see?</h2>
      </div>

      <div className="space-y-2">
        <Label htmlFor="artist" className="text-white">
          Artist or Event
        </Label>
        <Input
          id="artist"
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="e.g., Taylor Swift, Coldplay"
          className="bg-slate-800 border-slate-700 text-white"
        />
      </div>

      <Button
        onClick={onNext}
        disabled={!value.trim()}
        className="w-full"
      >
        Continue
      </Button>
    </div>
  )
}


