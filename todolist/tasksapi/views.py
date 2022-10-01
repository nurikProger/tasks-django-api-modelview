from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Tasks
from .serializers import TasksSerializer
from datetime import datetime
from pytz import timezone
from django.utils.datastructures import MultiValueDictKeyError



class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    
    # Filter
    def filter(self, request):
        try:
            start_time = request.GET['start_date']
        except MultiValueDictKeyError:
            start_time = ""
            
        try:
            end_time = request.GET['end_date']
        except MultiValueDictKeyError:
            end_time = ""
        
        # No Parameters
        if len(start_time) == 0 and len(end_time) == 0:
            tasks = Tasks.objects.all()
            serializer = TasksSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        filtered = [] # list of suitable times
        tasks = Tasks.objects.all().values()

        # If Start_Time is given
        if len(start_time) != 0:

            # In Case Give Date does NOT MATCH the FORMAT
            try:
                # converting the str to datetime object and making it timezone aware
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                start_time = timezone("Asia/Tashkent").localize(start_time)

                # filtering tasks

                for task in tasks:
                    task_start_time = task['start_time']

                    if start_time <= task_start_time:
                        filtered.append(task)
                
                if len(filtered) == 0:
                    return Response({"res":"No suitable tasks for the given time period"},
                    status=status.HTTP_400_BAD_REQUEST)

            except ValueError:
                return Response(
                {"res":f"'{start_time}' does not match format YY-mm-dd HH:MM:SS"},
                status=status.HTTP_400_BAD_REQUEST)


        # If End_Time is given
        if len(end_time) != 0:


            # In Case Give Date does NOT MATCH the FORMAT
            try:
                end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                end_time = timezone("Asia/Tashkent").localize(end_time)

                # filtering tasks
                check_for = filtered
                temporary_filtered = []

                if len(filtered) == 0:
                    check_for = tasks

                
                for task in check_for:
                    task_end_time = task['end_time']

                    if end_time >= task_end_time:
                        temporary_filtered.append(task)
                
                filtered = temporary_filtered

                if len(filtered) == 0:
                    return Response({"res":"No suitable tasks for the given time period"},
                    status=status.HTTP_400_BAD_REQUEST)

            except ValueError:
                return Response(
                {"res":f"'{end_time}' does not match format YY-mm-dd HH:MM:SS"},
                status=status.HTTP_400_BAD_REQUEST)

        
        return Response(filtered)
    

    def todo(self, request):
        tasks = Tasks.objects.filter(status="todo")
        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def expired(self, request):
        current = timezone("Asia/Tashkent").localize(datetime.now())
        tasks = Tasks.objects.all().values()
        expired = []

        for task in tasks:
            end_time = task['end_time']

            if current > end_time:
                expired.append(task)

        return Response(expired, status=status.HTTP_200_OK)
    
    def in_progress(self, request):
        tasks = Tasks.objects.filter(status="in progress")
        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def done(self, request):
        tasks = Tasks.objects.filter(status="done")
        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)