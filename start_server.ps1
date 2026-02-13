
Write-Host "正在啟動 Tibet Companion 伺服器..." -ForegroundColor Cyan
Write-Host "請在瀏覽器中開啟 http://localhost:8000" -ForegroundColor Green
python -m http.server 8000
