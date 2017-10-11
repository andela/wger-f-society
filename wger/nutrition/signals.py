from wger.nutrition.models import NutritionPlan, Meal, MealItem
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache

signal_types = [post_delete, post_save]


@receiver(signal_types, sender=NutritionPlan)
@receiver(signal_types, sender=Meal)
@receiver(signal_types, sender=MealItem)
def delete_cache(sender, instance, **kwargs):
    plan = instance.get_owner_object()
    cache.delete(plan.id)
