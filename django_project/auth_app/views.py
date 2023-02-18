from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer


class RegisterApi(APIView):
    """
    The class handles User request to register
    """
    def post(self, request, *args, **kwargs):
        """
        the function takes post request and proceeds for registration
        :param request: request data
        :return:  Response of status
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })
