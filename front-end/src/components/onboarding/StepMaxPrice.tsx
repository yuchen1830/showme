import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Search } from 'lucide-react'

interface StepMaxPriceProps {
  value: number
  onChange: (value: number) => void
  onSubmit: () => void
  onBack: () => void
}

export function StepMaxPrice({ value, onChange, onSubmit, onBack }: StepMaxPriceProps) {
  return (
    <div className="w-full max-w-md space-y-6">
      <div className="text-center space-y-2">
        <p className="text-sm text-slate-400">Step 4 of 4</p>
        <h2 className="text-2xl font-bold text-white">What's your budget?</h2>
      </div>

      <div className="space-y-2">
        <Label htmlFor="maxPrice" className="text-white">
          Maximum Price (per ticket)
        </Label>
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
            $
          </span>
          <Input
            id="maxPrice"
            type="number"
            min="1"
            value={value || ''}
            onChange={(e) => onChange(Number(e.target.value))}
            placeholder="500"
            className="bg-slate-800 border-slate-700 text-white pl-8"
          />
        </div>
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="outline" className="flex-1">
          Back
        </Button>
        <Button
          onClick={onSubmit}
          disabled={!value || value <= 0}
          className="flex-1"
        >
          <Search className="mr-2 h-4 w-4" />
          Search Tickets
        </Button>
      </div>
    </div>
  )
}


