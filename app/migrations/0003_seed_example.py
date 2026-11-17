from django.db import migrations


def add_example(apps, schema_editor):
    Project = apps.get_model("app", "Project")
    Technology = apps.get_model("app", "Technology")
    if Project.objects.exists():
        return
    p = Project.objects.create(
        name="shopping", slug="shopping",
        summary="A family shared shopping list.",
        description="A shared shopping list the whole family can add to and tick off from their phones.",
        url="https://shopping.venividiludi.com",
    )
    for name in ("Django", "Postgres"):
        t, _ = Technology.objects.get_or_create(slug=name.lower(), defaults={"name": name})
        p.technologies.add(t)


class Migration(migrations.Migration):
    dependencies = [("app", "0002_projects")]
    operations = [migrations.RunPython(add_example, migrations.RunPython.noop)]
