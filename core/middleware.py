class PageTitleRenamer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if response.context_data and response.context_data.get("title"):
            response.context_data["title"] = f"{response.context_data['title']} - 💩"
        return response
