#!/usr/bin/env bash
set -euo pipefail
python main.py demo-server > /tmp/cyberquality-demo.log 2>&1 &
DEMO_PID=$!
trap 'kill $DEMO_PID 2>/dev/null || true' EXIT
sleep 2
streamlit run app.py
