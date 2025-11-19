# Cấu hình Render Disk cho SQLite

## Nếu muốn dùng SQLite với persistent storage

### Bước 1: Update settings.py để dùng /data directory

Database sẽ được lưu ở `/data/db.sqlite3` (persistent disk của Render)

### Bước 2: Cấu hình Render Disk

1. Vào Web Service → "Settings" → scroll xuống "Disks"
2. Click "Add Disk"
3. Cấu hình:
   - **Name:** `data`
   - **Mount Path:** `/data`
   - **Size:** 1 GB (free tier) hoặc nhiều hơn
4. Save

### Bước 3: Update DATABASE setting

Environment variable cần thêm:
```
SQLITE_PATH=/data/db.sqlite3
```

### Lưu ý:

⚠️ **Disk trên Render Free tier:**
- Chỉ có trên Paid plans (từ $7/month)
- Free tier KHÔNG hỗ trợ persistent disk

⚠️ **Khuyến nghị:**
- Dùng PostgreSQL free tier (90 ngày)
- Hoặc upgrade lên Starter plan ($7/month) để dùng disk

## Tóm tắt:

| Option | Cost | Data Persistence | Recommended |
|--------|------|------------------|-------------|
| SQLite (no disk) | Free | ❌ Lost on redeploy | Development only |
| SQLite + Disk | $7/month | ✅ Persistent | Small apps |
| PostgreSQL Free | Free | ✅ 90 days | Testing |
| PostgreSQL Starter | $7/month | ✅ Permanent | Production |

**→ Khuyến nghị: Dùng PostgreSQL (miễn phí 90 ngày, sau đó $7/month)**
