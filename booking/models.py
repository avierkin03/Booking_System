from django.db import models
from django.conf import settings

# модель категорії
class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["title"]


# модель кімнати
class Room(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    location = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rooms')
    price = models.IntegerField()
    image = models.ImageField(upload_to='rooms', null=True)

    def __str__(self):
        return f"Room №{self.number} for {self.capacity} person(s)"
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["number"]


# модель бронювання
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateField()
    end_time = models.DateField()
    creation_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["start_time"]

