# Testing the ShowMe Backend

## ✅ Quick Verification Test

Run this to verify the backend is working:

```bash
cd /Users/kd2/projects/showme/backend
source venv/bin/activate
python test_backend.py
```

Expected output: All tests passing ✅

## 🚀 Start the Server

```bash
cd /Users/kd2/projects/showme/backend
source venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## 🧪 Test the API

### Option 1: Browser

Visit these URLs:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Service Info**: http://localhost:8000

### Option 2: curl

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Search (demo mode - no API keys needed)
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "artist": "Taylor Swift",
    "location": "New York, NY",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "max_price": 300.00
  }'
```

### Option 3: Python Script

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Search
response = requests.post(
    "http://localhost:8000/api/v1/search",
    json={
        "artist": "Taylor Swift",
        "location": "New York, NY",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "max_price": 300.00
    }
)
print(response.json())
```

## 🔗 Frontend Integration Test

### 1. Start Backend

```bash
cd /Users/kd2/projects/showme/backend
source venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```

### 2. Start Frontend (in another terminal)

```bash
cd /Users/kd2/projects/showme/front-end
npm run dev
```

### 3. Create Frontend API Client

Create `front-end/src/services/api.ts`:

```typescript
const API_URL = 'http://localhost:8000/api/v1';

export interface SearchParams {
  artist: string;
  location: string;
  latitude: number;
  longitude: number;
  maxPrice?: number;
}

export const searchEvents = async (params: SearchParams) => {
  const response = await fetch(`${API_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });
  
  if (!response.ok) {
    throw new Error('Search failed');
  }
  
  return response.json();
};

export const checkHealth = async () => {
  const response = await fetch(`${API_URL}/health`);
  return response.json();
};
```

### 4. Test in Frontend

```typescript
import { searchEvents, checkHealth } from './services/api';

// Check backend health
const health = await checkHealth();
console.log('Backend status:', health.status);

// Search events
const results = await searchEvents({
  artist: 'Taylor Swift',
  location: 'New York, NY',
  latitude: 40.7128,
  longitude: -74.0060,
  maxPrice: 300,
});

console.log('Events found:', results.total);
```

## 📊 Expected Responses

### Health Check Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-12-07T..."
}
```

### Search Response (Demo Mode)

```json
{
  "events": [],
  "total": 0
}
```

Note: In demo mode (without real API keys), the backend returns empty results. This is normal!

### Search Response (With Real API Keys)

```json
{
  "events": [
    {
      "id": "evt_123",
      "name": "Taylor Swift - The Eras Tour",
      "artist": "Taylor Swift",
      "venue_name": "MetLife Stadium",
      "date": "2024-06-15T19:30:00",
      "location": "East Rutherford, NJ",
      "latitude": 40.8128,
      "longitude": -74.0742,
      "price_tiers": [
        {
          "name": "General",
          "min_price": 150.00,
          "max_price": 250.00,
          "currency": "USD"
        }
      ],
      "min_price": 150.00,
      "max_price": 250.00,
      "vendor": "ticketmaster",
      "vendor_url": "https://ticketmaster.com/event/evt_123"
    }
  ],
  "total": 1
}
```

## 🐛 Troubleshooting

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Module not found errors

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### CORS errors in frontend

The backend is already configured for CORS with:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (Create React App default)

If using a different port, update `src/api/main.py`:

```python
allow_origins=["http://localhost:YOUR_PORT"]
```

## ✨ Next Steps

1. ✅ Backend is working
2. Add real API keys to `.env` for production data
3. Integrate with your frontend
4. Deploy to production

---

**Backend Status**: ✅ READY FOR USE

