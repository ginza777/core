# Docker Setup for Core Project

## 🚀 Overview

This project now includes a complete Docker environment with:
- **Django Application** with optimized admin panel
- **Celery Workers** (10 parallel workers)
- **Redis** message broker
- **PostgreSQL** database
- **Prometheus** metrics collection
- **Grafana** monitoring dashboards
- **Nginx** reverse proxy with rate limiting

## ✨ New Features Added

### 1. Download Status Tracking
- **Download Status Field**: Tracks file download progress
- **Status Options**: Pending, Downloading, Downloaded, Failed, Skipped
- **Timing Information**: Download start/completion timestamps
- **Error Tracking**: Detailed error messages for failed downloads
- **Admin Display**: Color-coded status indicators with icons

### 2. Enhanced Admin Panel
- **Download Status Column**: Shows current download state
- **File Path Display**: Shows local file storage location
- **Performance Optimization**: Reduced page sizes, caching, better database settings
- **Status Filtering**: Filter documents by download status

### 3. Monitoring & Observability
- **Prometheus Metrics**: HTTP requests, response times, Celery tasks
- **Grafana Dashboards**: Real-time monitoring with beautiful visualizations
- **Download Statistics**: Track download success/failure rates
- **Performance Metrics**: Database connections, Redis usage, task processing

## 🐳 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.12+ (for local development)

### 1. Automated Setup (Recommended)
```bash
# Run the automated setup script
./setup_docker.sh
```

### 2. Manual Setup
```bash
# Create directories
mkdir -p media/documents staticfiles monitoring/{prometheus,grafana/{provisioning/{dashboards,datasources}}} nginx/conf.d

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start services
docker-compose up --build -d
```

## 📊 Service Access

| Service | URL | Credentials | Description |
|---------|-----|-------------|-------------|
| **Django Admin** | http://localhost/admin/ | Create superuser | Main application admin |
| **Grafana** | http://localhost:3000 | admin/admin123 | Monitoring dashboards |
| **Prometheus** | http://localhost:9090 | None | Metrics collection |
| **PostgreSQL** | localhost:5432 | core_user/core_password | Database |
| **Redis** | localhost:6379 | None | Message broker |
| **Nginx** | http://localhost/ | None | Reverse proxy |

## 🔧 Configuration

### Environment Variables
```bash
# Django
DJANGO_SETTINGS_MODULE=core_project.settings

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Database
POSTGRES_DB=core_db
POSTGRES_USER=core_user
POSTGRES_PASSWORD=core_password
```

### Celery Configuration
- **Workers**: 10 parallel processes
- **Beat Schedule**: Every 3 days at 2 AM
- **Task Limits**: 5 min soft, 10 min hard
- **Retry Policy**: Exponential backoff with 3 max retries

### Nginx Configuration
- **Rate Limiting**: Admin (5 req/s), API (10 req/s)
- **Security Headers**: XSS protection, CSRF, content security
- **Gzip Compression**: Optimized for performance
- **File Uploads**: 100MB max body size

## 📈 Monitoring Dashboard

### Grafana Dashboard Features
1. **HTTP Metrics**
   - Request rate and response times
   - Error rates and status codes
   - Performance trends

2. **Celery Metrics**
   - Task processing rates
   - Success/failure ratios
   - Worker utilization

3. **System Metrics**
   - Redis connections
   - PostgreSQL performance
   - Resource usage

4. **Download Statistics**
   - Download success rates
   - Processing times
   - Error patterns

## 🗄️ Database Schema

### Document Model Updates
```python
class Document(models.Model):
    # ... existing fields ...
    
    # New download tracking fields
    download_status = models.CharField(
        max_length=20,
        choices=DOWNLOAD_STATUS_CHOICES,
        default='pending'
    )
    download_started_at = models.DateTimeField(null=True, blank=True)
    download_completed_at = models.DateTimeField(null=True, blank=True)
    download_error = models.TextField(null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
```

### Download Status Values
- **pending**: File not yet processed
- **downloading**: Currently being downloaded
- **downloaded**: Successfully downloaded
- **failed**: Download failed with error
- **skipped**: No file URL available

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using the ports
   lsof -i :8000,3000,9090,5432,6379
   ```

2. **Service Not Starting**
   ```bash
   # Check logs
   docker-compose logs -f [service_name]
   
   # Restart specific service
   docker-compose restart [service_name]
   ```

3. **Database Connection Issues**
   ```bash
   # Check PostgreSQL logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

4. **Celery Worker Issues**
   ```bash
   # Check worker status
   docker-compose exec web celery -A core_project inspect active
   
   # Restart workers
   docker-compose restart celery_worker
   ```

### Performance Tuning

1. **Adjust Worker Count**
   ```bash
   # Modify docker-compose.yml
   celery_worker:
     command: celery -A core_project worker --loglevel=info --concurrency=15
   ```

2. **Database Optimization**
   ```bash
   # Add to settings.py
   DATABASES = {
       'default': {
           'OPTIONS': {
               'timeout': 30,
               'max_connections': 100,
           }
       }
   }
   ```

3. **Redis Configuration**
   ```bash
   # Add to docker-compose.yml
   redis:
     command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
   ```

## 🚀 Production Deployment

### Security Considerations
1. **Change Default Passwords**
   - Grafana admin password
   - PostgreSQL credentials
   - Django secret key

2. **SSL/TLS Configuration**
   - Add Let's Encrypt certificates
   - Configure HTTPS in Nginx
   - Enable secure headers

3. **Network Security**
   - Use internal networks
   - Restrict external access
   - Implement firewall rules

### Scaling
1. **Horizontal Scaling**
   ```bash
   # Scale workers
   docker-compose up --scale celery_worker=20 -d
   
   # Scale web services
   docker-compose up --scale web=3 -d
   ```

2. **Load Balancing**
   - Configure Nginx upstream
   - Add health checks
   - Implement sticky sessions

## 📝 Maintenance

### Regular Tasks
1. **Database Backups**
   ```bash
   docker-compose exec db pg_dump -U core_user core_db > backup.sql
   ```

2. **Log Rotation**
   ```bash
   # Add logrotate configuration
   docker-compose exec nginx logrotate /etc/logrotate.conf
   ```

3. **Metrics Cleanup**
   ```bash
   # Prometheus data retention
   # Configure in prometheus.yml
   --storage.tsdb.retention.time=7d
   ```

### Updates
1. **Application Updates**
   ```bash
   git pull origin main
   docker-compose build --no-cache
   docker-compose up -d
   ```

2. **Infrastructure Updates**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

## 🎯 Next Steps

1. **Custom Metrics**: Add application-specific Prometheus metrics
2. **Alerting**: Configure Grafana alerts for critical issues
3. **Log Aggregation**: Implement centralized logging with ELK stack
4. **CI/CD**: Set up automated deployment pipelines
5. **Backup Strategy**: Implement automated backup and recovery

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Celery Best Practices](https://docs.celeryproject.org/en/stable/userguide/tasks.html)

---

**Happy Monitoring! 🚀📊**
