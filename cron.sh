cd /opt/app/genwiz && python apscheduler/scheduler.py &
gunicorn --bind 0.0.0.0 --workers 4 --threads 8 -k gthread --timeout 600 app:app