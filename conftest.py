import os

# Allow synchronous database operations in threads with running event loops (required for Playwright + Django E2E tests)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
