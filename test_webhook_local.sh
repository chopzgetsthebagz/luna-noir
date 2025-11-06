#!/bin/bash
# Test webhook locally by sending a sample Telegram update

echo "Testing Luna Noir Bot Webhook Locally"
echo "======================================"
echo ""

# Check if server is running
if ! curl -s http://localhost:5000/health > /dev/null; then
    echo "❌ Error: Server is not running on localhost:5000"
    echo "Please start the server first with: make dev"
    exit 1
fi

echo "✓ Server is running"
echo ""

# Test /start command
echo "Sending test /start command..."
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456789,
    "message": {
      "message_id": 1,
      "from": {
        "id": 987654321,
        "is_bot": false,
        "first_name": "TestUser",
        "username": "testuser",
        "language_code": "en"
      },
      "chat": {
        "id": 987654321,
        "first_name": "TestUser",
        "username": "testuser",
        "type": "private"
      },
      "date": 1698765432,
      "text": "/start"
    }
  }'

echo ""
echo ""

# Test /menu command
echo "Sending test /menu command..."
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456790,
    "message": {
      "message_id": 2,
      "from": {
        "id": 987654321,
        "is_bot": false,
        "first_name": "TestUser",
        "username": "testuser",
        "language_code": "en"
      },
      "chat": {
        "id": 987654321,
        "first_name": "TestUser",
        "username": "testuser",
        "type": "private"
      },
      "date": 1698765433,
      "text": "/menu"
    }
  }'

echo ""
echo ""

# Test regular message
echo "Sending test regular message..."
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456791,
    "message": {
      "message_id": 3,
      "from": {
        "id": 987654321,
        "is_bot": false,
        "first_name": "TestUser",
        "username": "testuser",
        "language_code": "en"
      },
      "chat": {
        "id": 987654321,
        "first_name": "TestUser",
        "username": "testuser",
        "type": "private"
      },
      "date": 1698765434,
      "text": "Hello Luna!"
    }
  }'

echo ""
echo ""
echo "======================================"
echo "✓ Test complete!"
echo "Check the server logs to see the JSON output"
echo "======================================"

