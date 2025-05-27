# Cars360 Folder Structure

This document provides a comprehensive overview of the Cars360 project structure and organization.

## 📁 Root Directory

```
Cars360/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CHANGELOG.md                 # Version history and changes
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 SECURITY.md                  # Security policy and reporting
├── 📄 FOLDER_STRUCTURE.md          # This file
├── 📄 package.json                 # Root package configuration
├── 📄 docker-compose.yml           # Docker services configuration
├── 📄 .gitignore                   # Git ignore rules
├── 🔧 setup.sh                     # Unix setup script
├── 🔧 setup.bat                    # Windows setup script
├── 🔧 preview.bat                  # Windows preview script
├── 📊 PROJECT_STATUS.md            # Current project status
├── 📚 DEVELOPMENT_GUIDE.md         # Development workflow guide
├── 📚 PREVIEW_GUIDE.md             # Preview and demo guide
├── 🎨 frontend/                    # Next.js frontend application
├── ⚡ backend/                     # FastAPI backend service
├── 🔗 blockchain/                  # Smart contracts and tests
├── 📊 data/                        # Dataset storage and samples
├── 📚 docs/                        # Comprehensive documentation
├── 🔧 scripts/                     # Utility and deployment scripts
├── 🐳 .github/                     # GitHub workflows and templates
└── 📁 [Generated Folders]          # Auto-generated during build
    ├── node_modules/               # Node.js dependencies (ignored)
    ├── .next/                      # Next.js build output (ignored)
    ├── dist/                       # Distribution builds (ignored)
    └── uploads/                    # User uploaded files (ignored)
```

## 🎨 Frontend Structure (`frontend/`)

```
frontend/
├── 📄 package.json                 # Frontend dependencies and scripts
├── 📄 tsconfig.json               # TypeScript configuration
├── 📄 tailwind.config.js          # Tailwind CSS configuration
├── 📄 next.config.js              # Next.js configuration
├── 📄 .eslintrc.json              # ESLint configuration
├── 📄 prettier.config.js          # Prettier configuration
├── 📄 Dockerfile                  # Docker container configuration
├── 📄 .env.local                  # Environment variables (ignored)
├── 📄 .env.example                # Environment template
├── 🎯 src/                        # Source code directory
│   ├── 📱 app/                    # Next.js App Router pages
│   │   ├── 🏠 page.tsx            # Home page
│   │   ├── 📊 datasets/           # Dataset marketplace
│   │   │   └── page.tsx
│   │   ├── 📤 upload/             # Dataset upload
│   │   │   └── page.tsx
│   │   ├── 📈 dashboard/          # User dashboard
│   │   │   └── page.tsx
│   │   ├── 📊 analytics/          # Analytics page
│   │   │   └── page.tsx
│   │   ├── ⚙️ settings/           # User settings
│   │   │   └── page.tsx
│   │   ├── 🎨 globals.css         # Global styles
│   │   └── 📄 layout.tsx          # Root layout component
│   ├── 🧩 components/             # Reusable UI components
│   │   ├── 🎨 ui/                 # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── [Other UI components]
│   │   ├── 📐 layout/             # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   ├── 📊 charts/             # Chart components
│   │   ├── 📝 forms/              # Form components
│   │   └── 🔧 common/             # Common components
│   ├── 🎣 hooks/                  # Custom React hooks
│   │   ├── useStacks.ts           # Stacks blockchain integration
│   │   ├── useApi.ts              # API interaction hooks
│   │   └── [Other custom hooks]
│   ├── 🌐 contexts/               # React contexts
│   │   ├── StacksContext.tsx      # Stacks wallet context
│   │   ├── AuthContext.tsx        # Authentication context
│   │   └── [Other contexts]
│   ├── 📚 lib/                    # Utility libraries
│   │   ├── utils.ts               # General utilities
│   │   ├── api.ts                 # API client configuration
│   │   ├── constants.ts           # Application constants
│   │   └── [Other utilities]
│   ├── 🏷️ types/                  # TypeScript type definitions
│   │   ├── api.ts                 # API response types
│   │   ├── blockchain.ts          # Blockchain types
│   │   └── [Other type definitions]
│   └── 🔧 utils/                  # Utility functions
│       ├── formatting.ts          # Data formatting
│       ├── validation.ts          # Input validation
│       └── [Other utilities]
├── 📁 public/                     # Static assets
│   ├── 🖼️ images/                # Image assets
│   ├── 🎨 icons/                 # Icon files
│   └── 📄 favicon.ico            # Site favicon
└── 📁 [Build Outputs]             # Generated during build
    ├── .next/                     # Next.js build cache (ignored)
    ├── out/                       # Static export output (ignored)
    └── node_modules/              # Dependencies (ignored)
```

## ⚡ Backend Structure (`backend/`)

```
backend/
├── 📄 requirements.txt            # Python dependencies
├── 📄 main.py                     # FastAPI application entry point
├── 📄 Dockerfile                  # Docker container configuration
├── 📄 .env                        # Environment variables (ignored)
├── 📄 .env.example                # Environment template
├── 🎯 app/                        # Application source code
│   ├── 🌐 api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── v1/                    # API version 1
│   │       ├── __init__.py
│   │       ├── auth.py            # Authentication endpoints
│   │       ├── datasets.py        # Dataset CRUD endpoints
│   │       ├── users.py           # User management endpoints
│   │       ├── analytics.py       # Analytics endpoints
│   │       └── [Other endpoints]
│   ├── 🏗️ core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py              # Application configuration
│   │   ├── database.py            # Database connection
│   │   ├── security.py            # Authentication & authorization
│   │   └── [Other core modules]
│   ├── 🗄️ models/                 # Database models
│   │   ├── __init__.py
│   │   ├── base.py                # Base model class
│   │   ├── user.py                # User model
│   │   ├── dataset.py             # Dataset models
│   │   ├── transaction.py         # Transaction model
│   │   └── [Other models]
│   ├── 🔧 services/               # Business logic services
│   │   ├── __init__.py
│   │   ├── storage.py             # IPFS storage service
│   │   ├── data_processor.py      # Data processing service
│   │   ├── blockchain.py          # Blockchain integration
│   │   └── [Other services]
│   └── 🛠️ utils/                  # Utility functions
│       ├── __init__.py
│       ├── helpers.py             # General helpers
│       ├── validators.py          # Data validation
│       └── [Other utilities]
├── 📁 uploads/                    # File upload directory (ignored)
├── 📁 logs/                       # Application logs (ignored)
└── 📁 [Generated]                 # Auto-generated files
    ├── __pycache__/               # Python cache (ignored)
    ├── .pytest_cache/             # Pytest cache (ignored)
    └── venv/                      # Virtual environment (ignored)
```

## 🔗 Blockchain Structure (`blockchain/`)

```
blockchain/
├── 📄 Clarinet.toml               # Clarinet configuration
├── 📄 settings/                   # Network settings
│   ├── Devnet.toml                # Development network
│   ├── Testnet.toml               # Test network
│   └── Mainnet.toml               # Main network
├── 🔗 contracts/                  # Smart contracts
│   ├── dataset-registry.clar      # Dataset registry contract
│   ├── marketplace.clar           # Marketplace contract
│   ├── access-control.clar        # Access control contract
│   └── [Other contracts]
├── 🧪 tests/                      # Contract tests
│   ├── dataset-registry_test.ts   # Registry tests
│   ├── marketplace_test.ts        # Marketplace tests
│   ├── access-control_test.ts     # Access control tests
│   └── [Other test files]
└── 📁 [Generated]                 # Auto-generated files
    ├── .clarinet/                 # Clarinet cache (ignored)
    └── deployments/               # Deployment artifacts (ignored)
```

## 📊 Data Structure (`data/`)

```
data/
├── 📄 README.md                   # Data documentation
├── 🗂️ raw/                        # Original datasets
│   ├── cars45_scraped_data_raw.csv
│   ├── cars45_scraped_data_raw_1.csv
│   └── [Other raw datasets]
├── 🧹 processed/                  # Cleaned datasets
│   ├── cars45_scraped_data_clean.csv
│   └── [Other processed datasets]
├── 📋 samples/                    # Sample data for testing
│   ├── sample_dataset.csv
│   ├── sample_metadata.json
│   └── [Other samples]
└── 📊 analysis/                   # Data analysis outputs
    ├── market_trends.json
    ├── price_analysis.json
    └── [Other analysis files]
```

## 📚 Documentation Structure (`docs/`)

```
docs/
├── 📄 README.md                   # Documentation index
├── 🚀 installation.md             # Installation guide
├── ⚡ quickstart.md               # Quick start guide
├── 🏗️ architecture.md             # System architecture
├── 🗄️ database-schema.md          # Database design
├── 🌐 api-reference.md            # API documentation
├── 🔗 smart-contracts.md          # Contract documentation
├── 🎨 components.md               # UI components guide
├── 🚀 deployment.md               # Deployment guide
├── 🧪 testing.md                  # Testing guide
├── 🎨 styling.md                  # Style guide
├── 📁 legacy/                     # Legacy documentation
│   ├── original_analysis.ipynb
│   ├── cars45_dashboard.html
│   └── [Other legacy files]
└── 📁 analysis/                   # Data analysis documentation
    ├── market_analysis.png
    ├── price_trends.png
    └── [Other analysis charts]
```

## 🔧 Scripts Structure (`scripts/`)

```
scripts/
├── 📄 README.md                   # Scripts documentation
├── 🔧 setup/                      # Setup scripts
│   ├── install-dependencies.sh
│   ├── setup-database.sh
│   └── configure-environment.sh
├── 🚀 deployment/                 # Deployment scripts
│   ├── deploy-production.sh
│   ├── deploy-staging.sh
│   └── backup-database.sh
├── 🧪 testing/                    # Testing scripts
│   ├── run-all-tests.sh
│   ├── e2e-tests.sh
│   └── performance-tests.sh
└── 🛠️ maintenance/                # Maintenance scripts
    ├── cleanup-logs.sh
    ├── update-dependencies.sh
    └── health-check.sh
```

## 🐳 GitHub Structure (`.github/`)

```
.github/
├── 🔄 workflows/                  # GitHub Actions
│   ├── ci.yml                     # Continuous Integration
│   ├── deploy.yml                 # Deployment workflow
│   └── security.yml               # Security scanning
├── 📋 ISSUE_TEMPLATE/             # Issue templates
│   ├── bug_report.md
│   ├── feature_request.md
│   └── security_report.md
├── 📝 PULL_REQUEST_TEMPLATE.md    # PR template
└── 📄 CODEOWNERS                  # Code ownership rules
```

## 📝 File Naming Conventions

### Frontend (TypeScript/React)
- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useStacks.ts`)
- **Utilities**: camelCase (e.g., `formatPrice.ts`)
- **Types**: PascalCase (e.g., `ApiResponse.ts`)

### Backend (Python)
- **Modules**: snake_case (e.g., `data_processor.py`)
- **Classes**: PascalCase (e.g., `DataProcessor`)
- **Functions**: snake_case (e.g., `process_dataset`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`)

### Smart Contracts (Clarity)
- **Contracts**: kebab-case (e.g., `dataset-registry.clar`)
- **Functions**: kebab-case (e.g., `register-dataset`)
- **Variables**: kebab-case (e.g., `dataset-count`)

### Documentation
- **Files**: kebab-case (e.g., `api-reference.md`)
- **Folders**: kebab-case (e.g., `smart-contracts/`)

## 🔍 Key Directories to Know

### For Developers
- `frontend/src/components/` - UI components
- `backend/app/api/v1/` - API endpoints
- `blockchain/contracts/` - Smart contracts
- `docs/` - Documentation

### For Contributors
- `CONTRIBUTING.md` - Contribution guidelines
- `.github/` - GitHub templates and workflows
- `scripts/` - Utility scripts
- `docs/testing.md` - Testing guide

### For Deployment
- `docker-compose.yml` - Container orchestration
- `frontend/Dockerfile` - Frontend container
- `backend/Dockerfile` - Backend container
- `scripts/deployment/` - Deployment scripts

---

This structure is designed to be scalable, maintainable, and developer-friendly. Each directory has a specific purpose and follows established conventions for its respective technology stack.
