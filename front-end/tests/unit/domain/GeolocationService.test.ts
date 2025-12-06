import { describe, it, expect, vi, beforeEach } from 'vitest'
import { 
  GeolocationService, 
  GeolocationError,
  type GeolocationResult 
} from '@/domain/services/GeolocationService'

describe('GeolocationService', () => {
  let service: GeolocationService

  beforeEach(() => {
    service = new GeolocationService()
  })

  describe('getCurrentPosition', () => {
    it('returns coordinates when geolocation succeeds', async () => {
      const mockPosition = {
        coords: {
          latitude: 40.7128,
          longitude: -74.006,
          accuracy: 10,
        },
      }

      const mockGeolocation = {
        getCurrentPosition: vi.fn((success) => success(mockPosition)),
      }
      
      vi.stubGlobal('navigator', { geolocation: mockGeolocation })

      const result = await service.getCurrentPosition()

      expect(result).toEqual({
        lat: 40.7128,
        lng: -74.006,
      })
    })

    it('throws GeolocationError when permission denied', async () => {
      const mockGeolocation = {
        getCurrentPosition: vi.fn((_, error) => 
          error({ code: 1, message: 'User denied geolocation' })
        ),
      }
      
      vi.stubGlobal('navigator', { geolocation: mockGeolocation })

      await expect(service.getCurrentPosition()).rejects.toThrow(GeolocationError)
      
      try {
        await service.getCurrentPosition()
      } catch (e) {
        expect((e as GeolocationError).type).toBe('permission_denied')
      }
    })

    it('throws GeolocationError when position unavailable', async () => {
      const mockGeolocation = {
        getCurrentPosition: vi.fn((_, error) => 
          error({ code: 2, message: 'Position unavailable' })
        ),
      }
      
      vi.stubGlobal('navigator', { geolocation: mockGeolocation })

      try {
        await service.getCurrentPosition()
      } catch (e) {
        expect((e as GeolocationError).type).toBe('position_unavailable')
      }
    })

    it('throws GeolocationError when timeout', async () => {
      const mockGeolocation = {
        getCurrentPosition: vi.fn((_, error) => 
          error({ code: 3, message: 'Timeout' })
        ),
      }
      
      vi.stubGlobal('navigator', { geolocation: mockGeolocation })

      try {
        await service.getCurrentPosition()
      } catch (e) {
        expect((e as GeolocationError).type).toBe('timeout')
      }
    })

    it('throws GeolocationError when geolocation not supported', async () => {
      vi.stubGlobal('navigator', { geolocation: undefined })

      try {
        await service.getCurrentPosition()
      } catch (e) {
        expect((e as GeolocationError).type).toBe('not_supported')
      }
    })
  })

  describe('isSupported', () => {
    it('returns true when geolocation is available', () => {
      vi.stubGlobal('navigator', { 
        geolocation: { getCurrentPosition: vi.fn() } 
      })

      expect(service.isSupported()).toBe(true)
    })

    it('returns false when geolocation is not available', () => {
      vi.stubGlobal('navigator', { geolocation: undefined })

      expect(service.isSupported()).toBe(false)
    })
  })
})

