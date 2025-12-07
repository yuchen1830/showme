import { Loader2 } from 'lucide-react'

export function LoadingState() {
  return (
    <div
      className="flex flex-col items-center justify-center min-h-[50vh] space-y-4"
      role="status"
      aria-label="Loading search results"
    >
      <Loader2 className="h-12 w-12 text-purple-500 animate-spin" data-loading />
      <div className="text-center space-y-2">
        <p className="text-xl font-semibold text-white">Searching for events...</p>
        <p className="text-sm text-slate-400">
          Finding the best tickets across multiple vendors
        </p>
      </div>
    </div>
  )
}


