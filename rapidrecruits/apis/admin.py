from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ApplicantInfoModel)
admin.site.register(models.CollegeInfoModel)
admin.site.register(models.EmployeeInfoModel)
admin.site.register(models.VacanciesInfoModel)
admin.site.register(models.RecruitmentCommitteeInfoModel)
admin.site.register(models.ApplicantQualificationModel)
admin.site.register(models.ApplicantExperienceModel)
admin.site.register(models.VacancyApplicantMapping)