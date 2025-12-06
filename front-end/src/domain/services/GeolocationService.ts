export type GeolocationErrorType = 
  | 'permission_denied'
  | 'position_unavailable'
  | 'timeout'
  | 'not_supported'
  | 'unknown'

export class GeolocationError extends Error {
  constructor(
    public readonly type: GeolocationErrorType,
    message?: string
  ) {
    super(message || type)
    this.name = 'GeolocationError'
  }
}

export interface GeolocationResult {
  lat: number
  lng: number
}

export class GeolocationService {
  isSupported(): boolean {
    return typeof navigator !== 'undefined' && 'geolocation' in navigator && !!navigator.geolocation
  }

  getCurrentPosition(): Promise<GeolocationResult> {
    return new Promise((resolve, reject) => {
      if (!this.isSupported()) {
        reject(new GeolocationError('not_supported', 'Geolocation is not supported'))
        return
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          })
        },
        (error) => {
          const errorType = this.mapErrorCode(error.code)
          reject(new GeolocationError(errorType, error.message))
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0,
        }
      )
    })
  }

  private mapErrorCode(code: number): GeolocationErrorType {
    switch (code) {
      case 1:
        return 'permission_denied'
      case 2:
        return 'position_unavailable'
      case 3:
        return 'timeout'
      default:
        return 'unknown'
    }
  }
}

