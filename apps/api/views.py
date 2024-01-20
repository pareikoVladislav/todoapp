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
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.viewsets import ModelViewSet

from rest_framework.serializers import ValidationError
from rest_framework import status

from apps.messages import SUBTASK_SUCCESS_CREATED_MESSAGE, SUBTASK_SUCCESS_DELETED_MESSAGE
from apps.todo.models import (
    Task,
    Status,
    Category,
    SubTask,
)
from apps.api.serializers import (
    AllTasksSerializer,
    StatusSerializer,
    CategorySerializer,
    TaskInfoSerializer,
    SubTaskSerializer
)


# class TasksApiView(APIView):
#
#     def get(self, request: Request):
#         tasks = Task.objects.filter(
#             creator=request.user.id
#         )
#
#         if tasks:
#             serializer = AllTasksSerializer(
#                 instance=tasks,
#                 many=True
#             )
#
#             return Response(
#                 status=status.HTTP_200_OK,
#                 data=serializer.data
#             )
#
#         return Response(
#             status=status.HTTP_204_NO_CONTENT,
#             data=[]
#         )
#
#     def post(self, request: Request):
#         try:
#             serializer = AllTasksSerializer(
#                 data=request.data
#             )
#
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#
#             return Response(
#                 status=status.HTTP_201_CREATED,
#                 data=serializer.data
#             )
#         except ValidationError as error:
#             return Response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 data={
#                     "error": str(error),
#                     "detail": error.detail
#                 }
#             )


class TasksListGenericView(ListCreateAPIView):
    serializer_class = TaskInfoSerializer

    def get_queryset(self):
        # список всех задач
        # для каждой задачи получить доп инфу о статусе и категории
        # для каждой задачи нужно будет получать список
        # всех доступных подзадач именно для этой задачи
        queryset = Task.objects.select_related(
            'category',
            'status'
        ).prefetch_related('subtasks')

        # фильтрация по:
        # status, category, [date_from, date_to], deadline

        # query_params -> 127.0.0.1:8000/api/tasks/?status=NEW&category=Work

        status = self.request.query_params.get("status")
        category = self.request.query_params.get("category")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        deadline = self.request.query_params.get("deadline")

        if status:
            queryset = queryset.filter(
                status__name=status
            )
        if category:
            queryset = queryset.filter(
                category__name=category
            )
        if date_from and date_to:
            queryset = queryset.filter(
                date_started__range=[date_from, date_to]
            )
        if deadline:
            queryset = queryset.filter(
                deadline=deadline
            )

        return queryset

    def get(self, request: Request, *args, **kwargs):
        filtered_data = self.get_queryset()

        if filtered_data.exists():
            serializer = self.serializer_class(
                instance=filtered_data,
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

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )


class TaskDetailGenericView(RetrieveAPIView):
    serializer_class = TaskInfoSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")

        task = get_object_or_404(Task, id=task_id)

        return task


class AllSubtasksGenericView(ListCreateAPIView):
    serializer_class = SubTaskSerializer

    def create_subtask(self, data):
        serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer

    def get_queryset(self):
        subtasks = SubTask.objects.filter(
            creator=self.request.user.id
        )

        return subtasks

    def get(self, request: Request, *args, **kwargs):
        subtasks = self.get_queryset()

        if not subtasks:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data=[]
            )

        serializer = self.serializer_class(subtasks, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def post(self, request: Request, *args, **kwargs):
        new_subtask = self.create_subtask(data=request.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=new_subtask.data
        )


class SubTaskInfoGenericView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskSerializer

    def update_subtask_info(self, instance):
        serializer = self.serializer_class(
            instance=instance,
            data=self.request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data

    def get_object(self):
        subtask_id = self.kwargs.get('subtask_id')
        subtask = get_object_or_404(
            SubTask,
            id=subtask_id
        )

        return subtask

    def get(self, request: Request, *args, **kwargs):
        subtask = self.get_object()

        serializer = self.serializer_class(instance=subtask)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        subtask = self.get_object()

        data = self.update_subtask_info(instance=subtask)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": SUBTASK_SUCCESS_CREATED_MESSAGE,
                "data": data
            }
        )

    def delete(self, request, *args, **kwargs):
        subtask = self.get_object()

        subtask.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=SUBTASK_SUCCESS_DELETED_MESSAGE
        )


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
