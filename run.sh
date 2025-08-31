#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Multi Parser Services...${NC}"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}⚠️  Port $1 is already in use${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Port $1 is available${NC}"
        return 0
    fi
}

# Function to check if a service is running
check_service() {
    if pgrep -f "$1" > /dev/null; then
        echo -e "${GREEN}✅ $2 is already running${NC}"
        return 0
    else
        echo -e "${YELLOW}❌ $2 is not running${NC}"
        return 1
    fi
}

# Function to start Elasticsearch
start_elasticsearch() {
    echo -e "${BLUE}🔍 Starting Elasticsearch...${NC}"
    
    if check_service "elasticsearch" "Elasticsearch"; then
        echo -e "${GREEN}Elasticsearch is already running${NC}"
        return 0
    fi
    
    # Check if Elasticsearch is installed
    if ! command -v elasticsearch &> /dev/null; then
        echo -e "${RED}❌ Elasticsearch is not installed. Please install it first.${NC}"
        echo -e "${YELLOW}💡 You can install Elasticsearch using:${NC}"
        echo -e "${YELLOW}   - Homebrew (macOS): brew install elasticsearch${NC}"
        echo -e "${YELLOW}   - Or download from: https://www.elastic.co/downloads/elasticsearch${NC}"
        return 1
    fi
    
    # Start Elasticsearch in background
    elasticsearch > /dev/null 2>&1 &
    ELASTICSEARCH_PID=$!
    
    # Wait for Elasticsearch to start
    echo -e "${YELLOW}⏳ Waiting for Elasticsearch to start...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:9200 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Elasticsearch started successfully on port 9200${NC}"
            echo $ELASTICSEARCH_PID > .elasticsearch.pid
            return 0
        fi
        sleep 2
        echo -n "."
    done
    
    echo -e "${RED}❌ Failed to start Elasticsearch${NC}"
    return 1
}

# Function to start Tika server
start_tika_server() {
    echo -e "${BLUE}📄 Starting Tika Server...${NC}"
    
    if check_service "tika-server" "Tika Server"; then
        echo -e "${GREEN}Tika Server is already running${NC}"
        return 0
    fi
    
    # Check if Tika JAR file exists
    if [ ! -f "tika-server-standard-2.6.0.jar" ]; then
        echo -e "${RED}❌ Tika server JAR file not found${NC}"
        echo -e "${YELLOW}💡 Please ensure tika-server-standard-2.6.0.jar is in the project root${NC}"
        return 1
    fi
    
    # Check if Java is installed
    if ! command -v java &> /dev/null; then
        echo -e "${RED}❌ Java is not installed. Please install Java 8 or higher.${NC}"
        return 1
    fi
    
    # Start Tika server in background
    java -jar tika-server-standard-2.6.0.jar > /dev/null 2>&1 &
    TIKA_PID=$!
    
    # Wait for Tika server to start
    echo -e "${YELLOW}⏳ Waiting for Tika Server to start...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:9998/tika > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Tika Server started successfully on port 9998${NC}"
            echo $TIKA_PID > .tika.pid
            return 0
        fi
        sleep 2
        echo -n "."
    done
    
    echo -e "${RED}❌ Failed to start Tika Server${NC}"
    return 1
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    
    # Stop Elasticsearch
    if [ -f ".elasticsearch.pid" ]; then
        ELASTICSEARCH_PID=$(cat .elasticsearch.pid)
        if kill $ELASTICSEARCH_PID 2>/dev/null; then
            echo -e "${GREEN}✅ Elasticsearch stopped${NC}"
        fi
        rm -f .elasticsearch.pid
    fi
    
    # Stop Tika Server
    if [ -f ".tika.pid" ]; then
        TIKA_PID=$(cat .tika.pid)
        if kill $TIKA_PID 2>/dev/null; then
            echo -e "${GREEN}✅ Tika Server stopped${NC}"
        fi
        rm -f .tika.pid
    fi
    
    # Kill any remaining processes
    pkill -f "elasticsearch" 2>/dev/null
    pkill -f "tika-server" 2>/dev/null
    
    echo -e "${GREEN}✅ All services stopped${NC}"
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    
    if check_service "elasticsearch" "Elasticsearch"; then
        echo -e "${GREEN}   🔍 Elasticsearch: Running on port 9200${NC}"
    else
        echo -e "${RED}   🔍 Elasticsearch: Not running${NC}"
    fi
    
    if check_service "tika-server" "Tika Server"; then
        echo -e "${GREEN}   📄 Tika Server: Running on port 9998${NC}"
    else
        echo -e "${RED}   📄 Tika Server: Not running${NC}"
    fi
    
    # Check ports
    echo -e "${BLUE}   🌐 Port Status:${NC}"
    check_port 9200
    check_port 9998
}

# Function to show help
show_help() {
    echo -e "${BLUE}Multi Parser Service Manager${NC}"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start Elasticsearch and Tika Server"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  status    Show service status"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start    # Start services"
    echo "  $0 stop     # Stop services"
    echo "  $0 status   # Check status"
}

# Main script logic
case "${1:-start}" in
    start)
        echo -e "${BLUE}🚀 Starting Multi Parser Services...${NC}"
        
        # Check ports
        check_port 9200
        check_port 9998
        
        # Start services
        if start_elasticsearch && start_tika_server; then
            echo -e "${GREEN}🎉 All services started successfully!${NC}"
            echo ""
            echo -e "${BLUE}📋 Service URLs:${NC}"
            echo -e "   🔍 Elasticsearch: http://localhost:9200"
            echo -e "   📄 Tika Server: http://localhost:9998"
            echo ""
            echo -e "${GREEN}✅ You can now run: python manage.py runserver${NC}"
        else
            echo -e "${RED}❌ Failed to start some services${NC}"
            exit 1
        fi
        ;;
    stop)
        stop_services
        ;;
    restart)
        echo -e "${BLUE}🔄 Restarting services...${NC}"
        stop_services
        sleep 2
        $0 start
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}💡 Tip: Use '$0 help' for more information${NC}"
