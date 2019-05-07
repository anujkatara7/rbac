from django.db import models

# Create your models here.


class Employee(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    emp_name = models.CharField(max_length=30)
    salary = models.IntegerField()
    city = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return self.emp_name


class ContactUs(models.Model):
    full_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=75)
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_date = models.DateField(null=True, blank=True)
    deleted_by = models.PositiveIntegerField(default=0)

    class Meta:
        index_together = ["full_name", "is_deleted"]
        db_table = 'dev_contact_us'
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.full_name
