from django.contrib import admin

from price_checking.models import Exchange, SymbolPair, Rule

admin.site.register(Exchange)
admin.site.register(SymbolPair)
admin.site.register(Rule)
