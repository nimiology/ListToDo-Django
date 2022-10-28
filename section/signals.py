def section_pre_save(sender, instance, *args, **kwargs):
    if instance.position is None:
        project_sections = sender.objects.filter(project=instance.project).order_by('-position')
        if project_sections.exists():
            project_section = project_sections[0]
            instance.position = project_section.position + 1
        else:
            instance.position = 0
