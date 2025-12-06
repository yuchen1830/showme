import { useSearch } from '@/application/useSearch'
import { ResultsView } from '@/components/results/ResultsView'
import { EmptyState } from '@/components/results/EmptyState'
import { LoadingState } from '@/components/results/LoadingState'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'

export function ResultsPage() {
  const {
    events,
    isLoading,
    error,
    searchCriteria,
    handleEventClick,
    handleModifySearch,
  } = useSearch()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-900">
        <LoadingState />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6">
        <div className="text-center space-y-4">
          <p className="text-red-400">{error}</p>
          <Button onClick={handleModifySearch}>Back to Search</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900">
      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-6">
          <Button
            onClick={handleModifySearch}
            variant="ghost"
            className="text-slate-400 hover:text-white"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Modify Search
          </Button>
        </div>

        {searchCriteria && (
          <div className="mb-6 bg-slate-800 border border-slate-700 rounded-lg p-4">
            <p className="text-sm text-slate-400">
              Searching for <span className="text-white font-semibold">{searchCriteria.query}</span>
              {' • '}
              {searchCriteria.startDate.toLocaleDateString()} - {searchCriteria.endDate.toLocaleDateString()}
              {' • '}
              Max ${searchCriteria.maxPrice}
            </p>
          </div>
        )}

        {events.length > 0 ? (
          <ResultsView events={events} onEventClick={handleEventClick} />
        ) : (
          <EmptyState onModifySearch={handleModifySearch} />
        )}
      </div>
    </div>
  )
}

