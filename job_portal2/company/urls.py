from django.urls import re_path
from company import views as company_view

urlpatterns = [
    re_path(r'^companies/$', company_view.companyList.as_view()),
    re_path(r'^companies/(?P<company_id>.*)/recruiters/$',
            company_view.CompanyRecruiterList.as_view()),
    re_path(r'^companies/(?P<company_id>.*)/recruiters/(?P<recruiter_id>.*)/$',
            company_view.CompanyRecruiter.as_view()),
    re_path(r'^companies/(?P<company_id>.*)/addresses/$',
            company_view.CompanyAddressList.as_view()),
    re_path(r'^companies/(?P<company_id>.*)/addresses/(?P<address_id>.*)/$',
            company_view.CompanyAddress.as_view())
]
