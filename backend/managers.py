from django.db import models


class BikeManager(models.Manager):
    def with_match(self, search_string):
        queryset = self.get_queryset()
        match_name = queryset.filter(name__contains=search_string)
        match_model = queryset.filter(model__contains=search_string)
        return match_name.union(match_model)


class CustomerManager(models.Manager):
    def with_email(self, email):
        return self.get_queryset().filter(email__contains=email)
