from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# local imports 
from api import serializers
from api import models
from api.utils import model_utils

# call automatic Jira agent  
class JiraAgentApiView(APIView):
    request_serializer_class = serializers.ModelRequestSerializer
    response_serializer_class = serializers.ModelResponseSerializer

    def post(self, request):
        """Query the Jira agent"""

        if  (serializer := self.request_serializer_class(data=request.data)) and \
            serializer.is_valid():
            
            request = serializer.validated_data.get('request')
            
            try:
                response = model_utils.agent.invoke({"input": request})
                if output := response.get('output'):
                    
                    serializer = self.response_serializer_class(data={"response": output})
                    if serializer.is_valid():
                        response = self.response_serializer_class(data={"response": response})
                        modelRequest = models.ModelRequest(request=request, response=response)
                        modelRequest.save()
                        return Response({'output': output})
            except Exception as e:
                print(f'ERROR JiraAgentApiView: {e}')
            
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
class HealthCheck(APIView):
    def get(self, request):
        """Healthcheck endpoint"""
        return Response({'message': 'OK'})
    
class GetRecords(APIView):
    def get(self, request):
        """Get request records endpoint"""
        data = models.ModelRequest.objects.all().values()
        return Response({'result': str(data)})