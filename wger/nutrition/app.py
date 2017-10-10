from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class NutritionConfig(AppConfig):
	name="wger.nutrition"
	verbose_name=_('nutrition')

	def ready(self):
		import wger.nutrition.signals