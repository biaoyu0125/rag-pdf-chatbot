#!/bin/bash

echo "Starting Streamlit app..."
echo "Current directory:"
pwd
echo "Files:"
ls -la

echo "Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Starting Streamlit..."
python -m streamlit run app.py \
  --server.port=8000 \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --browser.gatherUsageStats=false
