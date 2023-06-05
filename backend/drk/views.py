from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drk.authentication import ZitadelAuthentication, ZitadelLocalAuthentication


class SampleResource(ViewSet):
    authentication_classes = [ZitadelAuthentication]

    def list(self, request):
        return Response(request.user.user_info)


class SampleResourceLocalValidation(ViewSet):
    authentication_classes = [ZitadelLocalAuthentication]

    def list(self, request):
        return Response(request.user.user_info)
