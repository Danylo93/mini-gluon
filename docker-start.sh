#!/bin/bash

# ===========================================
# Scaffold Forge Docker Startup Script
# ===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Docker is running
check_docker() {
    # Check if we're running in WSL or if wsl command is available
    if command_exists wsl; then
        # Running on Windows with WSL available
        if ! wsl docker info >/dev/null 2>&1; then
            print_error "Docker is not running in WSL. Please start Docker first."
            exit 1
        fi

        if ! wsl command -v docker-compose >/dev/null 2>&1; then
            print_error "Docker Compose is not installed in WSL. Please install Docker Compose first."
            exit 1
        fi
    elif command_exists docker; then
        # Running directly in WSL or Linux
        if ! docker info >/dev/null 2>&1; then
            print_error "Docker is not running. Please start Docker first."
            exit 1
        fi

        if ! command_exists docker-compose; then
            print_error "Docker Compose is not installed. Please install Docker Compose first."
            exit 1
        fi
    else
        print_error "Neither WSL nor Docker is available. Please install Docker or WSL first."
        exit 1
    fi
}

# Function to create .env file if it doesn't exist
setup_env() {
    if [ ! -f .env ]; then
        print_status "Creating .env file from docker.env.example..."
        cp docker.env.example .env
        print_warning "Please edit .env file with your configuration before running again."
        print_warning "Especially set your GITHUB_TOKEN!"
        exit 1
    fi
}

# Function to get docker command
get_docker_cmd() {
    if command_exists wsl; then
        echo "wsl docker"
    else
        echo "docker"
    fi
}

get_docker_compose_cmd() {
    if command_exists wsl; then
        echo "wsl docker-compose"
    else
        echo "docker-compose"
    fi
}

# Function to build and start services
start_services() {
    local mode=${1:-development}
    local compose_cmd=$(get_docker_compose_cmd)
    
    print_status "Starting Scaffold Forge in $mode mode..."
    
    case $mode in
        "development")
            print_status "Building and starting development environment..."
            $compose_cmd --env-file .env build
            $compose_cmd --env-file .env up -d mongodb backend frontend
            ;;
        "production")
            print_status "Building and starting production environment..."
            $compose_cmd --env-file .env build
            $compose_cmd --env-file .env --profile production up -d
            ;;
        "full")
            print_status "Building and starting all services..."
            $compose_cmd --env-file .env build
            $compose_cmd --env-file .env up -d
            ;;
        *)
            print_error "Invalid mode: $mode. Use 'development', 'production', or 'full'"
            exit 1
            ;;
    esac
}

# Function to show logs
show_logs() {
    local service=${1:-}
    local compose_cmd=$(get_docker_compose_cmd)
    
    if [ -n "$service" ]; then
        print_status "Showing logs for $service..."
        $compose_cmd logs -f "$service"
    else
        print_status "Showing logs for all services..."
        $compose_cmd logs -f
    fi
}

# Function to stop services
stop_services() {
    local compose_cmd=$(get_docker_compose_cmd)
    print_status "Stopping all services..."
    $compose_cmd down
    print_success "All services stopped."
}

# Function to clean up
cleanup() {
    local compose_cmd=$(get_docker_compose_cmd)
    local docker_cmd=$(get_docker_cmd)
    print_status "Cleaning up Docker resources..."
    $compose_cmd down -v --remove-orphans
    $docker_cmd system prune -f
    print_success "Cleanup completed."
}

# Function to show status
show_status() {
    local compose_cmd=$(get_docker_compose_cmd)
    print_status "Service status:"
    $compose_cmd ps
}

# Function to show help
show_help() {
    echo "Scaffold Forge Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  start [mode]     Start services (development|production|full)"
    echo "  stop             Stop all services"
    echo "  restart [mode]   Restart services"
    echo "  logs [service]   Show logs (optionally for specific service)"
    echo "  status           Show service status"
    echo "  cleanup          Stop services and clean up resources"
    echo "  help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start development"
    echo "  $0 start production"
    echo "  $0 logs backend"
    echo "  $0 status"
    echo ""
}

# Main script logic
main() {
    local command=${1:-help}
    
    case $command in
        "start")
            check_docker
            setup_env
            start_services "$2"
            print_success "Services started successfully!"
            print_status "Frontend: http://localhost:3000"
            print_status "Backend API: http://localhost:8000"
            print_status "MongoDB: localhost:27017"
            ;;
        "stop")
            check_docker
            stop_services
            ;;
        "restart")
            check_docker
            setup_env
            stop_services
            start_services "$2"
            print_success "Services restarted successfully!"
            ;;
        "logs")
            check_docker
            show_logs "$2"
            ;;
        "status")
            check_docker
            show_status
            ;;
        "cleanup")
            check_docker
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
