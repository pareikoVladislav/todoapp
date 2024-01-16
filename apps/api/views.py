# from rest_framework.response import Response
# from rest_framework.request import Request
# from rest_framework import status
# from rest_framework.decorators import (
#     api_view
# )
#
# from apps.api.serializers import AllTasksSerializer
# from apps.todo.models import Task

#
# @api_view(['GET'])
# def task_list(request: Request):
#     tasks = Task.objects.all()
#
#     if tasks:
#         serializer = AllTasksSerializer(
#             instance=tasks,
#             many=True
#         )
#
#         return Response(
#             status=status.HTTP_200_OK,
#             data=serializer.data
#         )
#     return Response(
#         status=status.HTTP_204_NO_CONTENT,
#         data=[]
#     )
#
#
# @api_view(['POST'])
# def create_new_task(request: Request):
#     serializer = AllTasksSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#
#         return Response(
#             status=status.HTTP_201_CREATED,
#             data=serializer.data
#         )
#
#     return Response(
#         status=status.HTTP_400_BAD_REQUEST,
#         data=serializer.errors
#     )

# -----------------------------------------------------------------------------------------------

from rest_framework.views import (
    APIView,
    Request,
    Response
)
from rest_framework.generics import (
    RetrieveAPIView,
    get_object_or_404,
)

from rest_framework.viewsets import ModelViewSet

from rest_framework.serializers import ValidationError
from rest_framework import status

from apps.todo.models import Task, Status, Category
from apps.api.serializers import (
    AllTasksSerializer,
    StatusSerializer,
    CategorySerializer,
    TaskInfoSerializer
)


class TasksApiView(APIView):

    def get(self, request: Request):
        tasks = Task.objects.filter(
            creator=request.user.id
        )

        if tasks:
            serializer = AllTasksSerializer(
                instance=tasks,
                many=True
            )

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=[]
        )

    def post(self, request: Request):
        try:
            serializer = AllTasksSerializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        except ValidationError as error:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": str(error),
                    "detail": error.detail
                }
            )


class TaskDetailGenericView(RetrieveAPIView):
    serializer_class = TaskInfoSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")

        task = get_object_or_404(Task, id=task_id)

        return task


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
