from django.contrib import admin

from exchange.models import Exchange, SymbolPair

admin.site.register(Exchange)
admin.site.register(SymbolPair)
