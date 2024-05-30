import datetime
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ListManipulationViewSet  # Import your view




class TestListManipulationViewSet:

    #valid payload
    def test_list_view_success(self):
        factory = APIRequestFactory()
        view = ListManipulationViewSet.as_view({'post': 'list'})

        payload = {"batchid": "id0101", "payload": [[1, 2], [3, 4]]}
        request = factory.post('/sumList/', data=payload, format='json')

        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert "response" in response.data
        assert response.data["response"]["response"] == [3,7]
        
    #invalid payload
    def test_list_view_invalid_payload(self):
        factory = APIRequestFactory()
        view = ListManipulationViewSet.as_view({'post': 'list'})

        payload = {"batchid": "id0101", "payload": "invalid_payload"}
        request = factory.post('/sumList/', data=payload, format='json')

        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    #empty payload
    def test_list_action_empty_payload(self):
        factory = APIRequestFactory()
        view = ListManipulationViewSet.as_view({'post': 'list'})
        payload = {"batchid": "id0101", "payload": []}  # Empty payload
        request = factory.post('/sumList/', data=payload, format='json')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["response"]["response"] == []# Ensure results are empty
        


    #mocked exception
    @patch('innerApp.views.ListManipulationViewSet.process_list', side_effect=Exception("Mocked exception"))
    def test_list_action_exception_handling(self, mock_process_list):
        factory = APIRequestFactory()
        view = ListManipulationViewSet.as_view({'post': 'list'})
        payload = {"batchid": "id0101", "payload": [[1, 2], [3, 4]]}
        request = factory.post('/sumList/', data=payload, format='json')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["response"] == 'Mocked exception'    

    #inValid Key
    def test_list_action_invalid_payload_format(self):
        factory = APIRequestFactory()
        view = ListManipulationViewSet.as_view({'post': 'list'})
        payload = {"batchid": "id0101", "invalid_payload_key": [[1, 2], [3, 4]]}  # Invalid payload key
        request = factory.post('/sumList/', data=payload, format='json')
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["response"] == "'Not a Valid Key'" # Ensure results are empty
        assert response.data["error"]["batchid"] == None       