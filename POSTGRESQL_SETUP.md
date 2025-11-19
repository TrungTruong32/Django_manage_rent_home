# Setup PostgreSQL trên Render

## Bước 1: Tạo PostgreSQL Database

1. Vào Render Dashboard: https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Cấu hình:
   - **Name:** `manage-rent-home-db`
   - **Database:** `manage_rent_home`
   - **User:** `manage_rent_home_user` (tự động)
   - **Region:** Singapore
   - **Plan:** Free (90 days) hoặc Starter ($7/month - permanent)
4. Click "Create Database"

## Bước 2: Lấy Database URL

Sau khi database được tạo, copy **Internal Database URL**:
- Format: `postgresql://user:password@host:5432/database`

## Bước 3: Add Environment Variable vào Web Service

1. Vào Web Service của bạn (django-manage-rent-home)
2. Click "Environment" tab
3. Add variable:
   ```
   Key: DATABASE_URL
   Value: <paste Internal Database URL>
   ```
4. Click "Save Changes"

Render sẽ tự động redeploy và dùng PostgreSQL thay vì SQLite.

## Bước 4: Tạo lại superuser

Vì database mới, cần tạo superuser:

1. Vào Web Service → "Shell" tab
2. Chạy:
   ```bash
   python create_superuser.py
   ```

Hoặc tạo custom:
```bash
python manage.py createsuperuser
```

## Ưu điểm PostgreSQL:

✅ Dữ liệu không bị mất khi redeploy
✅ Performance tốt hơn cho production
✅ Backup tự động (trên paid plan)
✅ Scalable

## Lưu ý:

- Free PostgreSQL có hạn 90 ngày
- Starter plan ($7/month) không giới hạn thời gian
- Database và Web Service cần cùng region để tốc độ tốt
