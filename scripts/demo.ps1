Write-Host "Starting CyberQuality demo server in a new PowerShell window..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'python main.py demo-server'
Start-Sleep -Seconds 2
Write-Host "Starting Streamlit dashboard..."
streamlit run app.py
