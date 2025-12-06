import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface StepDateRangeProps {
  startDate: Date | null
  endDate: Date | null
  onChange: (field: 'start' | 'end', date: Date) => void
  onNext: () => void
  onBack: () => void
}

export function StepDateRange({ startDate, endDate, onChange, onNext, onBack }: StepDateRangeProps) {
  const formatDateForInput = (date: Date | null) => {
    if (!date) return ''
    return date.toISOString().split('T')[0]
  }

  const handleDateChange = (field: 'start' | 'end', value: string) => {
    if (value) {
      onChange(field, new Date(value))
    }
  }

  return (
    <div className="w-full max-w-md space-y-6">
      <div className="text-center space-y-2">
        <p className="text-sm text-slate-400">Step 2 of 4</p>
        <h2 className="text-2xl font-bold text-white">When are you available?</h2>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="startDate" className="text-white">
            Start Date
          </Label>
          <Input
            id="startDate"
            type="date"
            value={formatDateForInput(startDate)}
            onChange={(e) => handleDateChange('start', e.target.value)}
            className="bg-slate-800 border-slate-700 text-white"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="endDate" className="text-white">
            End Date
          </Label>
          <Input
            id="endDate"
            type="date"
            value={formatDateForInput(endDate)}
            onChange={(e) => handleDateChange('end', e.target.value)}
            min={formatDateForInput(startDate)}
            className="bg-slate-800 border-slate-700 text-white"
          />
        </div>
      </div>

      <div className="flex gap-3">
        <Button onClick={onBack} variant="outline" className="flex-1">
          Back
        </Button>
        <Button
          onClick={onNext}
          disabled={!startDate || !endDate}
          className="flex-1"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}

