from rest_framework.views import APIView
import xlrd
from django.http import HttpResponse
from exportexcel import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser,MultiPartParser

class ExportExcelView(APIView):
    parser_classes=[FormParser,MultiPartParser]
    def post(self, request):
        try:
            excel_file = request.FILES.get('file')  # Use get() to provide a default value if the key is not found
            if not excel_file:
                return Response("No file found in the request.", status=status.HTTP_400_BAD_REQUEST)

            file_extension = excel_file.name.split('.')[-1].lower()
            
            # Check if the uploaded file is an Excel file
            if file_extension not in ['xls', 'xlsx']:
                return Response("Invalid file format. Only .xls and .xlsx are allowed.", status=status.HTTP_400_BAD_REQUEST)
            
            workbook = xlrd.open_workbook(file_contents=excel_file.read())
            worksheet = workbook.sheet_by_index(0)

            data = []
            headers = worksheet.row_values(0)

            # Validate if the headers are present
            if not all(headers):
                return Response("Headers are missing in the Excel file.", status=status.HTTP_400_BAD_REQUEST)

            for row_index in range(1, worksheet.nrows):
                row_data = worksheet.row_values(row_index)
                # Skip empty rows
                if not any(row_data):
                    continue
                data.append(dict(zip(headers, row_data)))

            serializer = serializers.ItemSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response("Loaded successfully.", status=status.HTTP_200_OK)

        except xlrd.XLRDError as e:
            return Response("Error processing the Excel file.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response("An error occurred during processing.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


