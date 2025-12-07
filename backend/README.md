# ShowMe Backend

FastAPI backend for ticket aggregation and AI-powered seat map analysis.

## 🚀 Quick Start

1. **Start the server:**
```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI
uvicorn src.api.main:app --reload --port 8000
```

2. **Visit API docs:** http://localhost:8000/docs

3. **Test health endpoint:** http://localhost:8000/api/v1/health

## 📖 API Endpoints

- `GET /` - Service info
- `GET /api/v1/health` - Health check
- `POST /api/v1/search` - Search events
- `GET /docs` - Interactive API documentation

## 🏗️ Architecture

Clean Architecture with four layers:
- **Domain**: Pure business logic (entities, services)
- **Application**: Use cases (search orchestration)
- **Infrastructure**: External integrations (API clients)
- **API**: FastAPI routes and schemas

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src
```

## 🔑 Environment Variables

Create `.env` file:
```
TICKETMASTER_API_KEY=your_key
STUBHUB_API_KEY=your_key
SEATGEEK_API_KEY=your_key
```

## 📦 Dependencies

Install with:
```bash
pip install -r requirements.txt
```

## 🐳 Docker

Start PostgreSQL and Redis:
```bash
docker-compose up -d
```

---

**Status**: ✅ Ready for frontend integration

