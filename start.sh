#!/bin/bash

# Gems 统一启动脚本
# 支持多种启动模式：web、cli、api

set -e

# 默认模式
MODE="${1:-web}"
PORT="${2:-8089}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
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

# 显示使用说明
show_usage() {
    echo "Gems 投资分析助手 - 统一启动脚本"
    echo ""
    echo "使用方法:"
    echo "  $0 [模式] [端口]"
    echo ""
    echo "模式选项:"
    echo "  web     - 启动Web界面 (默认)"
    echo "  cli     - 启动命令行界面"
    echo "  api     - 启动API服务器"
    echo "  help    - 显示帮助信息"
    echo ""
    echo "端口选项:"
    echo "  端口号   - 指定端口 (默认: 8089)"
    echo ""
    echo "示例:"
    echo "  $0 web 8089      # 启动Web界面，端口8089"
    echo "  $0 cli           # 启动命令行界面"
    echo "  $0 api 8080      # 启动API服务器，端口8080"
}

# 检查依赖
check_dependencies() {
    print_info "检查依赖..."

    # 检查Python环境
    if ! command -v python &> /dev/null; then
        print_error "未找到Python命令"
        exit 1
    fi

    # 检查uv
    if ! command -v uv &> /dev/null; then
        print_warning "未找到uv命令，尝试使用pip"
        USE_PIP=true
    else
        USE_PIP=false
    fi

    print_success "依赖检查完成"
}

# 启动Web服务器
start_web() {
    print_info "启动Web服务器..."
    print_info "🌐 访问地址: http://localhost:${PORT}"
    print_info "📡 WebSocket: ws://localhost:${PORT}/ws"
    print_info "📚 API文档: http://localhost:${PORT}/docs"
    print_info "❤️  健康检查: http://localhost:${PORT}/health"
    echo ""

    if [ "$USE_PIP" = true ]; then
        python apps/servers/main.py
    else
        uv run python apps/servers/main.py
    fi
}

# 启动CLI
start_cli() {
    print_info "启动命令行界面..."
    echo ""

    if [ "$USE_PIP" = true ]; then
        python apps/cli/main.py
    else
        uv run python apps/cli/main.py
    fi
}

# 启动API服务器
start_api() {
    print_info "启动API服务器..."
    print_info "📡 API地址: http://localhost:${PORT}/api"
    print_info "📚 API文档: http://localhost:${PORT}/docs"
    print_info "❤️  健康检查: http://localhost:${PORT}/health"
    echo ""

    # API模式只启动REST API，不启动WebSocket
    export API_ONLY=true

    if [ "$USE_PIP" = true ]; then
        python apps/servers/main.py
    else
        uv run python apps/servers/main.py
    fi
}

# 主函数
main() {
    echo "🚀 Gems 投资分析助手"
    echo "=" | head -c 60 | tr ' ' '='
    echo ""

    # 检查参数
    if [ "$MODE" = "help" ] || [ "$MODE" = "-h" ] || [ "$MODE" = "--help" ]; then
        show_usage
        exit 0
    fi

    # 验证模式
    case "$MODE" in
        web|cli|api)
            ;;
        *)
            print_error "无效的模式: $MODE"
            show_usage
            exit 1
            ;;
    esac

    # 验证端口
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
        print_error "无效的端口号: $PORT"
        exit 1
    fi

    # 检查依赖
    check_dependencies

    # 根据模式启动
    case "$MODE" in
        web)
            print_success "正在启动Web界面模式..."
            start_web
            ;;
        cli)
            print_success "正在启动命令行模式..."
            start_cli
            ;;
        api)
            print_success "正在启动API服务模式..."
            start_api
            ;;
    esac
}

# 捕获中断信号
trap 'print_warning "收到中断信号，正在退出..."; exit 0' INT TERM

# 运行主函数
main "$@"}