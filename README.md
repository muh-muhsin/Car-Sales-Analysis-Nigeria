# Cars360 🚗💎

> **A Decentralized Marketplace for Nigerian Car Sales Data Built on Stacks Blockchain**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Stacks](https://img.shields.io/badge/Stacks-5546FF?logo=stacks&logoColor=white)](https://stacks.co/)

Cars360 is a revolutionary decentralized marketplace that transforms how Nigerian car sales data is shared, monetized, and accessed. Built on the Stacks blockchain, it provides a secure, transparent, and efficient platform for data providers and consumers in Nigeria's automotive industry.

## 🌟 Features

### 🔒 **Blockchain-Powered Security**
- Smart contracts ensure transparent and secure transactions
- Immutable data provenance and ownership tracking
- Decentralized storage with IPFS integration

### 📊 **Quality Data Marketplace**
- Verified Nigerian car sales datasets
- Advanced data validation and quality scoring
- Real-time market analytics and insights

### 💰 **Fair Monetization**
- Direct payments to data providers in STX tokens
- Transparent fee structure (5% platform fee)
- Automated royalty distribution system

### 🌍 **Nigerian Market Focus**
- Specialized for Nigerian automotive market
- Local payment methods and currency support
- Regional data insights and analytics

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+ and pip
- **PostgreSQL** 12+
- **Git**

### Installation

```bash
# Clone the repository
git clone https://github.com/muhsinmuhammad/Cars360.git
cd Cars360

# Run automated setup
chmod +x setup.sh
./setup.sh

# Or manual setup
npm run setup
```

### Development

```bash
# Start all services
npm run dev

# Or start individually
npm run dev:frontend    # Frontend at http://localhost:3000
npm run dev:backend     # Backend at http://localhost:8000
npm run dev:blockchain  # Blockchain devnet
```

## 📁 Project Structure

```
Cars360/
├── 🎨 frontend/          # Next.js frontend application
│   ├── src/
│   │   ├── app/          # App router pages
│   │   ├── components/   # Reusable UI components
│   │   ├── contexts/     # React contexts
│   │   ├── hooks/        # Custom React hooks
│   │   └── lib/          # Utility functions
│   └── package.json
├── ⚡ backend/           # FastAPI backend service
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Database models
│   │   └── services/     # Business logic
│   └── requirements.txt
├── 🔗 blockchain/        # Smart contracts
│   ├── contracts/        # Clarity contracts
│   ├── tests/           # Contract tests
│   └── Clarinet.toml
├── 📊 data/             # Dataset storage
│   ├── raw/             # Original datasets
│   ├── processed/       # Cleaned datasets
│   └── samples/         # Sample data
└── 📚 docs/             # Documentation
    ├── api/             # API documentation
    ├── contracts/       # Smart contract docs
    └── deployment/      # Deployment guides
```

## 🛠 Technology Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion
- **State Management**: React Query + Context API
- **Web3**: Stacks Connect for wallet integration

### Backend
- **Framework**: FastAPI with Python 3.9+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for performance optimization
- **Storage**: IPFS for decentralized file storage
- **Validation**: Pydantic for data validation

### Blockchain
- **Platform**: Stacks Blockchain
- **Language**: Clarity for smart contracts
- **Tools**: Clarinet for development and testing
- **Integration**: Hiro APIs for blockchain interaction

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **Deployment**: Nginx reverse proxy
- **Monitoring**: Comprehensive logging and analytics
- **Security**: SSL/TLS encryption and secure headers

## 📖 Usage Examples

### For Data Providers

```typescript
// Upload a new dataset
const uploadDataset = async (file: File, metadata: DatasetMetadata) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('title', metadata.title)
  formData.append('description', metadata.description)
  formData.append('price', metadata.price.toString())
  
  const response = await fetch('/api/v1/datasets/upload', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  })
  
  return response.json()
}
```

### For Data Consumers

```typescript
// Purchase and download a dataset
const purchaseDataset = async (datasetId: number) => {
  // Initiate blockchain transaction
  const transaction = await openContractCall({
    contractAddress: CONTRACT_ADDRESS,
    contractName: 'marketplace',
    functionName: 'purchase-dataset',
    functionArgs: [uintCV(datasetId)],
  })
  
  // Download after successful payment
  const downloadUrl = await getDatasetDownloadUrl(datasetId)
  return downloadUrl
}
```

## 🔧 API Documentation

### Authentication
```bash
# Authenticate with wallet signature
POST /api/v1/auth/wallet
{
  "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "signature": "...",
  "message": "Sign in to Cars360"
}
```

### Datasets
```bash
# List datasets with filtering
GET /api/v1/datasets?search=toyota&tags=lagos&sort=price

# Get dataset details
GET /api/v1/datasets/{id}

# Upload new dataset
POST /api/v1/datasets/upload
```

### Analytics
```bash
# Get marketplace statistics
GET /api/v1/analytics/marketplace-stats

# Get price trends
GET /api/v1/analytics/price-trends?days=30
```

## 🚀 Deployment

### Development Environment

```bash
# Using Docker Compose
docker-compose up -d

# Manual setup
npm run setup
npm run dev
```

### Production Deployment

```bash
# Build for production
npm run build

# Deploy to cloud provider
npm run deploy

# Or use Docker
docker build -t cars360 .
docker run -p 3000:3000 cars360
```

For detailed deployment instructions, see [docs/deployment.md](docs/deployment.md).

## 🧪 Testing

```bash
# Run all tests
npm test

# Frontend tests
cd frontend && npm test

# Backend tests
cd backend && pytest

# Smart contract tests
cd blockchain && clarinet test

# End-to-end tests
npm run test:e2e
```

## 📊 Data Sources

Cars360 includes a comprehensive dataset of Nigerian car sales:

- **2,600+ verified listings** from Cars45.com
- **46 car brands** with detailed specifications
- **13 Nigerian states** represented
- **Real-time market data** and pricing trends

## 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of conduct
- Development process
- Coding standards
- Testing requirements
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Muhammad Muhsin Muhammad**
- 🌍 Location: Abuja, Nigeria
- 💼 Role: Web3 Developer & Data Scientist
- 📧 Email: muhammad.m1601550@st.futminna.edu.ng
- 🔗 LinkedIn: [Muhammad Muhsin Muhammad](https://www.linkedin.com/in/muhsinmuhammad/)
- 🐦 Twitter: [@DataPeritus](https://x.com/DataPeritus)

## 🙏 Acknowledgments

- **Stacks Foundation** for blockchain infrastructure
- **Cars45.com** for initial dataset
- **Nigerian automotive community** for market insights
- **Open source contributors** for tools and libraries

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/muhsinmuhammad/Cars360/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/muhsinmuhammad/Cars360/discussions)
- 📧 **Email**: muhammad.m1601550@st.futminna.edu.ng

---

<div align="center">

**Built with ❤️ in Nigeria for the Nigerian automotive industry**

[🌐 Website](https://cars360.ng) • [📖 Documentation](https://docs.cars360.ng) • [🚀 Demo](https://demo.cars360.ng)

</div>
