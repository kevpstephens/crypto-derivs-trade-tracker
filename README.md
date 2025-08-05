# 🚀 Crypto Derivatives Trade Tracker

A high-performance, production-ready crypto derivatives trading system backend built with FastAPI, PostgreSQL, and Redis.

[![Tests](https://img.shields.io/badge/tests-14%20passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](Dockerfile)

## 🎯 Overview

This project demonstrates a **production-ready fintech backend** that simulates core functionality of crypto derivatives trading platforms like BitMEX, Binance Futures, or FTX. Built with modern Python technologies and following industry best practices.

### Key Features

- 🏗️ **RESTful API** with automatic OpenAPI documentation
- 🗄️ **PostgreSQL** for persistent trade storage
- ⚡ **Redis** caching for high-performance data retrieval
- 🧮 **Advanced margin calculations** with liquidation price modeling
- 🐳 **Docker containerization** for easy deployment
- 🧪 **Comprehensive test suite** (14 tests, 100% core coverage)
- 📊 **Production-ready architecture** with proper separation of concerns

## 🛠️ Technology Stack

| Component             | Technology              | Purpose                      |
| --------------------- | ----------------------- | ---------------------------- |
| **Backend Framework** | FastAPI 0.116+          | High-performance async API   |
| **Database**          | PostgreSQL 15           | Persistent trade storage     |
| **Cache**             | Redis 7                 | Fast recent trades retrieval |
| **ORM**               | SQLAlchemy 2.0          | Database operations          |
| **Validation**        | Pydantic 2.11+          | Request/response validation  |
| **Testing**           | Pytest 8.0+             | Comprehensive test coverage  |
| **Containerization**  | Docker & Docker Compose | Deployment & orchestration   |

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/kevpstephens/crypto-derivs-trade-tracker.git
cd crypto-derivs-trade-tracker

# Start all services
docker-compose up --build

# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database/redis URLs

# Run the application
uvicorn app.main:app --reload
```

## 🔧 Development Workflow

```bash
# Setup
make install          # Install dependencies
make help            # See all available commands

# Development
make run             # Start development server
make test            # Run test suite
make test-cov        # Run tests with coverage

# Code Quality
make format          # Format code (Black + isort)
make lint            # Check code quality (flake8)

# Docker
make docker-build    # Build containers
make docker-up       # Start full stack
make docker-down     # Stop all services
```

## 📖 API Documentation

### Core Endpoints

| Method | Endpoint                  | Description                   |
| ------ | ------------------------- | ----------------------------- |
| `POST` | `/trades/`                | Create a new derivative trade |
| `GET`  | `/trades/{id}`            | Retrieve specific trade by ID |
| `GET`  | `/trades/recent`          | Get recent trades (cached)    |
| `POST` | `/trades/simulate-margin` | Calculate margin requirements |
| `GET`  | `/health`                 | Health check                  |

### Example Usage

#### Create a Trade

```bash
curl -X POST "http://localhost:8000/trades/" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "BTC-PERP",
       "side": "long",
       "size": "0.1",
       "price": "45000.00",
       "leverage": 10
     }'
```

**Response:**

```json
{
  "id": 1,
  "symbol": "BTC-PERP",
  "side": "long",
  "size": "0.10000000",
  "price": "45000.00",
  "status": "filled",
  "leverage": 10,
  "created_at": "2025-08-04T22:41:41.246206Z",
  "updated_at": null
}
```

#### Simulate Margin Requirements

```bash
curl -X POST "http://localhost:8000/trades/simulate-margin" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "BTC-PERP",
       "side": "long",
       "size": "0.1",
       "price": "50000.00",
       "leverage": 10
     }'
```

**Response:**

```json
{
  "required_margin": "500.00",
  "maintenance_margin": "250.00",
  "liquidation_price": "45250.00",
  "max_loss": "550.00"
}
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   PostgreSQL    │    │     Redis       │
│                 │    │                 │    │                 │
│ • API Routes    │◄──►│ • Trade Storage │    │ • Recent Trades │
│ • Validation    │    │ • Persistence   │    │ • Caching       │
│ • Documentation │    │ • ACID Compliance│   │ • Performance   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│  Service Layer  │    │   Data Models   │
│                 │    │                 │
│ • Business Logic│    │ • SQLAlchemy    │
│ • Margin Calc   │    │ • Pydantic      │
│ • Cache Mgmt    │    │ • Validation    │
└─────────────────┘    └─────────────────┘
```

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_api_complete.py -v
pytest tests/test_services_complete.py -v
```

**Test Coverage:**

- ✅ API endpoints (success & error cases)
- ✅ Margin calculation accuracy
- ✅ Data validation
- ✅ Database operations
- ✅ Cache functionality
- ✅ Edge cases & boundary conditions

## 💡 Key Technical Decisions

### Financial Precision

- Uses `Decimal` for all monetary calculations to avoid floating-point errors
- Proper handling of leverage and margin requirements
- Realistic liquidation price modeling

### Performance Optimization

- Redis caching for frequently accessed recent trades
- Database connection pooling with SQLAlchemy
- Async/await throughout the application stack

### Production Readiness

- Comprehensive error handling and validation
- Health checks and monitoring endpoints
- Docker containerization for consistent deployments
- Environment-based configuration management

## 🔮 Future Enhancements

- [ ] **Authentication & Authorization** (JWT-based)
- [ ] **WebSocket Support** for real-time updates
- [ ] **Market Data Integration** (live price feeds)
- [ ] **Order Book Simulation** (matching engine)
- [ ] **Advanced Risk Management** (portfolio-level limits)
- [ ] **Metrics & Monitoring** (Prometheus/Grafana)
- [ ] **CI/CD Pipeline** (GitHub Actions)

## 📊 Financial Concepts Implemented

### Margin Trading

- **Initial Margin**: Collateral required to open position
- **Maintenance Margin**: Minimum margin to keep position open
- **Liquidation Price**: Price at which position gets forcibly closed
- **Leverage**: Multiplier for position size (1x to 100x)

### Risk Management

- Position size validation
- Leverage limits (1x-100x)
- Margin requirement calculations
- Maximum loss estimation

## 🤝 Contributing

This project demonstrates production-ready development practices:

1. **Clean Architecture**: Separation of concerns with models, services, and API layers
2. **Type Safety**: Full type hints throughout the codebase
3. **Error Handling**: Comprehensive validation and error responses
4. **Testing**: High test coverage with realistic scenarios
5. **Documentation**: Self-documenting code with OpenAPI specs

---
