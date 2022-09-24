from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions
class HandleWithCustomExceptions(exceptions.ValidationError):

    def __init__(self,message):
     
        self.message = message
        
        
    def handle_with_404_error(self):

        data ={}
        
        data['message'] = self.message
        data['status_code'] = status.HTTP_404_NOT_FOUND
        data['detail'] = 'Não foi possível processar a requisição, não econtrado.'

        return Response(data,status.HTTP_404_NOT_FOUND)
    
    def handle_with_bad_request(self):
            
            data ={}
            
            data['message'] = self.message
            data['status_code'] = status.HTTP_400_BAD_REQUEST
            data['detail'] = 'Não foi possível processar a requisição'
    
            return Response(data,status.HTTP_400_BAD_REQUEST)


