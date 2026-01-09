# 阿里云部署指南 (Linux)

本指南假设您使用的是标准的 Linux 发行版（例如 Ubuntu 22.04 或 CentOS 7/8）。

## 1. 准备工作

通过 SSH 连接到您的服务器：
```bash
ssh root@your_server_ip
```

### 安装核心依赖
```bash
# 更新软件包列表
sudo apt update && sudo apt upgrade -y

# 安装 git, redis, nginx 和 python3-venv
sudo apt install -y git redis-server nginx python3-pip python3-venv
```

### 安装 Node.js (用于构建前端)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 2. 克隆代码仓库
```bash
cd /opt
git clone https://github.com/niushijin24/drink-heatmap.git
cd drink-heatmap
```

## 3. 后端部署

### 设置 Python 环境
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt 
# 或者如果还没有生成 requirements.txt，可以手动安装：
pip install fastapi uvicorn redis pydantic
```

### 创建 Systemd 服务
创建一个服务文件以保持后端持续运行：
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
执行完毕后会生成一个 `dist` 文件夹。

### 配置 Nginx
编辑默认配置文件：`sudo nano /etc/nginx/sites-available/default`

```nginx
server {
    listen 80;
    server_name your_domain_or_ip; # 替换为您的域名或 IP 地址

    # 前端静态文件
    location / {
        root /opt/drink-heatmap/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 代理 API 请求到后端
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 重启 Nginx
```bash
sudo systemctl restart nginx
```

## 5. 验证
在浏览器中访问 `http://your_server_ip`。您应该能看到应用正在运行！
