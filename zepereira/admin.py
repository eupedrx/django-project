from django.contrib import admin
from .models import Animal, MoneyDonation, ItemDonation


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    """
    Admin customizado para o model Animal.
    """
    list_display = ['raca', 'status', 'data_acolhimento', 'data_adocao', 'created_at']
    list_filter = ['status', 'data_acolhimento']
    search_fields = ['raca']
    date_hierarchy = 'data_acolhimento'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('raca', 'status')
        }),
        ('Datas', {
            'fields': ('data_acolhimento', 'data_adocao')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MoneyDonation)
class MoneyDonationAdmin(admin.ModelAdmin):
    """
    Admin customizado para doações em dinheiro.
    """
    list_display = ['valor', 'nome_doador', 'data', 'created_at']
    list_filter = ['data']
    search_fields = ['nome_doador']
    date_hierarchy = 'data'
    ordering = ['-data']
    
    fieldsets = (
        ('Informações da Doação', {
            'fields': ('valor', 'data', 'nome_doador')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['tipo', 'created_at', 'updated_at']


@admin.register(ItemDonation)
class ItemDonationAdmin(admin.ModelAdmin):
    """
    Admin customizado para doações de itens.
    """
    list_display = ['nome_item', 'quantidade', 'nome_doador', 'data', 'created_at']
    list_filter = ['data']
    search_fields = ['nome_item', 'nome_doador']
    date_hierarchy = 'data'
    ordering = ['-data']
    
    fieldsets = (
        ('Informações da Doação', {
            'fields': ('nome_item', 'quantidade', 'data', 'nome_doador')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['tipo', 'created_at', 'updated_at']

