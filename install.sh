#!/bin/bash

set -e

if [ -d "venv" ]; then
    echo "✅ Virtual environment 'venv' already exists."
else
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🐍 Activating virtual environment..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "⚠️ 'requirements.txt' not found."
fi

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating .env from .env.example..."
        cp .env.example .env
    else
        echo "⚠️ Neither .env nor .env.example found — skipping .env creation."
    fi
else
    echo "✅ .env file already exists."
fi

if [ "$(uname)" == "Linux" ]; then
    echo "🕒 Changing system time to Kyiv time..."
    sudo timedatectl set-timezone Europe/Kyiv
else
    echo "⚠️ System time change is not supported on this OS."
fi