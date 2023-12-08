from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.serializers import TaskValidatorSerializer
from task.validators import task_validators


class TaskValidatorAPIView(APIView):
    serializer_class = TaskValidatorSerializer

    # def get_serializer_class(self):
    #     if self.action == "post":
    #         return TaskValidatorSerializer

    def post(self, request):
        # serializing
        serializer = self.serializer_class(data=request.data)

        # validate serializer
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            list_tasks: list = data["json"]
            if not list_tasks:
                raise exceptions.ParseError("json is empty.")

            result = task_validators(list_tasks)

        except Exception:
            raise exceptions.ParseError("json is note valid.")

        return Response({"result": result}, status=status.HTTP_200_OK)
