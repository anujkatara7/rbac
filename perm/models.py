from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Article(models.Model):
    title = models.TextField()
    STATUS = (
        ('pending', 'Pending'),
        ('InProgress', 'InProgress'),
        ('approved', 'Approved')
    )
    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS, default='pending')

    class Meta:
        permissions = (
            ('can_view_odd_ids', 'can_view_odd_ids'),
            ('can_view_even_ids', 'can_view_even_ids'),
        )

    def __str__(self):
        return self.title


class User(User):
    phone = models.CharField(max_length=20, null=True, blank=True)


class SuperVisor(Group):
    sv = models.OneToOneField(to=User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=250)


class SecurityPersonal(Group):
    sp = models.OneToOneField(to=User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=250)
