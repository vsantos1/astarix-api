
# On production Enable this middleware
class DisableCacheMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store,no-cache, max-age=0'
        return response

    def process_request(self, request, spider):
        request.meta['dont_cache'] = True

    def process_response(self, request, response, spider):
        response.headers.pop('Cache-Control', None)
        return response

    def process_exception(self, request, exception, spider):
        return None