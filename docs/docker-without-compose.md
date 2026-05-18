# Docker Without Compose

The current server has Docker 18.09 but does not have Docker Compose.

That is enough for the first version. We will run two containers manually:

- backend container on port `8000`
- frontend container on port `5173`

## Build Backend

```bash
cd ~/sdg-policy-intelligence-agent/backend
docker build -t sdg-policy-backend .
```

## Run Backend

```bash
docker run -d \
  --name sdg-policy-backend \
  -p 8000:8000 \
  --restart unless-stopped \
  sdg-policy-backend
```

Check:

```bash
curl http://localhost:8000/health
```

Expected result:

```json
{"status":"ok"}
```

## Build Frontend

```bash
cd ~/sdg-policy-intelligence-agent/frontend
docker build -t sdg-policy-frontend .
```

## Run Frontend

```bash
docker run -d \
  --name sdg-policy-frontend \
  -p 5173:80 \
  --restart unless-stopped \
  sdg-policy-frontend
```

Open:

```text
http://SERVER_IP:5173
```

For this server:

```text
http://213.142.148.196:5173
```

## Stop Containers

```bash
docker stop sdg-policy-frontend sdg-policy-backend
```

## Remove Containers

```bash
docker rm sdg-policy-frontend sdg-policy-backend
```

