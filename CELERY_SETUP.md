# Celery Setup and Configuration

## Overview
This project now includes Celery for background task processing, automatic file downloads, and periodic data updates.

## Features Added

### 1. File Download System
- **Automatic file downloads**: When products are parsed, files are automatically downloaded and saved locally
- **10 parallel workers**: Files are processed concurrently for better performance
- **Random timeouts**: 1-5 second random delays to prevent blocking
- **File path tracking**: Local file paths are stored in the database

### 2. Periodic Data Updates
- **Every 3 days**: Data is automatically updated at 2 AM every 3 days
- **Duplicate checking**: Product ID 327540 is checked and ignored if exists
- **Smart processing**: Only processes first 10 pages to avoid long-running tasks

### 3. Admin Panel Improvements
- **Performance optimization**: Reduced page sizes, caching, and better database settings
- **File status display**: Shows download status and local file paths
- **Clickable links**: Direct download links for files

## Setup Instructions

### 1. Install Redis
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Start Celery Services

#### Option A: Using Management Command (Recommended)
```bash
# Start both worker and beat
python manage.py start_celery

# Start only worker
python manage.py start_celery --worker-only

# Start only beat scheduler
python manage.py start_celery --beat-only

# Custom number of workers
python manage.py start_celery --workers 15
```

#### Option B: Manual Commands
```bash
# Terminal 1: Start Beat Scheduler
celery -A core_project beat --loglevel=info --scheduler=django_celery_beat.schedulers:DatabaseScheduler

# Terminal 2: Start Worker
celery -A core_project worker --loglevel=info --concurrency=10
```

### 5. Test Celery
```bash
python test_celery.py
```

## Configuration

### Celery Settings (core_project/celery.py)
- **Broker**: Redis (localhost:6379)
- **Workers**: 10 concurrent processes
- **Task limits**: 5 min soft, 10 min hard
- **Beat schedule**: Every 3 days at 2 AM

### Periodic Tasks
1. **Data Update**: Every 3 days at 2 AM
2. **File Cleanup**: Every Sunday at 3 AM

### File Storage
- **Location**: `media/documents/`
- **Naming**: UUID-based with original extensions
- **Database**: `file_path` field tracks local storage

## Monitoring

### Admin Panel
- Check `Periodic Tasks` section for scheduled tasks
- Monitor `Document` model for file download status
- View file paths and download links

### Logs
- Celery worker logs show task execution
- Beat scheduler logs show task scheduling
- Django logs show database operations

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   ```bash
   # Check if Redis is running
   redis-cli ping
   # Should return PONG
   ```

2. **Worker Not Processing Tasks**
   ```bash
   # Check worker status
   celery -A core_project inspect active
   ```

3. **Beat Not Scheduling**
   ```bash
   # Check beat status
   celery -A core_project inspect scheduled
   ```

### Performance Tuning
- Adjust `--concurrency` based on your system
- Modify task timeouts in `celery.py`
- Tune Redis memory settings if needed

## API Endpoints

### Manual Task Execution
```python
from products.tasks import update_parsed_data_periodic, cleanup_old_files

# Run tasks manually
update_parsed_data_periodic.delay()
cleanup_old_files.delay()
```

### Task Status
```python
from celery.result import AsyncResult

result = update_parsed_data_periodic.delay()
task_id = result.id

# Check status
status = AsyncResult(task_id).status
print(f"Task {task_id}: {status}")
```

## Security Notes
- Redis should be configured with authentication in production
- File downloads include timeout and retry mechanisms
- Admin panel includes permission checks for file operations
