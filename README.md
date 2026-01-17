# Unified Compliance Platform

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Python-3.11+-yellow" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109-red" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18-61DAFB" alt="React">
</p>

<p align="center">
  <strong>A comprehensive, enterprise-grade compliance management platform supporting multiple regulatory frameworks with AI-powered automation</strong>
</p>

---

## 🚀 Features

### Multi-Framework Compliance
- **DPDP Act** - India's Digital Personal Data Protection Act (2023)
- **SOC 2** - Service Organization Control 2 Trust Services Criteria
- **GDPR** - EU General Data Protection Regulation
- **HIPAA** - Health Insurance Portability and Accountability Act
- **ISO 27001** - Information Security Management System
- **NIST CSF** - Cybersecurity Framework
- **CMMC** - Cybersecurity Maturity Model Certification

### Core Capabilities
- 📊 **Real-time Dashboard** - Live compliance status, risk scores, and progress tracking
- 🔍 **AI-Powered PII Detection** - Automatic personal data identification using Microsoft Presidio
- 📝 **Consent Management** - Multi-language consent capture with cryptographic proof
- 📋 **DSR Automation** - Data Subject Request handling (Access, Correction, Deletion, Portability)
- 📈 **Assessment Workflows** - Create, track, and complete compliance assessments
- 📑 **Automated Reporting** - Generate compliance reports (PDF, Excel, JSON)
- 🔐 **Audit Trail** - Immutable audit logging for all compliance activities
- 🔐 **Role-Based Access** - Multi-tenant architecture with granular permissions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React + TypeScript Frontend               │
│                   (Vite, Tailwind CSS, Recharts)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│   │ Auth        │ │ DPDP        │ │ Frameworks          │  │
│   │ (JWT/OAuth) │ │ Engine      │ │ (SOC2, GDPR...)     │  │
│   └─────────────┘ └─────────────┘ └─────────────────────┘  │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│   │ Assessments │ │ Reports     │ │ ML Services         │  │
│   └─────────────┘ └─────────────┘ └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│   │ PostgreSQL  │ │ Redis       │ │ Celery + Redis      │  │
│   │ (Primary)   │ │ (Cache)     │ │ (Background Jobs)   │  │
│   └─────────────┘ └─────────────┘ └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language |
| FastAPI 0.109 | API framework (async, high-performance) |
| SQLAlchemy 2.0 | Database ORM (async) |
| PostgreSQL 15 | Primary database |
| Redis 7 | Caching, rate limiting, Celery broker |
| Microsoft Presidio | PII detection and anonymization |
| JWT + Bcrypt | Authentication & encryption |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| Tailwind CSS | Styling |
| Recharts | Data visualization |
| React Router | Navigation |
| Axios | HTTP client |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Local development |
| GitHub Actions | CI/CD |
| Prometheus | Monitoring |

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/unified-compliance-platform.git
cd unified-compliance-platform

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/unified-compliance-platform.git
cd unified-compliance-platform

# Backend setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Frontend setup
cd frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start development servers
# Terminal 1 - Backend
uvicorn src.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 📁 Project Structure

```
unified-compliance-platform/
├── src/
│   ├── api/                    # FastAPI endpoints
│   │   ├── auth.py            # Authentication (JWT, OAuth2)
│   │   ├── dpdpa.py           # DPDP Act compliance
│   │   ├── frameworks.py      # Framework management
│   │   ├── assessments.py     # Assessment workflows
│   │   ├── reports.py         # Report generation
│   │   └── health.py          # Health checks
│   ├── core/                  # Core utilities
│   │   ├── config.py          # Settings management
│   │   ├── database.py        # Database connection
│   │   └── logging.py         # Structured logging
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py            # User, Tenant, RefreshToken
│   │   ├── assessment.py      # Framework, Assessment, DSR
│   │   └── audit.py           # Audit logging
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py            # Authentication schemas
│   │   ├── framework.py       # Framework schemas
│   │   └── dpdpa.py           # DPDP schemas
│   ├── services/              # Business logic
│   │   ├── auth.py            # Auth service
│   │   └── frameworks/        # Framework compliance engines
│   │       ├── soc2.py        # SOC2 controls (118)
│   │       ├── gdpr.py        # GDPR controls (20+)
│   │       ├── hipaa.py       # HIPAA controls (75+)
│   │       └── iso27001.py    # ISO27001 controls (93+)
│   └── main.py                # Application entry point
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Dashboard, Login, etc.
│   │   ├── services/          # API client
│   │   └── App.tsx            # Main app component
│   ├── package.json
│   └── vite.config.ts
├── tests/                     # Test suite
│   └── unit/
│       └── test_compliance.py # Unit tests
├── docker-compose.yml         # Docker configuration
├── pyproject.toml             # Python dependencies
├── pytest.ini                 # Pytest configuration
├── .github/workflows/         # CI/CD pipeline
│   └── ci-cd.yml
└── README.md                  # This file
```

---

## 🔌 API Documentation

Once the application is running, access the interactive API documentation:

| Endpoint | Description |
|----------|-------------|
| `/api/docs` | Swagger UI - Interactive API documentation |
| `/api/redoc` | ReDoc - Alternative API documentation |
| `/api/metrics` | Prometheus metrics endpoint |

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new tenant and admin user
- `POST /api/v1/auth/login` - Login and receive JWT tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user profile

#### DPDP Compliance
- `POST /api/v1/dpdpa/scan` - Start data discovery scan
- `GET /api/v1/dpdpa/scans` - List all scans
- `POST /api/v1/dpdpa/consent/session` - Create consent session
- `POST /api/v1/dpdpa/dsr` - Create DSR request
- `GET /api/v1/dpdpa/dashboard` - DPDP dashboard metrics

#### Frameworks
- `GET /api/v1/frameworks` - List all frameworks
- `GET /api/v1/frameworks/{id}` - Get framework details
- `POST /api/v1/frameworks` - Create custom framework

#### Assessments
- `GET /api/v1/assessments` - List all assessments
- `POST /api/v1/assessments` - Create new assessment
- `GET /api/v1/assessments/{id}` - Get assessment details
- `PUT /api/v1/assessments/{id}` - Update assessment
- `POST /api/v1/assessments/{id}/start` - Start assessment
- `POST /api/v1/assessments/{id}/controls` - Submit control status
- `POST /api/v1/assessments/{id}/complete` - Complete assessment

#### Reports
- `POST /api/v1/reports/generate` - Generate compliance report
- `GET /api/v1/reports/download/{id}` - Download report
- `GET /api/v1/reports/templates` - List report templates

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_compliance.py
```

---

## 🚢 Deployment

### Production Deployment Checklist

1. **Environment Variables**
   - Generate strong secrets (JWT, encryption keys)
   - Configure production database
   - Enable SSL/TLS

2. **Database Security**
   - Enable PostgreSQL authentication
   - Configure SSL connections
   - Set up regular backups

3. **Security Hardening**
   - Enable rate limiting
   - Configure CORS for production domains
   - Set up WAF (Web Application Firewall)

4. **Monitoring**
   - Configure Prometheus scraping
   - Set up Grafana dashboards
   - Configure alerting

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

---

## 📊 Supported Compliance Frameworks

| Framework | Controls | Description |
|-----------|----------|-------------|
| **DPDP** | 50+ | India's Digital Personal Data Protection Act |
| **SOC 2** | 118 | Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy) |
| **GDPR** | 20+ | EU General Data Protection Regulation |
| **HIPAA** | 75+ | US Healthcare Privacy & Security Rules |
| **ISO 27001** | 93+ | Information Security Management System |
| **NIST CSF** | 100+ | Cybersecurity Framework |
| **CMMC** | 110+ | Defense Contracting Security Requirements |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For support, please open an issue on GitHub or contact:
- **Email**: support@compliance.example.com
- **Issues**: GitHub Issues

---

<p align="center">
  Built with ❤️ for enterprise compliance
</p>
