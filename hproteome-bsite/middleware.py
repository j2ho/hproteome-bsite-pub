from django.http import HttpRequest


class AddHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        if "text/html" in response.get("Content-Type", ""):
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "connect-src 'self' https: data:; "
                "img-src 'self' http://ligand-expo.rcsb.org https: data:; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://static.cloudflareinsights.com; "
                "style-src 'self' 'unsafe-inline'; "
                "child-src 'unsafe-inline'"
            )
        return response
