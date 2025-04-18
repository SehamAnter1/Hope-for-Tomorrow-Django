
from projects.models import Project
def update_project_progress(sender, instance, **kwargs):
    project = instance.project
    project.update_progress()
    