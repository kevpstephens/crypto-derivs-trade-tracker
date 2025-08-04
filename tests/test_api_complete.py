from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data


def test_root_endpoint(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Crypto Derivatives Trade Tracker API" in data["message"]


def test_create_trade_success(client: TestClient):
    """Test successful trade creation"""
    trade_data = {
        "symbol": "BTC-PERP",
        "side": "long",
        "size": "0.1",
        "price": "45000.00",
        "leverage": 10,
    }

    response = client.post("/trades/", json=trade_data)
    assert response.status_code == 201

    data = response.json()
    assert data["symbol"] == "BTC-PERP"
    assert data["side"] == "long"
    assert data["status"] == "filled"
    assert data["leverage"] == 10
    assert "id" in data
    assert "created_at" in data


def test_create_trade_validation_errors(client: TestClient):
    """Test trade creation with invalid data"""
    # Test negative size
    invalid_trade = {
        "symbol": "BTC-PERP",
        "side": "long",
        "size": "-0.1",  # Negative size should fail
        "price": "45000.00",
        "leverage": 10,
    }

    response = client.post("/trades/", json=invalid_trade)
    assert response.status_code == 422

    # Test invalid leverage
    invalid_leverage = {
        "symbol": "BTC-PERP",
        "side": "long",
        "size": "0.1",
        "price": "45000.00",
        "leverage": 150,  # Too high leverage
    }

    response = client.post("/trades/", json=invalid_leverage)
    assert response.status_code == 422


def test_get_trade_by_id(client: TestClient):
    """Test retrieving a trade by ID"""
    # First create a trade
    trade_data = {
        "symbol": "ETH-PERP",
        "side": "short",
        "size": "1.0",
        "price": "3000.00",
        "leverage": 5,
    }

    create_response = client.post("/trades/", json=trade_data)
    trade_id = create_response.json()["id"]

    # Then fetch it
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == trade_id
    assert data["symbol"] == "ETH-PERP"
    assert data["side"] == "short"


def test_get_nonexistent_trade(client: TestClient):
    """Test retrieving a non-existent trade"""
    response = client.get("/trades/999999")
    assert response.status_code == 404
    assert "Trade not found" in response.json()["detail"]


def test_margin_simulation_long(client: TestClient):
    """Test margin simulation for long position"""
    margin_data = {
        "symbol": "BTC-PERP",
        "side": "long",
        "size": "0.1",
        "price": "50000.00",
        "leverage": 10,
    }

    response = client.post("/trades/simulate-margin", json=margin_data)
    assert response.status_code == 200

    data = response.json()
    assert "required_margin" in data
    assert "maintenance_margin" in data
    assert "liquidation_price" in data
    assert "max_loss" in data

    # Verify calculations
    assert float(data["required_margin"]) == 500.0  # 0.1 * 50000 / 10
    assert float(data["maintenance_margin"]) == 250.0  # 50% of required margin


def test_margin_simulation_short(client: TestClient):
    """Test margin simulation for short position"""
    margin_data = {
        "symbol": "BTC-PERP",
        "side": "short",
        "size": "0.5",
        "price": "40000.00",
        "leverage": 5,
    }

    response = client.post("/trades/simulate-margin", json=margin_data)
    assert response.status_code == 200

    data = response.json()
    # 0.5 * 40000 / 5 = 4000
    assert float(data["required_margin"]) == 4000.0


def test_get_recent_trades(client: TestClient):
    """Test getting recent trades"""
    # Create multiple trades
    trades_data = [
        {
            "symbol": "BTC-PERP",
            "side": "long",
            "size": "0.1",
            "price": "45000.00",
            "leverage": 10,
        },
        {
            "symbol": "ETH-PERP",
            "side": "short",
            "size": "1.0",
            "price": "3000.00",
            "leverage": 5,
        },
        {
            "symbol": "SOL-PERP",
            "side": "long",
            "size": "10.0",
            "price": "100.00",
            "leverage": 3,
        },
    ]

    for trade_data in trades_data:
        client.post("/trades/", json=trade_data)

    # Get recent trades
    response = client.get("/trades/recent?limit=10")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_api_openapi_schema(client: TestClient):
    """Test that OpenAPI schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Crypto Derivatives Trade Tracker"
