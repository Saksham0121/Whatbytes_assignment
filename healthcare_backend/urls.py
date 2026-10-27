import os

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def openapi_schema_view(request):
    """Serves the raw OpenAPI 3.0.3 YAML specification."""
    schema_path = os.path.join(settings.BASE_DIR, "openapi.yaml")
    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HttpResponse(content, content_type="application/yaml")


def swagger_ui_view(request):
    """Interactive Swagger UI rendered in the browser."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Healthcare Backend API - Swagger UI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  <style>
    body { margin: 0; padding: 0; background: #fafafa; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .swagger-ui .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: '/api/schema/',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", openapi_schema_view, name="openapi-schema"),
    path("api/docs/", swagger_ui_view, name="swagger-ui"),
    path("api/auth/", include("authentication.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/mappings/", include("mappings.urls")),
]
