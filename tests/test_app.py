import pytest
from django.contrib.auth import get_user_model

from app.auth import PlatformOIDCBackend
from app.models import Heartbeat


@pytest.mark.django_db
def test_health_and_home(client):
    assert client.get("/health").status_code == 200
    r = client.get("/")
    assert r.status_code == 200 and b"Sign in" not in r.content


@pytest.mark.django_db
def test_superadmin_maps_to_superuser_and_follows_the_group():
    b = PlatformOIDCBackend()
    claims = {"sub": "s1", "preferred_username": "owner", "email": "o@example.com", "groups": ["superadmin"]}
    u = b.create_user(claims)
    assert u.is_superuser and u.is_staff
    assert list(b.filter_users_by_claims(claims)) == [u]
    u = b.update_user(u, claims | {"groups": ["dev-access"]})
    assert not u.is_superuser and not u.is_staff


@pytest.mark.django_db
def test_existing_user_is_adopted_by_email():
    old = get_user_model().objects.create_user(username="legacy", email="friend@example.com")
    found = list(PlatformOIDCBackend().filter_users_by_claims({"sub": "s2", "email": "FRIEND@example.com"}))
    assert found == [old]


@pytest.mark.django_db
def test_jobs():
    from django.core.management import call_command
    call_command("seed")
    call_command("heartbeat")
    assert Heartbeat.objects.count() == 2


@pytest.mark.django_db
def test_the_description_is_escaped(client, tmp_path, monkeypatch):
    from app import context
    d = tmp_path / "description.txt"
    d.write_text("{{ evil }} {% load x %} <script>alert(1)</script>\n")
    monkeypatch.setattr(context, "_DESCRIPTION", d)
    body = client.get("/").content.decode()
    assert "&lt;script&gt;" in body and "<script>alert" not in body and "{{ evil }}" in body


@pytest.mark.django_db
def test_showcase_filter_and_detail(client):
    from app.models import Project, Technology
    assert Project.objects.filter(slug="shopping").exists()  # from the data migration
    htmx = Technology.objects.create(name="HTMX", slug="htmx")
    other = Project.objects.create(name="Other", slug="other", summary="x")
    other.technologies.add(htmx)
    Project.objects.create(name="Hidden", slug="hidden", summary="x", published=False)
    body = client.get("/").content.decode()
    assert "shopping" in body and "Other" in body and "Hidden" not in body
    body = client.get("/?tech=htmx").content.decode()
    assert "Other" in body and "A family shared shopping list" not in body
    assert client.get("/projects/shopping/").status_code == 200
    assert client.get("/projects/hidden/").status_code == 404
