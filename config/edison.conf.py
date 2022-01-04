[program:edison]
command=/home/second/venv/bin/gunicorn edison.wsgi:application -c /home/second/edison/config/gunicorn.conf.py
directory=/home/second/edison
user=second
autorestart=true
redirect_stderr=true
stdout_logfile = /home/second/edison/logs/debug.log