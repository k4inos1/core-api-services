from django.conf import settings


def test_settings_loaded():
    assert settings.SECRET_KEY


def test_admin_endpoint_is_reachable(client):
    response = client.get("/admin/")
    assert response.status_code in (200, 302)
