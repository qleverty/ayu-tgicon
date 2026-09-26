taskkill /f /im explorer.exe
timeout /t 1 /nobreak
del /f /q "%localappdata%\Microsoft\Windows\Explorer\iconcache_*.db"
del /f /q "%localappdata%\IconCache.db"
start explorer.exe