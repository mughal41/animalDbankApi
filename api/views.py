from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
import threading
from .functions import fetch_all_animal_details_with_threads, bulk_parse_data

# Create your views here.


class AnimalDetailsView(APIView):

    def get(self, request):
        try:
            data_list = fetch_all_animal_details_with_threads(request.query_params.get('page', 1))
            if data_list:
                return JsonResponse({
                    "status":"success",
                    "message":None,
                    'data': data_list,
                }, safe=False,  status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    "status":"error",
                    "message": "Something went wrong",
                    "data": None,
                },safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return JsonResponse({
                "status": "failed",
                "message": "Something went wrong...",
                "data": None
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)


class CreateAnimalView(APIView):

    def post(self, request):
        try:
            payload = request.data.get('data')
            resp = bulk_parse_data(payload)
            if resp:
                return JsonResponse(
                {
                    "status":"success",
                    "message":None,
                    'data': "submission successful",
                },
                safe=False,
                status=status.HTTP_200_OK
                )
            return JsonResponse({
                "status": "success",
                "message": None,
                'data': "data_list",
            }, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return JsonResponse({
                "status": "failed",
                "message": "Something went wrong...",
                "data": None
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)

