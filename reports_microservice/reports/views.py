from rest_framework import viewsets
from .models import Reserva
from .serializers import ReservaSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import openpyxl
from reportlab.pdfgen import canvas
from datetime import datetime

# CRUD de reservas
class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

# Reporte en Excel
class ReporteExcelView(APIView):
    def get(self, request):
        reservas = Reserva.objects.all()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reservas"
        ws.append(["ID", "Usuario", "Estado", "Fecha"])

        for r in reservas:
            ws.append([r.id, r.usuario, r.estado, str(r.fecha)])

        # Nombre con timestamp para evitar conflictos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_reservas_{timestamp}.xlsx"

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

# Reporte en PDF
class ReportePDFView(APIView):
    def get(self, request):
        reservas = Reserva.objects.all()
        
        # Nombre con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_reservas_{timestamp}.pdf"

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Reporte de Reservas - {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        y = 760
        for r in reservas:
            # Control de página para evitar que se salga del PDF
            if y < 50:
                p.showPage()
                y = 800
                
            p.drawString(100, y, f"ID: {r.id}, Usuario: {r.usuario}, Estado: {r.estado}, Fecha: {r.fecha}")
            y -= 20

        p.showPage()
        p.save()
        return response
