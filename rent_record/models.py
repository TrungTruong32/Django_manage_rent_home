from django.db import models

class RentRecord(models.Model):
    room_name = models.CharField(max_length=100)
    tenant_name = models.CharField(max_length=100)
    month = models.CharField(max_length=20)  # Ví dụ: "11/2025"

    rent_price = models.IntegerField(default=3000000)  # tiền thuê cố định

    old_electric = models.IntegerField()
    new_electric = models.IntegerField()
    electric_price = models.IntegerField(default=4000)

    water_fee = models.IntegerField(default=200000)
    # internet_fee = models.IntegerField(default=0)
    other_fee = models.IntegerField(default=65000)

    created_at = models.DateTimeField(auto_now_add=True)

    def total_electric(self):
        return (self.new_electric - self.old_electric) * self.electric_price

    def total(self):
        return self.rent_price + self.total_electric() + self.water_fee + self.other_fee

    def __str__(self):
        return f"{self.room_name} - {self.month}"
