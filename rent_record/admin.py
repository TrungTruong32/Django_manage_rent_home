from django.contrib import admin
from django.utils.html import format_html
from .models import RentRecord


@admin.register(RentRecord)
class RentRecordAdmin(admin.ModelAdmin):
	"""Admin for RentRecord with helpful list display and read-only totals."""
	list_display = (
		'room_name', 'tenant_name', 'month', 'rent_price',
		'total_electric', 'water_fee', 'other_fee', 'total', 'created_at'
	)
	readonly_fields = ('rental_breakdown', 'total_electric', 'total', 'created_at')
	search_fields = ('room_name', 'tenant_name', 'month')
	list_filter = ('month', 'room_name')
	
	fieldsets = (
		('Thông tin cơ bản', {
			'fields': ('room_name', 'tenant_name', 'month')
		}),
		('Chi phí', {
			'fields': ('rent_price', 'old_electric', 'new_electric', 'electric_price', 
			          'water_fee', 'other_fee')
		}),
		('Tổng kết', {
			'fields': ('rental_breakdown', 'created_at'),
			'classes': ('wide',)
		}),
	)
	
	def rental_breakdown(self, obj):
		"""Display a formatted breakdown box with all rental details."""
		if not obj.pk:  # New object being added
			return "Nhập thông tin để xem chi tiết"
		
		try:
			# Calculate values
			old_elec = obj.old_electric or 0
			new_elec = obj.new_electric or 0
			elec_price = obj.electric_price or 4000
			elec_usage = new_elec - old_elec
			elec_total = elec_usage * elec_price
			
			rent = obj.rent_price or 0
			water = obj.water_fee or 0
			# internet = obj.internet_fee or 0
			other = obj.other_fee or 0
			grand_total = rent + elec_total + water + other
			
			# Format numbers with thousand separators
			def fmt(num):
				return f"{num:,}".replace(',', '.')
			
			# Build HTML box
			html = f"""
			<div style="
				background: #f8f9fa;
				border: 2px solid #007bff;
				border-radius: 8px;
				padding: 20px;
				max-width: 500px;
				font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
				box-shadow: 0 2px 4px rgba(0,0,0,0.1);
			">
				<h3 style="margin-top: 0; color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px;">
					Chi tiết thanh toán tháng {obj.month}
				</h3>
				<div style="line-height: 1.8; font-size: 14px;">
					<div style="margin-bottom: 8px;">
						<strong>Tiền trọ:</strong> {fmt(rent)}đ
					</div>
					<div style="margin-bottom: 8px;">
						<strong>Nước:</strong> {fmt(water)}đ
					</div>
					<div style="margin-bottom: 8px; padding: 10px; background: #e7f3ff; border-radius: 4px;">
						<strong>Điện:</strong> {new_elec} - {old_elec} = {elec_usage} số
						<br/>
						<span style="margin-left: 20px;">{elec_usage} × {fmt(elec_price)}đ = <strong>{fmt(elec_total)}đ</strong></span>
					</div>
					<div style="margin-bottom: 8px;">
						<strong>Khác:</strong> {fmt(other)}đ
					</div>
					<hr style="margin: 15px 0; border: none; border-top: 2px solid #dee2e6;"/>
					<div style="font-size: 16px; font-weight: bold; color: #28a745; padding: 10px; background: #d4edda; border-radius: 4px;">
						<strong>TỔNG CỘNG:</strong> 
						{fmt(rent)} + {fmt(water)} + {fmt(elec_total)} + {fmt(other)} = 
						<span style="font-size: 18px;">{fmt(grand_total)}đ</span>
					</div>
				</div>
			</div>
			"""
			return format_html(html)
		except Exception as e:
			return f"Không thể hiển thị chi tiết: {str(e)}"
	
	rental_breakdown.short_description = 'Chi tiết thanh toán'

	def total_electric(self, obj):
		# When adding a new object in the admin `obj` fields may be None.
		# Guard against None to avoid TypeError during form rendering.
		try:
			old = getattr(obj, 'old_electric', None)
			new = getattr(obj, 'new_electric', None)
			price = getattr(obj, 'electric_price', None)
			if old is None or new is None or price is None:
				return ''
			return (new - old) * price
		except Exception:
			return ''
	total_electric.short_description = 'Electric charge'

	def total(self, obj):
		try:
			# rely on model's total(), but guard for None values
			if getattr(obj, 'rent_price', None) is None:
				return ''
			# total_electric() may return a number or raise; use model method inside try
			return obj.total()
		except Exception:
			return ''
	total.short_description = 'Grand total'
