export interface Seat {
  id: string
  section: string
  row: string
  seatNumber: string
  price: number
  available: boolean
  aiValueScore: number // 0-100, higher is better value
}

export function createSeat(params: {
  id: string
  section: string
  row: string
  seatNumber: string
  price: number
  available: boolean
  aiValueScore: number
}): Seat {
  return {
    id: params.id,
    section: params.section,
    row: params.row,
    seatNumber: params.seatNumber,
    price: params.price,
    available: params.available,
    aiValueScore: params.aiValueScore,
  }
}

export function isHighValueSeat(seat: Seat, threshold = 70): boolean {
  return seat.available && seat.aiValueScore >= threshold
}

