import { Button } from '@/components/ui/button'
import { SearchX } from 'lucide-react'

interface EmptyStateProps {
  onModifySearch: () => void
}

export function EmptyState({ onModifySearch }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] text-center space-y-6 p-6">
      <SearchX className="h-20 w-20 text-slate-600" />
      
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-white">No events found</h2>
        <p className="text-slate-400 max-w-md">
          We couldn't find any events matching your search criteria.
          Try adjusting your search criteria to see more results.
        </p>
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 max-w-md">
        <h3 className="text-sm font-semibold text-white mb-3">Try these tips:</h3>
        <ul className="text-sm text-slate-400 space-y-2 text-left">
          <li>• Increase your budget</li>
          <li>• Expand your date range</li>
          <li>• Search for a different artist or event</li>
          <li>• Try a different location</li>
        </ul>
      </div>

      <Button onClick={onModifySearch} size="lg">
        Modify Search
      </Button>
    </div>
  )
}


