from django.contrib import admin
from .models import *

admin.site.register(AllStatsSalaryYear)
admin.site.register(AllStatsVacanciesYear)
admin.site.register(AllStatsSalaryCity)
admin.site.register(AllStatsVacanciesCity)
admin.site.register(AllStatsTopSkills)
admin.site.register(RelevanceSalaryYear)
admin.site.register(RelevanceVacanciesYear)
admin.site.register(GeographySalaryCity)
admin.site.register(GeographyVacanciesCity)
admin.site.register(SkillsTopSkills)
admin.site.register(GraphPicture)