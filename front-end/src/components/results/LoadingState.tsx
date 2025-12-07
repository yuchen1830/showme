import { useState, useEffect } from 'react'
import { Loader2, Search, Globe, Ticket, Sparkles } from 'lucide-react'

const stages = [
  { icon: Search, text: 'Researching events...', duration: 30 },
  { icon: Globe, text: 'Searching Ticketmaster...', duration: 60 },
  { icon: Ticket, text: 'Searching TickPick...', duration: 90 },
  { icon: Sparkles, text: 'Analyzing best deals...', duration: 120 },
]

export function LoadingState() {
  const [elapsedTime, setElapsedTime] = useState(0)
  const [currentStage, setCurrentStage] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedTime((prev) => prev + 1)
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    // Progress through stages based on elapsed time
    const stage = stages.findIndex((s) => elapsedTime < s.duration)
    setCurrentStage(stage === -1 ? stages.length - 1 : stage)
  }, [elapsedTime])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`
  }

  const CurrentIcon = stages[currentStage]?.icon || Sparkles

  return (
    <div
      className="flex flex-col items-center justify-center min-h-[60vh] space-y-6"
      role="status"
      aria-label="Loading search results"
    >
      {/* Main spinner with icon */}
      <div className="relative">
        <div className="absolute inset-0 rounded-full bg-purple-500/20 animate-ping" />
        <div className="relative bg-slate-800 rounded-full p-6 border border-purple-500/50">
          <CurrentIcon className="h-8 w-8 text-purple-400" />
        </div>
      </div>

      {/* Status text */}
      <div className="text-center space-y-2">
        <p className="text-xl font-semibold text-white">
          {stages[currentStage]?.text || 'Searching...'}
        </p>
        <p className="text-sm text-slate-400">
          AI agents are browsing real ticket sites
        </p>
      </div>

      {/* Progress stages */}
      <div className="flex items-center gap-2 mt-4">
        {stages.map((_, index) => (
          <div
            key={index}
            className={`h-2 w-8 rounded-full transition-all duration-500 ${index <= currentStage
              ? 'bg-purple-500'
              : 'bg-slate-700'
              }`}
          />
        ))}
      </div>

      {/* Timer */}
      <div className="text-center space-y-1">
        <p className="text-sm text-slate-500">
          Elapsed: {formatTime(elapsedTime)}
        </p>
        <p className="text-xs text-slate-600">
          Usually takes 2-4 minutes
        </p>
      </div>

      {/* Spinner */}
      <Loader2 className="h-5 w-5 text-slate-500 animate-spin" data-loading />
    </div>
  )
}

