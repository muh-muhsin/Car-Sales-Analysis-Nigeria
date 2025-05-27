# Cars360 API Reference

## Base URL

- **Production:** `https://api.cars360.ng`
- **Staging:** `https://staging-api.cars360.ng`
- **Development:** `http://localhost:8000`

## Authentication

Cars360 API uses wallet-based authentication with JWT tokens.

### Connect Wallet
```http
POST /api/v1/auth/wallet
Content-Type: application/json

{
  "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
  "signature": "0x...",
  "message": "Sign in to Cars360"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 691200,
  "user": {
    "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
    "verified": false,
    "role": "basic_user"
  }
}
```

### Authorization Header
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Datasets

### List Datasets
```http
GET /api/v1/datasets?page=1&limit=20&sort=created_at&order=desc&search=toyota
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20, max: 100)
- `sort` (string): Sort field (created_at, price, title, rating)
- `order` (string): Sort order (asc, desc)
- `search` (string): Search query
- `category` (string): Filter by category
- `min_price` (int): Minimum price in microSTX
- `max_price` (int): Maximum price in microSTX

**Response:**
```json
{
  "datasets": [
    {
      "id": 1,
      "title": "Nigerian Car Sales Q1 2024",
      "description": "Comprehensive car sales data for Q1 2024",
      "price": 5000000,
      "owner": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
      "ipfs_hash": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
      "records_count": 2500,
      "file_size": 1024000,
      "file_type": "csv",
      "tags": ["automotive", "nigeria", "sales"],
      "rating": 4.5,
      "rating_count": 12,
      "total_sales": 45,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "active": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "pages": 8
  }
}
```

### Get Dataset Details
```http
GET /api/v1/datasets/{dataset_id}
```

**Response:**
```json
{
  "id": 1,
  "title": "Nigerian Car Sales Q1 2024",
  "description": "Comprehensive car sales data for Q1 2024",
  "price": 5000000,
  "owner": {
    "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
    "verified": true,
    "reputation": 4.8
  },
  "metadata": {
    "columns": ["price", "brand", "model", "year", "region"],
    "date_range": "2024-01-01 to 2024-03-31",
    "regions": ["Lagos", "Abuja", "Kano"],
    "brands": ["Toyota", "Honda", "Mercedes-Benz"]
  },
  "ipfs_hash": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
  "records_count": 2500,
  "file_size": 1024000,
  "file_type": "csv",
  "tags": ["automotive", "nigeria", "sales"],
  "rating": 4.5,
  "rating_count": 12,
  "total_sales": 45,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "active": true,
  "has_access": false
}
```

### Preview Dataset
```http
GET /api/v1/datasets/{dataset_id}/preview
```

**Response:**
```json
{
  "preview": [
    {
      "price": 5400000,
      "brand": "Honda",
      "model": "CR-V",
      "year": 2007,
      "region": "Rivers State"
    },
    {
      "price": 7875000,
      "brand": "Toyota",
      "model": "Camry",
      "year": 2008,
      "region": "Lagos State"
    }
  ],
  "columns": ["price", "brand", "model", "year", "region"],
  "total_records": 2500
}
```

### Upload Dataset
```http
POST /api/v1/datasets/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}

file: [binary data]
title: "Nigerian Car Sales Q1 2024"
description: "Comprehensive car sales data for Q1 2024"
price: 5000000
tags: "automotive,nigeria,sales"
```

**Response:**
```json
{
  "dataset_id": 1,
  "ipfs_hash": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
  "metadata": {
    "title": "Nigerian Car Sales Q1 2024",
    "description": "Comprehensive car sales data for Q1 2024",
    "records_count": 2500,
    "file_type": "csv"
  },
  "message": "Dataset uploaded successfully"
}
```

### Purchase Dataset
```http
POST /api/v1/datasets/{dataset_id}/purchase
Authorization: Bearer {token}
```

**Response:**
```json
{
  "transaction_id": "0x1234567890abcdef",
  "dataset_id": 1,
  "amount_paid": 5000000,
  "platform_fee": 250000,
  "seller_amount": 4750000,
  "purchase_date": "2024-01-15T15:30:00Z",
  "access_granted": true
}
```

### Download Dataset
```http
GET /api/v1/datasets/{dataset_id}/download
Authorization: Bearer {token}
```

**Response:** Binary file download with appropriate headers.

## Users

### Get User Profile
```http
GET /api/v1/users/profile
Authorization: Bearer {token}
```

**Response:**
```json
{
  "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
  "role": "verified_seller",
  "verified": true,
  "reputation_score": 4.8,
  "total_uploads": 5,
  "total_purchases": 12,
  "total_earned": 25000000,
  "withdrawable": 5000000,
  "joined_at": "2024-01-01T00:00:00Z",
  "last_active": "2024-01-15T15:30:00Z"
}
```

### Get User Datasets
```http
GET /api/v1/users/datasets
Authorization: Bearer {token}
```

**Response:**
```json
{
  "uploaded": [
    {
      "id": 1,
      "title": "Nigerian Car Sales Q1 2024",
      "total_sales": 45,
      "total_earned": 22500000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "purchased": [
    {
      "id": 2,
      "title": "Lagos Car Market Analysis",
      "purchase_date": "2024-01-10T14:20:00Z",
      "amount_paid": 3000000
    }
  ]
}
```

### Request Verification
```http
POST /api/v1/users/verification
Authorization: Bearer {token}
Content-Type: application/json

{
  "documents_uri": "ipfs://QmVerificationDocs123",
  "business_name": "AutoData Nigeria Ltd",
  "business_type": "Data Provider"
}
```

## Analytics

### Market Trends
```http
GET /api/v1/analytics/market-trends?period=30d&region=lagos
```

**Response:**
```json
{
  "period": "30d",
  "region": "lagos",
  "trends": {
    "average_price": 8500000,
    "price_change": 5.2,
    "popular_brands": ["Toyota", "Honda", "Mercedes-Benz"],
    "sales_volume": 1250,
    "volume_change": -2.1
  },
  "price_distribution": [
    {"range": "0-5M", "count": 450},
    {"range": "5M-10M", "count": 380},
    {"range": "10M+", "count": 420}
  ]
}
```

### Price Insights
```http
GET /api/v1/analytics/price-insights?brand=toyota&model=camry
```

**Response:**
```json
{
  "brand": "toyota",
  "model": "camry",
  "insights": {
    "average_price": 7200000,
    "median_price": 6800000,
    "price_range": {
      "min": 3500000,
      "max": 15000000
    },
    "depreciation_rate": 12.5,
    "market_share": 18.3
  }
}
```

## Error Responses

### Error Format
```json
{
  "error": {
    "code": "DATASET_NOT_FOUND",
    "message": "Dataset with ID 999 not found",
    "details": {
      "dataset_id": 999
    }
  }
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `DATASET_NOT_FOUND` | 404 | Dataset does not exist |
| `ALREADY_PURCHASED` | 409 | User already owns this dataset |
| `INSUFFICIENT_FUNDS` | 402 | Not enough STX for purchase |
| `INVALID_FILE_TYPE` | 400 | Unsupported file format |
| `FILE_TOO_LARGE` | 413 | File exceeds size limit |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |

## Rate Limits

- **Authenticated users:** 1000 requests/hour
- **Unauthenticated users:** 100 requests/hour
- **Upload endpoints:** 10 requests/hour
- **Download endpoints:** 50 requests/hour

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642694400
```

## SDKs and Libraries

### JavaScript/TypeScript
```bash
npm install @cars360/sdk
```

```typescript
import { Cars360SDK } from '@cars360/sdk'

const sdk = new Cars360SDK({
  apiUrl: 'https://api.cars360.ng',
  network: 'mainnet'
})

// List datasets
const datasets = await sdk.datasets.list({ limit: 10 })

// Purchase dataset
const purchase = await sdk.datasets.purchase(1)
```

### Python
```bash
pip install cars360-python
```

```python
from cars360 import Cars360Client

client = Cars360Client(
    api_url='https://api.cars360.ng',
    access_token='your_token'
)

# List datasets
datasets = client.datasets.list(limit=10)

# Get dataset details
dataset = client.datasets.get(1)
```
