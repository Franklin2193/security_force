from django.urls import path
from .views import home, VulnerabilityListView, FixedVulnerabilitiesView, ActiveVulnerabilitiesView, VulnerabilitySummaryView

urlpatterns = [
    path('', home, name='home'),
    path('vulnerabilities/', VulnerabilityListView.as_view(), name='vulnerability-list'),
    path('vulnerabilities/fixed/', FixedVulnerabilitiesView.as_view(), name='add-fixed-vulnerabilities'),
    path('vulnerabilities/active/', ActiveVulnerabilitiesView.as_view(), name='active-vulnerabilities'),
    path('vulnerabilities/summary/', VulnerabilitySummaryView.as_view(), name='vulnerability-summary'),
]
