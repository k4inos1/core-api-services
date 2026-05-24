from playwright.sync_api import Page


def test_ai_agent_sandbox_connection(page: Page, live_server):
    """
    Playwright Sandbox Test for AI Agents.
    This ensures that any AI tool or script can safely navigate the application.
    """
    # The API might just return JSON, but this validates that the server is up
    # and that the Playwright sandbox is correctly configured.
    response = page.request.get(f"{live_server.url}/admin/")
    assert response.status == 200

    # An AI agent could then interact with the DOM, scrape API responses, etc.
    # page.goto(f"{base_url}/api/v1/auth/login/")
    # ...
