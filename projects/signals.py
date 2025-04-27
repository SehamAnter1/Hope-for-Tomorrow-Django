# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation, Project

@receiver(post_save, sender=Donation)
def update_project_progress(sender, instance, created, **kwargs):
    if created:
        project = instance.project
        project.donations_amount += instance.amount
        project.donations_count += 1
        project.update_progress()
        project.save()
