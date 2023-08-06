Check TIER
==========

Django management command to check the tier current instance.

Required the tier setting from localsetting to be in main settings file as 
TIER=localsettings.tier

usage
-----

::
	python -Wi manage.py get_tier <TIER_TO_CHECK>


::
	python -Wi manage.py get_tier staging

will return success if tiers match error code if they do not as well as text.

Install as django app by putting 'check_tier' in installed apps.
