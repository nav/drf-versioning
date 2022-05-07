from rest_framework import renderers


class JSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get("request")
        response = {
            "data": data,
            "metadata": {
                "api_version": request.api_version.name,
                "deprecations": [],
                "removals": [],
            },
        }
        return super(JSONRenderer, self).render(
            response, accepted_media_type=None, renderer_context=None
        )
