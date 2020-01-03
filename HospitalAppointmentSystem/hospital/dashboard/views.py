from rest_framework.views import APIView
from appointment.models import Appointment
from patient.models import Patient
from doctor.models import Doctor
from django.db.models import Count
from hospitaldoctor.models import HospitalDoctor
from hospitalpatient.models import HospitalPatient
from hospital.models import Hospital
from doctor.serializer import GetAppointmentDoctorSerializer
from rest_framework.response import Response
from rest_framework import status
import datetime
from doctordepartment.models import DoctorDepartment
class DashboardAPI(APIView):

    def get(self, request, format=None):
        hospitalid = self.get_hospital_id(request.user)
        context={}
        context['message']="Dashboard Details"
        context['status']=True   
        data={}

        totalApp = Appointment.objects.all()
        totalApp = len(totalApp)
        data['total_app']   = totalApp
        
        totalPat = HospitalPatient.objects.filter(hospital=hospitalid).values_list('patient')
        totalPat = len(totalPat)
        data['total_pat']   = totalPat
        
        totalDoc = HospitalDoctor.objects.filter(hospital=hospitalid).values_list('doctor')
        totalDoc = len(totalDoc)
        avgPat = round(totalPat/totalDoc)
        data['avg_pat']     = avgPat
        
        today = datetime.date.today()
        first = today.replace(day=1)

        docobj  = Appointment.objects.filter(time__gte=first).values('hospital_doctor').annotate(total=Count('hospital_doctor')).order_by('-total')
        total_doc = docobj
        docobj = docobj.first()
        hpdoc   = HospitalDoctor.objects.filter(hospital_doctor_id=docobj['hospital_doctor']).values_list('doctor_id')
        doc     = Doctor.objects.filter(id=hpdoc[0][0]).first()
        ser     = GetAppointmentDoctorSerializer(doc, many=False)
        docobj.pop('hospital_doctor')
        docobj['doctor']=ser.data
        data['best_doc']=docobj
        
        d={}
        for doct in total_doc:
            dept = DoctorDepartment.objects.filter(hospital_doctor_id=doct['hospital_doctor']).values('dept','dept__department')
            if dept[0]['dept__department'] in d:
                d[dept[0]['dept__department']]+=doct['total']
            else:
                d[dept[0]['dept__department']]=doct['total']
        l =[]
        for key in d:
            d2 = {}
            d2[key]=d[key]
            l.append(d2)
        data['AdmByDiv'] = l
        context['data']=data
        return Response(context,status=status.HTTP_200_OK)

    def get_hospital_id(self, id):
        query = Hospital.objects.filter(User=id)
        hospital_id = query.values_list('id', flat=True)[0]
        return hospital_id

