export type TextLocation = {
  type: 'text'
  value: string
}

export type CoordsLocation = {
  type: 'coords'
  lat: number
  lng: number
}

export type Location = TextLocation | CoordsLocation

export interface SearchCriteria {
  query: string
  startDate: Date
  endDate: Date
  location: Location
  maxPrice: number
}

export function createSearchCriteria(params: {
  query: string
  startDate: Date
  endDate: Date
  location: Location
  maxPrice: number
}): SearchCriteria {
  return {
    query: params.query,
    startDate: params.startDate,
    endDate: params.endDate,
    location: params.location,
    maxPrice: params.maxPrice,
  }
}

export function isValidSearchCriteria(criteria: SearchCriteria): boolean {
  // Query must not be empty
  if (!criteria.query.trim()) {
    return false
  }

  // End date must be after or equal to start date
  if (criteria.endDate < criteria.startDate) {
    return false
  }

  // Max price must be positive
  if (criteria.maxPrice <= 0) {
    return false
  }

  // Location validation
  if (criteria.location.type === 'text' && !criteria.location.value.trim()) {
    return false
  }

  return true
}

