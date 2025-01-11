from django.db import models
import os


class AllStatsSalaryYear(models.Model):
    salary = models.FloatField('Зарплата')
    date = models.CharField('Дата', max_length=4)


    def __str__(self):
        return f"{self.date}"


    class Meta:
        db_table = 'all_stats_salary_year'


class AllStatsVacanciesYear(models.Model):
    vacancies_count = models.IntegerField('Количество вакансий')
    date = models.CharField('Дата', max_length=4)


    def __str__(self):
        return f"{self.date}"


    class Meta:
        db_table = 'all_stats_vacancies_year'


class AllStatsSalaryCity(models.Model):
    salary = models.FloatField('Зарплата', null=True, blank=True)
    city = models.CharField('Город', max_length=255)


    def __str__(self):
        return f"{self.city}"


    class Meta:
        db_table = 'all_stats_salary_city'


class AllStatsVacanciesCity(models.Model):
    vacancies_count = models.IntegerField('Количество вакансий', null=True, blank=True)
    city = models.CharField('Город', max_length=255)


    def __str__(self):
        return f"{self.city}"


    class Meta:
        db_table = 'all_stats_vacancies_city'


class AllStatsTopSkills(models.Model):
    current_skill = models.CharField('Навык', max_length=255)
    skill_count = models.IntegerField()
    date = models.CharField('Дата', max_length=4)


    def __str__(self):
        return f"{self.date} {self.current_skill}"


    class Meta:
        db_table = 'all_stats_top_skills'


class RelevanceSalaryYear(models.Model):
    salary = models.FloatField('Зарплата')
    date = models.CharField('Дата', max_length=4)


    def __str__(self):
        return f"{self.date}"


    class Meta:
        db_table = 'relevance_salary_year'


class RelevanceVacanciesYear(models.Model):
    vacancies_count = models.IntegerField('Количество вакансий')
    date = models.CharField('Дата', max_length=4)


    def __str__(self):
        return f"{self.date}"


    class Meta:
        db_table = 'relevance_vacancies_year'


class GeographySalaryCity(models.Model):
    salary = models.FloatField('Зарплата', null=True, blank=True)
    city = models.CharField('Город', max_length=255)


    def __str__(self):
        return f"{self.city}"


    class Meta:
        db_table = 'geography_salary_city'


class GeographyVacanciesCity(models.Model):
    vacancies_count = models.IntegerField('Количество вакансий', null=True, blank=True)
    city = models.CharField('Город', max_length=255)


    def __str__(self):
        return f"{self.city}"


    class Meta:
        db_table = 'geography_vacancies_city'


class SkillsTopSkills(models.Model):
    current_skill = models.CharField('Навык', max_length=255)
    skill_count = models.IntegerField()
    date = models.CharField('Дата', max_length=4)


    def __str__(self):
        return f"{self.date} {self.current_skill}"


    class Meta:
        db_table = 'skills_top_skills'


class GraphPicture(models.Model):
    current_graph = models.ImageField('График', upload_to='')
    graph_name = models.CharField('Название графика', max_length=255)


    def __str__(self):
        return self.graph_name


    def save_graph(self, *args, **kwargs):
        try:
            previous_graph = GraphPicture.objects.get(graph_name=self.graph_name)
            previous_photo = previous_graph.current_graph
            if previous_photo and (self.current_graph != previous_photo):
                storage = previous_photo.storage
                path = previous_photo.path

                if os.path.exists(path):
                    storage.delete(path)
        except GraphPicture.DoesNotExist:
            pass
        super().save(*args, **kwargs)


    def delete_graph(self, *args, **kwargs):
        graph_to_delete = self.current_graph
        if graph_to_delete:
            storage = graph_to_delete.storage
            path = graph_to_delete.path
            if os.path.exists(path):
                storage.delete(path)
        super().delete(*args, **kwargs)


    class Meta:
        db_table = 'graphs'