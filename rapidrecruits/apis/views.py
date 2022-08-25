from unicodedata import name
from django.shortcuts import render

from apis.models import ApplicantExperienceModel, ApplicantInfoModel, ApplicantQualificationModel, CollegeInfoModel, EmployeeInfoModel, VacanciesInfoModel, VacancyApplicantMapping, RecruitmentCommitteeInfoModel

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
import openpyxl
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from datetime import *
# Create your views here.

class ApplicantAPIView(APIView):
    # Method to fetch the details of an applicant using username.
    def get(self, request, username, format = None):
        user = User.objects.get(username = username)
        temp_result = {}
        temp_result["username"] = user.username
        temp_result["email"] = user.email
        if (ApplicantInfoModel.objects.filter(user = user).exists()):
            applicant = ApplicantInfoModel.objects.get(user = user)
            temp_result["profile_pic"] = applicant.profile_pic
            temp_result["description"] = applicant.description
            temp_result["full_name"] = applicant.full_name
            temp_result["DOB"] = applicant.DOB
            temp_result["gender"] = applicant.gender
            temp_result["address"] = applicant.address
            temp_result["state"] = applicant.state
            temp_result["pincode"] = applicant.pincode
            temp_result["category"] = applicant.category
            temp_result["marital_status"] = applicant.marital_status
            temp_result["phone_number"] = applicant.phone_number
            temp_result["total_experience"] = applicant.total_experience
            temp_result["skillset"] = applicant.skillset.names()
            temp_result["resume"] = applicant.resume
            return Response(temp_result, status = 200)
        else:
            return Response({"user" : temp_result, "mssg" : "Applicant profile not updated!"}, status = 403)

    # Posting the data of the applicant and user signup and login api.
    def post(self, request, format = None):
        if (request.data["purpose"] == "signup"):
            username = request.data["username"]
            if (User.objects.filter(username = username).exists()):
                return Response({"mssg" : "username already exists!"}, status = 409)
            email = request.data["email"]
            if (User.objects.filter(email = email).exists()):
                return Response({"mssg" : "email already exists!"}, status = 409)
            password = request.data["password"]
            confirm_password = request.data["confirm_password"]
            if (password == confirm_password):
                user = User.objects.create(username = username, email = email, password = password)
                user.set_password(user.password)
                user.save()
                login(request, user)
                return Response({"mssg": "user signed up successfully!"}, status = 200)
            else:
                return Response({"mssg": "passwords do not match!"}, status = 409)
        elif (request.data["purpose"] == "login"):
            if (authenticate(username = request.data["username"], password = request.data["password"])):
                return Response({"mssg": "user logedin successfully!"}, status = 200)
            else:
                return Response({"mssg": "login failed!"}, status = 404)
        elif (request.data["purpose"] == "fill details"):
            user = User.objects.get(username = request.data["username"])
            request.data["details"]["user"] = user
            temp = request.data["details"]["skillset"]
            del request.data["details"]["skillset"]
            applicant = ApplicantInfoModel.objects.create(**request.data["details"])
            for skill in temp:
                applicant.skillset.add(skill)
            # print (type(applicant.skillset))
            return Response({"mssg": "data updated successfully!"}, status = 202)

    # Updating the data of the applicant using username.
    def put(self, request, username, format = None):
        user = User.objects.get(username = username)
        if (ApplicantInfoModel.objects.filter(user = user).exists()):
            applicant = ApplicantInfoModel.objects.get(user = user)
            user.email = request.data.get("email")
            applicant.profile_pic = request.data.get("profile_pic")
            applicant.description = request.data.get("description")
            applicant.full_name = request.data.get("full_name")
            applicant.DOB = request.data.get("DOB")
            applicant.gender = request.data.get("gender")
            applicant.address = request.data.get("address")
            applicant.state = request.data.get("state")
            applicant.pincode = request.data.get("pincode")
            applicant.category = request.data.get("category")
            applicant.marital_status = request.data.get("marital_status")
            applicant.phone_number = request.data.get("phone_number")
            applicant.total_experience = request.data.get("total_experience")
            applicant.skillset.clear()
            for skill in request.data["skillset"]:
                applicant.skillset.add(skill)
            applicant.resume = request.data.get("resume")
            user.save()
            applicant.save()
            return Response({"mssg" : "user updated successfully"}, status = 204)
        else:
            return Response({"mssg : Personal Profile not updated!"}, status = 403)

    # Deleting user from the database.
    def delete(self, request, username, format = None):
        user = User.objects.get(username = username)
        user.delete()
        return Response({"mssg": "user delete successfully"}, status = 200)


class CollegeAPIView(APIView):
    def get(self, request, username, format = None):
        user = User.objects.get(username = username)
        if (CollegeInfoModel.objects.filter(user = user).exists()):
            college = CollegeInfoModel.objects.get(user = user)
            temp_result = {}
            temp_result["username"] = college.user.username
            temp_result["email"] = college.user.email
            temp_result["empid"] = college.empid
            temp_result["location"] = college.location
            temp_result["website"] = college.website
            temp_result["director_mail"] = college.director_mail
            temp_result["registrar_mail"] = college.registrar_mail
            temp_result["hod_mail"] = college.hod_mail
            return Response(temp_result, status = 200)
        else:
            return Response({"mssg" : "profile not updated!"}, status = 403)

    def post(self, request, format = None):
        if (request.data["purpose"] == "signup"):
            username = request.data["username"]
            if (User.objects.filter(username = username).exists()):
                return Response({"mssg" : "username already exists!"}, status = 409)
            email = request.data["email"]
            if (User.objects.filter(email = email).exists()):
                return Response({"mssg" : "email already exists!"}, status = 409)
            password = request.data["password"]
            confirm_password = request.data["confirm_password"]
            if (password == confirm_password):
                user = User.objects.create(username = username, email = email, password = password)
                user.set_password(user.password)
                user.save()
                login(request, user)
                return Response({"mssg": "user signed up successfully!"}, status = 200)
            else:
                return Response({"mssg": "passwords do not match!"}, status = 409)
        elif (request.data["purpose"] == "login"):
            if (authenticate(username = request.data["username"], password = request.data["password"])):
                return Response({"mssg": "user logedin successfully!"}, status = 200)
            else:
                return Response({"mssg": "login failed!"}, status = 404)
        elif (request.data["purpose"] == "fill details"):
            user = User.objects.get(username = request.data["username"])
            request.data["details"]["user"] = user
            CollegeInfoModel.objects.create(**request.data["details"])
            return Response({"mssg": "data updated successfully!"}, status = 202)

    def put(self, request, username, format = None):
        user = User.objects.get(username = username)
        college = CollegeInfoModel.objects.get(user = user)
        user.email = request.data.get("email")
        college.empid = request.data.get("empid")
        college.location = request.data.get("location")
        college.website = request.data.get("website")
        college.director_mail = request.data.get("director_mail")
        college.registrar_mail = request.data.get("registrar_mail")
        college.hod_mail = request.data.get("hod_mail")
        user.save()
        college.save()
        return Response({"mssg" : "user updated successfully"}, status = 204)

    def delete(self, request, username, format = None):
        user = User.objects.get(username = username)
        college = CollegeInfoModel.objects.get(user = user)
        user.delete()
        college.delete()
        return Response({"mssg": "user delete successfully"}, status = 200)


# DOCUMENTATION DONE!
# Model for performing the CRUD operations on the user qualification.
class QualificationAPIView(APIView):

    # Method to get the qualifications of a particular applicant using username.
    def get(self, request, username, format = None):
        applicant = User.objects.get(username = username)
        qualifications = ApplicantQualificationModel.objects.filter(applicant = applicant)
        result = []
        for qualification in qualifications:
            temp_result = {}
            temp_result["qualification_title"] = qualification.qualification_title
            temp_result["institute"] = qualification.institute
            temp_result["passing_year"] = qualification.passing_year
            temp_result["marks"] = qualification.marks
            result.append(temp_result)
        return Response({"data" : result}, status = 200)

    # Posting the qualifications of an applicant using the username of the applicant.
    def post(self, request, username, format = None):
        user = User.objects.get(username = username)
        request.data["applicant"] = user
        ApplicantQualificationModel.objects.create(**request.data)
        return Response({"mssg" : "qualification added successfully"}, status = 202)

    # Method to update the qualifications of a user using the username and the qualification title.
    def put(self, request, username, format = None):
        applicant = User.objects.get(username = username)
        qualification = ApplicantQualificationModel.objects.get(applicant = applicant, qualification_title = request.data["title"])
        qualification.qualification_title = request.data["qualification_title"]
        qualification.institute = request.data["institute"]
        qualification.passing_year = request.data["passing_year"]
        qualification.marks = request.data["marks"]
        qualification.save()
        return Response({"mssg" : "qualification updated successfully"}, status = 204)

    # deleting the qualification of the user using username and the qualification title.
    def delete(self, request, username, format = None):
        applicant = User.objects.get(username = username)
        qualification = ApplicantQualificationModel.objects.get(applicant = applicant, qualification_title = request.data["qualification_title"])
        qualification.delete()
        return Response({"mssg": "qualification deleted successfully"}, status = 200)
