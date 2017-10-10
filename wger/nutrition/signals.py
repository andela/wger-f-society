from wger.nutrition.models import NutritionPlan
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.core.cache import cache


@receiver([post_delete,post_save], sender=NutritionPlan)
def delete_plan(sender,instance,**kwargs):
	cache.delete(instance.id)