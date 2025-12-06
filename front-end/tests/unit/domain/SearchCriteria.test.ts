import { describe, it, expect } from 'vitest'
import { 
  SearchCriteria, 
  createSearchCriteria, 
  isValidSearchCriteria,
  type Location 
} from '@/domain/entities/SearchCriteria'

describe('SearchCriteria', () => {
  describe('createSearchCriteria', () => {
    it('creates search criteria with all required fields', () => {
      const criteria = createSearchCriteria({
        query: 'Taylor Swift',
        startDate: new Date('2025-06-01'),
        endDate: new Date('2025-06-30'),
        location: { type: 'text', value: 'New York, NY' },
        maxPrice: 500,
      })

      expect(criteria.query).toBe('Taylor Swift')
      expect(criteria.startDate).toEqual(new Date('2025-06-01'))
      expect(criteria.endDate).toEqual(new Date('2025-06-30'))
      expect(criteria.location).toEqual({ type: 'text', value: 'New York, NY' })
      expect(criteria.maxPrice).toBe(500)
    })

    it('creates search criteria with coordinates location', () => {
      const criteria = createSearchCriteria({
        query: 'Coldplay',
        startDate: new Date('2025-07-01'),
        endDate: new Date('2025-07-31'),
        location: { type: 'coords', lat: 40.7128, lng: -74.006 },
        maxPrice: 300,
      })

      expect(criteria.location).toEqual({ type: 'coords', lat: 40.7128, lng: -74.006 })
    })
  })

  describe('isValidSearchCriteria', () => {
    it('returns true for valid criteria', () => {
      const criteria = createSearchCriteria({
        query: 'Taylor Swift',
        startDate: new Date('2025-06-01'),
        endDate: new Date('2025-06-30'),
        location: { type: 'text', value: 'New York, NY' },
        maxPrice: 500,
      })

      expect(isValidSearchCriteria(criteria)).toBe(true)
    })

    it('returns false when query is empty', () => {
      const criteria = createSearchCriteria({
        query: '',
        startDate: new Date('2025-06-01'),
        endDate: new Date('2025-06-30'),
        location: { type: 'text', value: 'New York, NY' },
        maxPrice: 500,
      })

      expect(isValidSearchCriteria(criteria)).toBe(false)
    })

    it('returns false when end date is before start date', () => {
      const criteria = createSearchCriteria({
        query: 'Taylor Swift',
        startDate: new Date('2025-06-30'),
        endDate: new Date('2025-06-01'),
        location: { type: 'text', value: 'New York, NY' },
        maxPrice: 500,
      })

      expect(isValidSearchCriteria(criteria)).toBe(false)
    })

    it('returns false when max price is zero or negative', () => {
      const criteria = createSearchCriteria({
        query: 'Taylor Swift',
        startDate: new Date('2025-06-01'),
        endDate: new Date('2025-06-30'),
        location: { type: 'text', value: 'New York, NY' },
        maxPrice: 0,
      })

      expect(isValidSearchCriteria(criteria)).toBe(false)
    })

    it('returns false when text location is empty', () => {
      const criteria = createSearchCriteria({
        query: 'Taylor Swift',
        startDate: new Date('2025-06-01'),
        endDate: new Date('2025-06-30'),
        location: { type: 'text', value: '' },
        maxPrice: 500,
      })

      expect(isValidSearchCriteria(criteria)).toBe(false)
    })
  })
})

