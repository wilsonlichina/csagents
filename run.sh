#!/bin/bash

# LCSC邮件客服系统启动脚本

echo "🚀 启动LCSC邮件客服智能体系统..."

# 检查Python版本 - 修复macOS兼容性
python_version=$(python3 --version 2>&1 | sed 's/Python //' | cut -d. -f1,2)
required_version="3.10"

# 简单的版本比较
if [ "$(echo "$python_version 3.10" | tr " " "\n" | sort -V | head -n1)" != "3.10" ]; then
    echo "❌ 需要Python 3.10+，当前版本: $python_version"
    echo "请升级Python版本或使用正确的Python环境"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  建议在虚拟环境中运行"
    echo "创建虚拟环境: python3 -m venv .venv"
    echo "激活虚拟环境: source .venv/bin/activate"
fi

# 安装依赖
echo "📦 检查并安装依赖..."
pip install -r requirements.txt

# 检查邮件目录
if [ ! -d "./emails" ]; then
    echo "⚠️  邮件目录不存在，创建示例目录..."
    mkdir -p emails
fi

# 加载环境变量
if [ -f "config.env" ]; then
    echo "📋 加载环境配置..."
    export $(cat config.env | grep -v '^#' | xargs)
else
    echo "⚠️  未找到config.env文件，使用默认配置"
    echo "请复制config.env.example为config.env并配置AWS凭证"
fi

# 检查AWS配置
if [ -z "$AWS_ACCESS_KEY_ID" ] && [ ! -f "$HOME/.aws/credentials" ]; then
    echo "⚠️  未检测到AWS凭证配置"
    echo "请配置AWS凭证以使用Amazon Bedrock:"
    echo "1. 设置环境变量 AWS_ACCESS_KEY_ID 和 AWS_SECRET_ACCESS_KEY"
    echo "2. 或运行 aws configure 配置凭证文件"
fi

# 检查并杀掉占用端口的进程
PORT=7860
echo "🔍 检查端口 $PORT 是否被占用..."

# 查找占用端口的进程
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
    echo "⚠️  发现端口 $PORT 被进程 $PID 占用"
    echo "🔪 正在终止占用端口的进程..."
    
    # 尝试优雅终止
    kill $PID 2>/dev/null
    sleep 2
    
    # 检查进程是否还在运行
    if kill -0 $PID 2>/dev/null; then
        echo "🔨 强制终止进程..."
        kill -9 $PID 2>/dev/null
        sleep 1
    fi
    
    # 再次检查端口是否释放
    NEW_PID=$(lsof -ti:$PORT)
    if [ -z "$NEW_PID" ]; then
        echo "✅ 端口 $PORT 已释放"
    else
        echo "❌ 无法释放端口 $PORT，请手动处理"
        echo "手动命令: sudo lsof -ti:$PORT | xargs kill -9"
        exit 1
    fi
else
    echo "✅ 端口 $PORT 可用"
fi

# 启动应用
echo "🌟 启动Gradio应用..."
python3 main.py
