from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions
class HandleWithCustomExceptions():

    def __init__(self,status_code,message,detail):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        
    def handle_with_404_error(self):

        data ={}
        
        data['message'] = self.message
        data['status_code'] = self.status_code
        data['detail'] = self.detail

        return Response(data,status.HTTP_404_NOT_FOUND)


