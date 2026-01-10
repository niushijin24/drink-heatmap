# 阿里云部署指南 (Linux) - 使用 uv

推荐使用 `uv` 来管理 Python 环境，它可以自动安装所需的 Python 版本 (3.12)，无需手动编译。

## 1. 准备工作

### 安装 uv
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使 uv 生效 (或者重新登录)
source $HOME/.cargo/env
```

### 安装核心依赖 (Git, Redis, Nginx)
```bash
# 如果是 Ubuntu/Debian
sudo apt update
sudo apt install -y git redis-server nginx

# 如果是 CentOS/Alibaba Cloud Linux
sudo yum install -y git redis nginx
sudo systemctl start redis
sudo systemctl enable redis
```

### 安装 Node.js (构建前端)
```bash
# Ubuntu
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# CentOS
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs
```

## 2. 克隆代码仓库
```bash
cd /opt
git clone https://github.com/niushijin24/drink-heatmap.git
cd drink-heatmap
```

## 3. 后端部署

### 使用 uv 初始化环境
`uv` 会自动下载 `pyproject.toml` 中指定的 Python 3.12。

```bash
# 同步依赖 (会自动创建虚拟环境并安装 Python 3.12)
uv sync
```

### 创建 Systemd 服务
**注意**：`uv` 的虚拟环境通常在项目目录下的 `.venv` 中。

`sudo nano /etc/systemd/system/drink-backend.service`

```ini
[Unit]
Description=Drink Heatmap Backend
After=network.target

[Service]
User=root
WorkingDirectory=/opt/drink-heatmap
# 使用 uv run 来启动，或者直接指向虚拟环境中的 uvicorn
ExecStart=/opt/drink-heatmap/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
Environment="PATH=/root/.local/bin:/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```

### 启动后端
```bash
sudo systemctl daemon-reload
sudo systemctl start drink-backend
sudo systemctl enable drink-backend
```

## 4. 前端部署

### 构建项目
```bash
cd frontend
npm install
npm run build
```

### 配置 Nginx
`sudo nano /etc/nginx/sites-available/default` (Ubuntu) 或 `/etc/nginx/nginx.conf` (CentOS)

```nginx
server {
    listen 80;
    server_name _; 

    location / {
        root /opt/drink-heatmap/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 重启 Nginx
```bash
# Ubuntu
sudo systemctl restart nginx
# CentOS
sudo systemctl restart nginx
```
