from django.db import models
from globals.models import Logs
from hospitaldoctor.models import HospitalDoctor
from department.models import Department
# Create your models here.

class DoctorDepartment(Logs):

    doctor_dept_id      = models.AutoField(primary_key=True)
    hospital_doctor_id  = models.ForeignKey(HospitalDoctor, on_delete=models.CASCADE, related_name='DoctorDepartmentDoctorId')
    dept_id             = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='DoctorDepartmentDeptId')  