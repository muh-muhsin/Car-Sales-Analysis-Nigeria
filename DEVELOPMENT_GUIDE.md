# Cars360 Development Guide

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **PostgreSQL 12+** (or use cloud database)
- **Git**

### Automated Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Cars360

# Run setup script
chmod +x setup.sh
./setup.sh
```

### Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configurations
nano .env
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local with your configurations
nano .env.local
```

#### 3. Database Setup

```bash
# Create PostgreSQL database
createdb cars360

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://username:password@localhost:5432/cars360
```

#### 4. Smart Contract Deployment

```bash
cd blockchain

# Install Clarinet (if not already installed)
# Follow instructions at: https://github.com/hirosystems/clarinet

# Deploy to testnet
clarinet deploy --testnet

# Update CONTRACT_ADDRESS in environment files
```

## 🏃‍♂️ Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Blockchain (Optional):**
```bash
cd blockchain
clarinet devnet start
```

### Access Points

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Blockchain Explorer:** http://localhost:8080 (if running devnet)

## 🔧 Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/cars360

# Blockchain
STACKS_NETWORK=testnet
STACKS_API_URL=https://api.testnet.hiro.so
CONTRACT_ADDRESS=your-deployed-contract-address

# IPFS
IPFS_API_URL=http://localhost:5001
IPFS_GATEWAY_URL=http://localhost:8080

# Security
SECRET_KEY=your-super-secret-key
```

### Frontend Environment Variables

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Blockchain
NEXT_PUBLIC_STACKS_NETWORK=testnet
NEXT_PUBLIC_CONTRACT_ADDRESS=your-deployed-contract-address

# IPFS
NEXT_PUBLIC_IPFS_GATEWAY=https://ipfs.io/ipfs/
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Smart Contract Tests

```bash
cd blockchain
clarinet test
```

## 📁 Project Structure

```
Cars360/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic
│   ├── main.py             # FastAPI app
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── hooks/         # Custom hooks
│   │   └── lib/           # Utilities
│   └── package.json       # Node.js dependencies
├── blockchain/            # Smart contracts
│   ├── contracts/         # Clarity contracts
│   ├── tests/            # Contract tests
│   └── Clarinet.toml     # Clarinet config
└── data/                 # Sample datasets
```

## 🔄 Development Workflow

### 1. Feature Development

1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement changes
3. Test locally
4. Commit and push
5. Create pull request

### 2. Database Migrations

```bash
cd backend
source venv/bin/activate

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

### 3. Smart Contract Updates

```bash
cd blockchain

# Test contracts
clarinet test

# Deploy to testnet
clarinet deploy --testnet

# Update contract addresses in environment files
```

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
psql -l | grep cars360
```

**2. IPFS Connection Error**
```bash
# Install and start IPFS
ipfs daemon
```

**3. Wallet Connection Issues**
- Ensure Hiro Wallet is installed
- Check network settings (testnet/mainnet)
- Clear browser cache

**4. Smart Contract Deployment Fails**
- Check Clarinet installation
- Verify network configuration
- Ensure sufficient STX balance

### Logs and Debugging

**Backend Logs:**
```bash
cd backend
tail -f logs/app.log
```

**Frontend Logs:**
Check browser console and terminal output

**Smart Contract Logs:**
```bash
cd blockchain
clarinet console
```

## 📚 Additional Resources

- [Stacks Documentation](https://docs.stacks.co/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Clarinet Documentation](https://github.com/hirosystems/clarinet)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📞 Support

- **GitHub Issues:** [Create an issue](https://github.com/your-repo/issues)
- **Email:** support@cars360.ng
- **Discord:** [Join our community](https://discord.gg/cars360)
