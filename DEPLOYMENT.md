# Alibaba Cloud Deployment Guide (Linux)

This guide assumes you are using a standard Linux distribution (e.g., Ubuntu 22.04 or CentOS 7/8).

## 1. Prerequisites

Connect to your server via SSH:
```bash
ssh root@your_server_ip
```

### Install Core Dependencies
```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install git, redis, nginx, and python3-venv
sudo apt install -y git redis-server nginx python3-pip python3-venv
```

### Install Node.js (for building frontend)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 2. Clone Repository
```bash
cd /opt
git clone https://github.com/niushijin24/drink-heatmap.git
cd drink-heatmap
```

## 3. Backend Deployment

### Setup Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt 
# OR if you don't have requirements.txt generated yet:
pip install fastapi uvicorn redis pydantic
```

### Create Systemd Service
Create a service file to keep the backend running:
`sudo nano /etc/systemd/system/drink-backend.service`

```ini
[Unit]
Description=Drink Heatmap Backend
After=network.target

[Service]
User=root
WorkingDirectory=/opt/drink-heatmap
ExecStart=/opt/drink-heatmap/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Start Backend
```bash
sudo systemctl daemon-reload
sudo systemctl start drink-backend
sudo systemctl enable drink-backend
```

## 4. Frontend Deployment

### Build the Project
```bash
cd frontend
npm install
npm run build
```
This will create a `dist` folder.

### Configure Nginx
Edit default config: `sudo nano /etc/nginx/sites-available/default`

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    # Frontend Static Files
    location / {
        root /opt/drink-heatmap/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API Requests to Backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

## 5. Verification
Visit `http://your_server_ip` in your browser. You should see the application running!
