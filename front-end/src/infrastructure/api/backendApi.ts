/**
 * Backend API Integration
 * Connects to the ShowMe FastAPI backend running on localhost:8000
 */

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000/api/v1'

// Backend response types
interface BackendPriceTier {
  name: string
  min_price: number
  max_price: number
  currency: string
}

interface BackendEvent {
  id: string
  name: string
  artist: string
  venue_name: string
  date: string
  location: string
  latitude: number
  longitude: number
  price_tiers: BackendPriceTier[]
  min_price: number
  max_price: number
  vendor: string
  vendor_url: string
}

interface BackendSearchResponse {
  events: BackendEvent[]
  total: number
}

// Backend request type
interface BackendSearchRequest {
  artist: string
  location: string
  latitude: number
  longitude: number
  start_date?: string
  end_date?: string
  max_price?: number
}

export class BackendApi {
  /**
   * Search events from the backend
   */
  async searchEvents(params: {
    query: string
    location: { lat: number; lng: number }
    locationText: string
    startDate?: Date
    endDate?: Date
    maxPrice?: number
  }): Promise<BackendSearchResponse> {
    const request: BackendSearchRequest = {
      artist: params.query,
      location: params.locationText,
      latitude: params.location.lat,
      longitude: params.location.lng,
      max_price: params.maxPrice,
    }

    // Add dates if provided
    if (params.startDate) {
      request.start_date = params.startDate.toISOString()
    }
    if (params.endDate) {
      request.end_date = params.endDate.toISOString()
    }

    const response = await fetch(`${API_BASE_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Search failed' }))
      throw new Error(error.detail || `Search failed: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Check backend health
   */
  async checkHealth(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${API_BASE_URL}/health`)
    if (!response.ok) {
      throw new Error('Backend is not healthy')
    }
    return response.json()
  }
}

// Export singleton instance
export const backendApi = new BackendApi()

