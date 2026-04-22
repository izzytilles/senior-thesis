#!/bin/bash
echo "=== startup.sh: wwwroot contents ==="
ls -la /home/site/wwwroot/
echo "===================================="

if [ -f /home/site/wwwroot/app/app.py ]; then
    gunicorn --bind=0.0.0.0:8000 --timeout 600 --chdir /home/site/wwwroot/app app:app
elif [ -f /home/site/wwwroot/app.py ]; then
    gunicorn --bind=0.0.0.0:8000 --timeout 600 --chdir /home/site/wwwroot app:app
else
    echo "ERROR: app.py not found in expected locations"
    find /home/site/wwwroot -name "app.py" 2>/dev/null
    exit 1
fi
