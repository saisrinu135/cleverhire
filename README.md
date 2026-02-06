# CleverHire - AI-Powered Job Matching Platform

CleverHire is a full-stack job matching platform that uses AI to intelligently match candidates with job opportunities. Built with Django REST Framework, Next.js, and powered by Google's Generative AI.

## 🚀 Features

- **AI-Powered Job Matching**: Intelligent candidate-job matching using Google Gemini AI
- **Real-time Notifications**: Celery-based background task processing
- **Advanced Search**: Elasticsearch integration for fast job and candidate search
- **Geospatial Queries**: PostGIS support for location-based job searches
- **File Storage**: S3/R2 compatible storage for resumes and media
- **JWT Authentication**: Secure token-based authentication
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2.9 + Django REST Framework
- **Database**: PostgreSQL with PostGIS
- **Cache/Queue**: Redis + RabbitMQ
- **Task Queue**: Celery + Celery Beat
- **Search**: Elasticsearch
- **AI**: Google Generative AI (Gemini)
- **Storage**: S3/Cloudflare R2
- **Server**: Gunicorn + Nginx

### Frontend
- **Framework**: Next.js 16.1.5 (React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI
- **Forms**: React Hook Form
- **HTTP Client**: Axios

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 16 with PostGIS
- Redis 7+
- RabbitMQ 3.12+
- Nginx (for production)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/saisrinu135/cleverhire.git
cd cleverhire
```

### 2. Environment Setup

Create `.env` file in root directory:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=cleverhire.saisrinu.online

# Database
POSTGRES_DB=cleverhire
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
DB_HOST=database
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# RabbitMQ
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=your-secure-password
CELERY_BROKER_URL=amqp://admin:your-secure-password@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Elasticsearch
ELASTICSEARCH_HOST=localhost:9200

# Email (Gmail SMTP)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 / Cloudflare R2
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_ENDPOINT_URL=https://your-endpoint.r2.cloudflarestorage.com

# Frontend
FRONTEND_URL=frontendurl
NEXT_PUBLIC_API_URL=backedapi

# CORS
CORS_ALLOWED_ORIGINS=originlist
```

### 3. Start Services

```bash
# Build and start all containers
docker compose up -d --build

# Check logs
docker compose logs -f

# Check running containers
docker ps
```

### 4. Create Django Superuser

```bash
docker exec -it cleverhire_backend python manage.py createsuperuser
```

### 5. Access Application

- **Frontend**: https://cleverhire.saisrinu.online
- **API**: https://cleverhire.saisrinu.online/api
- **Admin Panel**: https://cleverhire.saisrinu.online/admin/
- **API Docs**: https://cleverhire.saisrinu.online/api/schema/docs/
- **Flower (Celery Monitor)**: https://cleverhire.saisrinu.online/flower/

## 🏗️ Project Structure

```
cleverhire/
├── backend/                    # Django backend
│   ├── apps/                   # Django apps
│   │   ├── applications/       # Job applications
│   │   ├── core/              # Core utilities
│   │   ├── jobs/              # Job listings
│   │   ├── notifications/     # Notifications system
│   │   └── users/             # User management
│   ├── config/                # Django settings
│   │   └── settings/          # Environment-specific settings
│   ├── templates/             # Email templates
│   ├── Dockerfile             # Backend container
│   ├── requirements.txt       # Python dependencies
│   └── manage.py
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom hooks
│   │   ├── lib/              # Utilities
│   │   ├── services/         # API services
│   │   └── types/            # TypeScript types
│   ├── Dockerfile            # Frontend container
│   └── package.json
├── nginx/                     # Nginx configuration
│   └── nginx.conf
├── docker-compose.yml         # Docker orchestration
├── .env                       # Environment variables
└── README.md
```

## 🔧 Development

### Backend Development

```bash
# Enter backend container
docker exec -it cleverhire_backend bash

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test
```

### Frontend Development

```bash
# Enter frontend container
docker exec -it cleverhire_frontend bash

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🚀 Production Deployment

### Server Setup

1. **Install Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Nginx
sudo apt install nginx -y

# Install Certbot
sudo apt install certbot python3-certbot-nginx -y
```

2. **Clone Repository**

```bash
sudo mkdir -p /opt/cleverhire
cd /opt/cleverhire
git clone <repository-url> .
```

3. **Configure Environment**

```bash
# Create .env file
sudo nano .env
# Add production environment variables
```

4. **Setup Nginx**

```bash
# Copy nginx config
sudo cp /etc/nginx/sites-available/cleverhire /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

5. **Get SSL Certificate**

```bash
sudo certbot --nginx -d cleverhire.saisrinu.online
```

6. **Start Application**

```bash
cd /opt/cleverhire
docker compose up -d --build
```


## 📊 Monitoring


### Celery Monitoring

Access Flower dashboard at: https://cleverhire.saisrinu.online/flower/


## 🔒 Security

- JWT token-based authentication
- HTTPS enforced via Nginx
- CORS configured for specific origins
- Environment variables for sensitive data
- SQL injection protection via Django ORM
- XSS protection enabled
- CSRF protection enabled

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request


## 📞 Support

For issues and questions, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using Django, Next.js, and AI**
