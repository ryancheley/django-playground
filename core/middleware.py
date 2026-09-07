class PageTitleRenamer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        print("Page Title Start")
        print(response.context_data)
        print("Page Title End")
        if response.context_data and response.context_data.get("title"):
            print("Page Title Start")
            print(response.context_data["title"])
            print("Page Title End")
            response.context_data["title"] = f"{response.context_data['title']} - 💩"
        return response
