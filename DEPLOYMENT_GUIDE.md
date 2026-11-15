# PRODUCTION DEPLOYMENT GUIDE
## DevLog Blogging Platform with Flask

This guide details the step-by-step procedures to deploy the **DevLog** blogging platform to staging and production environments using **Docker** and **Gunicorn**.

---

## 1. System Requirements

- **Operating System:** Linux (Ubuntu 22.04 LTS recommended) or Docker Host
- **Runtime:** Python 3.11+
- **Database:** SQLite (default) or PostgreSQL 14+
- **Reverse Proxy:** Nginx
- **Process Manager / WSGI:** Gunicorn
- **SSL / TLS:** Let's Encrypt (Certbot)

---

## 2. Docker Deployment (Recommended)

Docker provides the simplest and most reproducible deployment workflow.

### Step 1: Clone Repository & Enter Directory
```bash
git clone https://github.com/chavanshraddha-blip/my-first-repo.git
cd Blogging-Platform-Flask
```

### Step 2: Configure Environment Variables
Create a production `.env` file:
```bash
cp .env.example .env
```
Edit `.env` with strong secrets:
```ini
SECRET_KEY=generate-a-strong-random-64-character-hex-secret
DATABASE_URL=sqlite:///instance/blog.db
FLASK_CONFIG=production
PORT=5000
```

### Step 3: Build the Docker Image
```bash
docker build -t devlog-flask-app:latest .
```

### Step 4: Run the Docker Container
Run the container with a persistent volume for the SQLite database instance directory:
```bash
docker run -d \
  --name devlog-app \
  -p 5000:5000 \
  -v $(pwd)/instance:/app/instance \
  --restart unless-stopped \
  --env-file .env \
  devlog-flask-app:latest
```

### Step 5: Verify Container Health
```bash
# Check container status
docker ps

# Check application logs
docker logs -f devlog-app

# Probe health endpoint
curl -I http://localhost:5000/
```

---

## 3. Direct Host Deployment with Gunicorn & Nginx

If deploying directly to a Linux Virtual Private Server (VPS) such as AWS EC2, DigitalOcean, or Linode:

### Step 1: Install System Packages
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv nginx curl git
```

### Step 2: Clone and Configure Virtual Environment
```bash
cd /var/www
sudo git clone https://github.com/chavanshraddha-blip/my-first-repo.git devlog
cd devlog
sudo chown -R $USER:$USER /var/www/devlog

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
flask init-db
```

### Step 4: Configure Systemd Service
Create a systemd service file `/etc/systemd/system/devlog.service`:
```ini
[Unit]
Description=Gunicorn instance to serve DevLog Flask application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/devlog
Environment="PATH=/var/www/devlog/venv/bin"
EnvironmentFile=/var/www/devlog/.env
ExecStart=/var/www/devlog/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 --access-logfile /var/log/gunicorn-access.log --error-logfile /var/log/gunicorn-error.log "run:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start devlog
sudo systemctl enable devlog
sudo systemctl status devlog
```

### Step 5: Configure Nginx as Reverse Proxy
Create `/etc/nginx/sites-available/devlog`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 16M;

    location /static {
        alias /var/www/devlog/app/static;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/devlog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL Security with Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 4. Production Checklist

- [x] Set a unique, cryptographically random `SECRET_KEY`.
- [x] Ensure `DEBUG = False` in production configuration.
- [x] Restrict database folder permissions (`chmod 700 instance/`).
- [x] Ensure all static assets are served efficiently with proper cache headers.
- [x] Configure automatic log rotation for Gunicorn access and error logs.
- [x] Verify automated backups for the database file (`instance/blog.db`).
