import multiprocessing
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from datetime import datetime
logger = logging.getLogger(__name__)


class ListManipulationViewSet(viewsets.ViewSet):
    @staticmethod
    def sum_inner(sublist):
        print(sublist)
        return sum(sublist)

    def process_list(self, nested_list):
        with multiprocessing.Pool() as pool:
            results = pool.map(self.sum_inner, nested_list)
        return results

    @method_decorator(never_cache)
    def list(self, request):
        response = {}
        end_at = None
        started_at= None
        try:
            if 'payload' not in request.data:
                raise KeyError("Not a Valid Key")

            input_list = request.data.get("payload", [])
            logger.info(f"Input processed: {input_list}")
            if not isinstance(input_list, list):
                raise ValueError("Payload must be a list")
            started_at = datetime.now()
            results = self.process_list(input_list)
            end_at = datetime.now()

            response["batchid"] = request.data.get("batchid")
            response["response"] = results
            response["started_at"] = started_at
            response["end_at"] = end_at
            response["status"] = "complete"

            logger.info(f"Response processed: {response}")

            return Response({"response": response}, status=200)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            response["batchid"] = None
            response["response"] = str(e)
            response["started_at"] = started_at
            response["end_at"] = end_at
            response["status"] = "incomplete"
            return Response({"error": response}, status=400)
