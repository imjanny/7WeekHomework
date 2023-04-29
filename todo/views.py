from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from todo.models import Todo
from todo.serializers import TodoSerializer, TodoCreateSerializer


class ToDoView(APIView):
    def get(self, request):
        todolists = Todo.objects.all()
        serializer = TodoSerializer(todolists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoDetailView(APIView):
    def get(self, request, todo_id):
        todolists = get_object_or_404(Todo, id=todo_id)
        serializer = TodoSerializer(todolists)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, todo_id):
        todolists = get_object_or_404(Todo, id=todo_id)
        if request.user == todolists.user:
            serializer = TodoCreateSerializer(todolists, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id):
        todolists = Todo.objects.get(id=todo_id)
        if request.user == todolists.user:
            todolists.delete()
            return Response("삭제됐습니다", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403)
