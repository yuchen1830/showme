export interface Venue {
  id: string
  name: string
  address: string
  lat: number
  lng: number
}

export function createVenue(params: {
  id: string
  name: string
  address: string
  lat: number
  lng: number
}): Venue {
  return {
    id: params.id,
    name: params.name,
    address: params.address,
    lat: params.lat,
    lng: params.lng,
  }
}


