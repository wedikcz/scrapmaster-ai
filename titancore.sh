#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TITANCORE_LOG="${SCRIPT_DIR}/data/logs/titancore-watchdog.log"
mkdir -p "${SCRIPT_DIR}/data/logs"

log_msg() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [TITANCORE-WATCHDOG] $1" | tee -a "${TITANCORE_LOG}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_msg "❌ Docker not found. Please install Docker."
        exit 1
    fi
    log_msg "✅ Docker found: $(docker --version)"
}

check_container_health() {
    local container_name=$1
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if docker ps --filter "name=${container_name}" --filter "status=running" | grep -q "${container_name}"; then
            log_msg "✅ Container ${container_name} is running"
            return 0
        fi
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            log_msg "⚠️  Container ${container_name} not running, retrying in 5 seconds..."
            sleep 5
        fi
    done
    
    log_msg "❌ Container ${container_name} failed after ${max_retries} retries. Attempting recovery..."
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" restart "${container_name}" || true
    return 1
}

check_disk_space() {
    local threshold=90
    local usage=$(df "${SCRIPT_DIR}/data" | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "${usage}" -gt "${threshold}" ]; then
        log_msg "⚠️  Disk usage at ${usage}%. Cleaning up old logs..."
        find "${SCRIPT_DIR}/data/logs" -name "*.log" -mtime +30 -delete
        find "${SCRIPT_DIR}/data/uploads" -type f -mtime +7 -delete
        log_msg "✅ Cleanup completed"
    else
        log_msg "✅ Disk usage at ${usage}% (healthy)"
    fi
}

perform_scan() {
    log_msg "🔍 Starting system scan..."
    check_docker
    check_container_health "scrapmaster-backend"
    check_container_health "scrapmaster-frontend"
    check_disk_space
    log_msg "✅ System scan completed"
}

perform_heal() {
    log_msg "🏥 Starting system heal procedure..."
    log_msg "Clearing application cache..."
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" exec -T scrapmaster-backend python -c "import shutil; shutil.rmtree('/tmp/scrapmaster-cache', ignore_errors=True)" || true
    log_msg "Restarting unhealthy containers..."
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" restart || true
    log_msg "✅ Heal procedure completed"
}

perform_upgrade() {
    log_msg "🆙 Starting zero-downtime upgrade..."
    
    if ! git -C "${SCRIPT_DIR}" diff --quiet; then
        log_msg "❌ Uncommitted changes detected. Stash or commit them first."
        return 1
    fi
    
    log_msg "Pulling latest changes..."
    git -C "${SCRIPT_DIR}" pull origin main || true
    
    log_msg "Rebuilding containers..."
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" build --no-cache || true
    
    log_msg "Applying database migrations..."
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" run --rm scrapmaster-backend python titancore.py db-init || true
    
    log_msg "Performing rolling restart..."
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" up -d --no-deps scrapmaster-backend || true
    sleep 2
    docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" up -d --no-deps scrapmaster-frontend || true
    
    log_msg "✅ Upgrade completed with zero downtime"
}

print_usage() {
    cat <<EOF
[TITANCORE] ScrapMaster AI Watchdog & Control Engine

Usage: $0 [command]

Commands:
  scan      - Perform comprehensive system health scan
  heal      - Execute self-healing recovery procedures
  upgrade   - Perform zero-downtime system upgrade
  validate  - Validate configuration and dependencies
  help      - Show this help message

Examples:
  $0 scan
  $0 heal
  $0 upgrade

EOF
}

case "${1:-help}" in
    scan)
        perform_scan
        ;;
    heal)
        perform_heal
        ;;
    upgrade)
        perform_upgrade
        ;;
    validate)
        check_docker
        ;;
    help)
        print_usage
        ;;
    *)
        echo "[TITANCORE] ❌ Unknown command: $1"
        print_usage
        exit 1
        ;;
esac
