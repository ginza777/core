#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Docker environment for Core Project (Multi Parser)${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p media/documents
mkdir -p staticfiles
mkdir -p monitoring/prometheus
mkdir -p monitoring/grafana/provisioning/dashboards
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p nginx/conf.d

echo -e "${GREEN}✅ Directories created${NC}"

# Create and apply migrations
echo -e "${BLUE}🗄️  Creating and applying database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

echo -e "${GREEN}✅ Database migrations applied${NC}"

# Collect static files
echo -e "${BLUE}📦 Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}✅ Static files collected${NC}"

# Build and start services
echo -e "${BLUE}🐳 Building and starting Docker services...${NC}"
docker-compose up --build -d

echo -e "${GREEN}✅ Docker services started${NC}"

# Wait for services to be ready
echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"
sleep 30

# Check service status
echo -e "${BLUE}🔍 Checking service status...${NC}"
docker-compose ps

# Display access information
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo -e "${BLUE}📱 Access your services at:${NC}"
echo -e "   🌐 Django Admin: http://localhost/admin/"
echo -e "   📊 Grafana: http://localhost:3000 (admin/admin123)"
echo -e "   📈 Prometheus: http://localhost:9090"
echo -e "   🗄️  PostgreSQL: localhost:5432"
echo -e "   🔴 Redis: localhost:6379"
echo -e "   📁 Nginx: http://localhost/"

echo -e "${YELLOW}💡 To stop services: docker-compose down${NC}"
echo -e "${YELLOW}💡 To view logs: docker-compose logs -f [service_name]${NC}"
echo -e "${YELLOW}💡 To restart services: docker-compose restart${NC}"

# Create superuser if needed
echo -e "${BLUE}👤 Do you want to create a superuser? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${BLUE}Creating superuser...${NC}"
    docker-compose exec web python manage.py createsuperuser
    echo -e "${GREEN}✅ Superuser created${NC}"
fi

echo -e "${GREEN}🎯 All done! Your Docker environment is ready.${NC}"
