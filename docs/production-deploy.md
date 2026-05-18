# Production Deploy On Ubuntu 22.04

This guide runs the project permanently on the server.

## Target

- Backend: FastAPI service on port `8000`
- Frontend: static production build served by nginx on port `80`

## 1. Backend systemd service

Stop the development backend first with `CTRL + C`, then create the service:

```bash
cat >/etc/systemd/system/sdg-policy-backend.service <<'EOF'
[Unit]
Description=SDG Policy Intelligence Agent Backend
After=network.target

[Service]
WorkingDirectory=/root/sdg-policy-intelligence-agent/backend
ExecStart=/root/sdg-policy-intelligence-agent/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start:

```bash
systemctl daemon-reload
systemctl enable sdg-policy-backend
systemctl start sdg-policy-backend
systemctl status sdg-policy-backend --no-pager
```

Check:

```bash
curl http://localhost:8000/health
```

## 2. Frontend production build

```bash
cd /root/sdg-policy-intelligence-agent/frontend
npm run build
apt install -y nginx
rm -rf /var/www/html/*
cp -r dist/* /var/www/html/
systemctl enable nginx
systemctl restart nginx
```

Open:

```text
http://213.142.148.196
```

## Useful checks

Backend logs:

```bash
journalctl -u sdg-policy-backend -n 80 --no-pager
```

Nginx status:

```bash
systemctl status nginx --no-pager
```

Restart backend:

```bash
systemctl restart sdg-policy-backend
```

