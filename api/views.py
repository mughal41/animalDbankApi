from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
import threading
from .functions import fetch_all_animal_details_with_threads, bulk_parse_data
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class AnimalDetailsView(APIView):

    def get(self, request):
        try:
            logger.info(f"Fetching animal details for page {request.query_params.get('page', 1)}")

            data_list = fetch_all_animal_details_with_threads(int(request.query_params.get('page', 1)))
            logger.info(f"Successfully fetched {len(data_list)} records")
            if data_list:
                return JsonResponse({
                    "status":"success",
                    "message":None,
                    'data': data_list,
                }, safe=False,  status=status.HTTP_200_OK)
            else:
                logger.warning("Animal detail fetch returned empty or None")
                return JsonResponse({
                    "status":"failed",
                    "message": "Something went wrong",
                    "data": None,
                },safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Exception Raised in  AnimalDetailsView")
            return JsonResponse({
                "status": "failed",
                "message": "Something went wrong...",
                "data": None
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)


class CreateAnimalView(APIView):

    def post(self, request):
        try:
            payload = request.data.get('data')
            logger.info(f"Received payload with {len(payload) if payload else 0} items")
            resp = bulk_parse_data(payload)
            if resp:
                logger.info("Successfully submitted animal data")

                return JsonResponse(
                {
                    "status":"success",
                    "message":None,
                    'data': "submission successful",
                },
                safe=False,
                status=status.HTTP_200_OK
                )
            logger.error("bulk_parse_data returned False / check payload format")

            return JsonResponse({
                "status": "failed",
                "message": "Invalid payload format",
                'data': None,
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Exception Raised in CreateAnimalView")
            return JsonResponse({
                "status": "failed",
                "message": "Something went wrong...",
                "data": None
            }, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

