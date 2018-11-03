from rest_framework.views import APIView
from .serializers import CompanySerializer
from .serializers import CompanyRecruiterSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from user_profile.models import Profile
from .models import Company
from .models import CompanyRecruiter as Recruiter
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import CompanyAddressSerializer
from core.models import Address
from core.serializers import AddressSerializer
from .models import CompanyAddress as Companyaddress
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from cs_utils.authentication import JWTAuthentication
from .permissions import IsCompanyOwner


class companyList(APIView):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsCompanyOwner, )

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        data['creator'] = request.user.id
        data['last_modifier'] = request.user.id
        serializer = CompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class CompanyRecruiterList(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsCompanyOwner, )

    serializer_class = CompanyRecruiterSerializer

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs['company_id'])
        return Recruiter.objects.filter(
            company=company,
            creator=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = CompanyRecruiterSerializer(data=self.request.data)
        try:
            recruiter_id = self.request.data['recruiter']
        except KeyError:
            return HttpResponse({'should share recruiter id'}, status=400)

        try:
            company = Company.objects.get(pk=kwargs['company_id'])
            recruiter = Profile.objects.get(id=recruiter_id)
            if not recruiter.user_type == 'Recruiter':
                print('recruiter_type error... *****')
                return HttpResponse(status=404)

        except ValidationError:
            return HttpResponse(status=404)

        if serializer.is_valid():
            serializer.save(
                company=company,
                recruiter=recruiter,
                creator=self.request.user.id)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class CompanyRecruiter(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsCompanyOwner, )

    def delete(self, request, company_id, recruiter_id, format=None):
        try:
            company = Company.objects.get(pk=company_id)
            recruiter = Profile.objects.get(pk=recruiter_id)
            company_recruiter = Recruiter.objects.filter(
                company=company,
                recruiter=recruiter,
                creator=self.request.user.id)
        except ValidationError:
            return HttpResponse(status=404)
        company_recruiter.delete()
        return HttpResponse(status=204)


class CompanyAddressList(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsCompanyOwner, )

    def post(self, request, company_id, format=None):
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user.id)
            company = Company.objects.get(pk=company_id)
            address_id = serializer.data['id']
            address = Address.objects.get(pk=address_id)
            companyaddress = Companyaddress(
                company_id=company.id,
                address=address,
                creator=self.request.user.id)
            companyaddress.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def get(self, request, company_id, format=None):
        try:
            company = Company.objects.get(pk=company_id)
        except ValidationError:
            return HttpResponse(status=404)
        company_address_list = Companyaddress.objects.filter(
            company=company,
            creator=self.request.user.id)
        serializer = CompanyAddressSerializer(
            company_address_list, many=True)
        if not company_address_list:
            return HttpResponse(status=404)
        return Response(serializer.data, status=200)


class CompanyAddress(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsCompanyOwner, )

    def get(self, request, company_id, address_id, format=None):

        try:
            company = Company.objects.get(pk=company_id)
            address = Address.objects.get(pk=address_id)
        except ValidationError:
            return HttpResponse(status=404)
        company_address = Companyaddress.objects.filter(
            company=company, address=address)
        serializer = CompanyAddressSerializer(
            company_address, many=True)
        if not company_address:
            return HttpResponse(status=404)
        return Response(serializer.data, status=200)

    def delete(self, request, company_id, address_id, format=None):
        try:
            company = Company.objects.get(pk=company_id)
            address = Address.objects.get(pk=address_id)
            company_address = Companyaddress.objects.filter(
                company=company,
                address=address,
                creator=self.request.user.id)
        except Companyaddress.DoesNotExist:
            return HttpResponse(status=404)
        company_address.delete()
        return HttpResponse(status=204)

    def put(self, request, company_id, address_id, format=None):
        try:
            company = Company.objects.get(pk=company_id)
            address = Address.objects.get(pk=address_id)
            company_address = Companyaddress.objects.filter(
                company=company,
                address=address,
                creator=self.request.user.id)
        except ValidationError:
            return HttpResponse(status=404)
        if not company_address:
            return HttpResponse(status=404)
        address = Address.objects.get(id=address_id)
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            update_value = serializer.data
            address.address_type = update_value['address_type']
            address.line1 = update_value['line1']
            address.line2 = update_value['line2']
            address.city = update_value['city']
            address.state = update_value['state']
            address.country = update_value['country']
            address.postal_code = update_value['postal_code']
            address.creator = self.request.user.id
            address.save()
            return HttpResponse(status=204)
        return JsonResponse(serializer.errors, status=400)
