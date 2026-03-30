from django.db import models
from django.core.exceptions import ValidationError


class Animal(models.Model):
    """
    Model para representar animais resgatados pela instituição.
    """
    
    STATUS_CHOICES = [
        ('acolhido', 'Acolhido'),
        ('disponivel', 'Disponível para Adoção'),
        ('adotado', 'Adotado'),
    ]
    
    raca = models.CharField('Raça', max_length=100)
    data_acolhimento = models.DateField('Data de Acolhimento')
    data_adocao = models.DateField('Data de Adoção', null=True, blank=True)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='acolhido'
    )
    
    # Campos de auditoria
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.raca} - {self.get_status_display()}"
    
    def clean(self):
        """
        Validação personalizada:
        - Se status = 'adotado', data_adocao deve estar preenchida
        - Se status != 'adotado', data_adocao deve ser nula
        """
        if self.status == 'adotado' and not self.data_adocao:
            raise ValidationError({
                'data_adocao': 'Data de adoção é obrigatória quando o status é "adotado".'
            })
        
        if self.status != 'adotado' and self.data_adocao:
            raise ValidationError({
                'data_adocao': 'Data de adoção deve ser nula quando o status não é "adotado".'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class DonationBase(models.Model):
    """
    Model abstrato base para doações.
    """
    
    TIPO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('item', 'Item'),
    ]
    
    tipo = models.CharField(
        'Tipo de Doação',
        max_length=20,
        choices=TIPO_CHOICES
    )
    data = models.DateField('Data da Doação')
    nome_doador = models.CharField(
        'Nome do Doador',
        max_length=200,
        blank=True,
        help_text='Opcional'
    )
    
    # Campos de auditoria
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-data']


class MoneyDonation(DonationBase):
    """
    Model para doações em dinheiro.
    """
    
    valor = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2,
        help_text='Valor em reais (R$)'
    )
    
    class Meta:
        verbose_name = 'Doação em Dinheiro'
        verbose_name_plural = 'Doações em Dinheiro'
        ordering = ['-data']
    
    def __str__(self):
        doador = self.nome_doador or 'Anônimo'
        return f"R$ {self.valor} - {doador} ({self.data})"
    
    def save(self, *args, **kwargs):
        self.tipo = 'dinheiro'
        super().save(*args, **kwargs)


class ItemDonation(DonationBase):
    """
    Model para doações de itens.
    """
    
    nome_item = models.CharField('Nome do Item', max_length=200)
    quantidade = models.PositiveIntegerField('Quantidade', default=1)
    
    class Meta:
        verbose_name = 'Doação de Item'
        verbose_name_plural = 'Doações de Itens'
        ordering = ['-data']
    
    def __str__(self):
        doador = self.nome_doador or 'Anônimo'
        return f"{self.nome_item} (x{self.quantidade}) - {doador} ({self.data})"
    
    def save(self, *args, **kwargs):
        self.tipo = 'item'
        super().save(*args, **kwargs)

