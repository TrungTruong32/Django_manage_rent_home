# Manage Rent Home - Deployment Guide

Ứng dụng quản lý nhà trọ được xây dựng bằng Django.

## Deployment lên Render (Docker)

### Chuẩn bị

1. Push code lên GitHub repository
2. Tạo tài khoản trên [Render.com](https://render.com)

### Các file đã tạo sẵn

- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- `.dockerignore` - Files to exclude from Docker build
- `build.sh` - Build script (optional)
- `render.yaml` - Render configuration (optional)

### Cách deploy

#### Option 1: Deploy qua Render Dashboard (Recommended)

1. **Tạo Web Service mới:**
   - Đăng nhập vào Render
   - Click "New +" → "Web Service"
   - Connect GitHub repository của bạn
   - Chọn repository `manage_rent_home`

2. **Cấu hình:**
   - **Name:** `manage-rent-home` (hoặc tên bạn muốn)
   - **Environment:** `Docker`
   - **Region:** Singapore (hoặc gần Việt Nam nhất)
   - **Branch:** `main` (hoặc branch bạn muốn deploy)
   - **Dockerfile Path:** `./Dockerfile`

3. **Environment Variables (quan trọng!):**
   
   Thêm các biến môi trường sau:
   
   ```
   SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   ```

   **Tạo SECRET_KEY mới:**
   ```python
   # Chạy lệnh này trong Python:
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

4. **Plan:**
   - Chọn "Free" nếu test
   - Chọn "Starter" ($7/month) nếu production

5. **Click "Create Web Service"**

6. Render sẽ tự động:
   - Build Docker image
   - Run migrations
   - Collect static files
   - Deploy ứng dụng

#### Option 2: Deploy bằng render.yaml

1. Đẩy file `render.yaml` lên repository
2. Trong Render Dashboard:
   - Click "New +" → "Blueprint"
   - Connect repository
   - Render sẽ tự động đọc cấu hình từ `render.yaml`

### Sau khi deploy

1. **Tạo superuser:**
   
   Vào Render Dashboard → Shell tab, chạy:
   ```bash
   python manage.py createsuperuser
   ```

2. **Access ứng dụng:**
   - URL: `https://your-app-name.onrender.com`
   - Admin: `https://your-app-name.onrender.com/admin`

### Sử dụng PostgreSQL (Recommended cho production)

1. Tạo PostgreSQL database trên Render:
   - Dashboard → "New +" → "PostgreSQL"
   - Chọn plan (Free có 90 days limit)
   - Copy "Internal Database URL"

2. Thêm environment variable:
   ```
   DATABASE_URL=<paste-internal-database-url-here>
   ```

3. Redeploy để apply thay đổi

### Test local với Docker

```powershell
# Build image
docker build -t manage-rent-home .

# Run container
docker run -p 8000:8000 -e DEBUG=True manage-rent-home

# Access: http://localhost:8000
```

### Troubleshooting

**Lỗi static files không load:**
- Kiểm tra `STATIC_ROOT` và `STATIC_URL` trong settings.py
- Chạy `python manage.py collectstatic` trong build process

**Lỗi migrations:**
- Đảm bảo `build.sh` có `python manage.py migrate`
- Hoặc chạy manual trong Render Shell

**Lỗi SECRET_KEY:**
- Đảm bảo đã set environment variable `SECRET_KEY`
- Không dùng secret key mặc định trong production

**App crash:**
- Check logs trong Render Dashboard → "Logs" tab
- Kiểm tra `ALLOWED_HOSTS` đã có domain của Render

### Free tier limitations (Render)

- App sẽ sleep sau 15 phút không hoạt động
- Request đầu tiên sau khi sleep sẽ chậm (cold start ~30s)
- 750 giờ/tháng free (đủ cho 1 app chạy 24/7)

### Upgrade to production

Nếu muốn dùng production:

1. Upgrade plan lên Starter ($7/month) - không sleep
2. Dùng PostgreSQL thay vì SQLite
3. Set `DEBUG=False`
4. Thêm custom domain
5. Enable HTTPS (tự động trên Render)
6. Set up monitoring và backups

## Local Development

```powershell
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access: http://localhost:8000
```

## Tech Stack

- Django 5.2.7
- Python 3.10
- SQLite (dev) / PostgreSQL (production)
- Gunicorn (WSGI server)
- WhiteNoise (static files)
- Docker

## Cấu trúc project

```
manage_rent_home/
├── manage_rent_home/      # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── rent_record/           # App chính
│   ├── models.py          # RentRecord model
│   ├── views.py           # Views (home, add_record)
│   ├── admin.py           # Django admin customization
│   ├── forms.py           # RentRecordForm
│   └── templates/         # HTML templates
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── .dockerignore         # Docker ignore file
└── manage.py             # Django CLI
```

## Support

Nếu gặp vấn đề khi deploy, check:
1. Render logs
2. Environment variables
3. Database connection
4. Static files settings
