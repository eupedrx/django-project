from rest_framework import serializers
from .models import Animal, MoneyDonation, ItemDonation


class AnimalSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Animal com validações de negócio.
    """
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Animal
        fields = [
            'id',
            'raca',
            'data_acolhimento',
            'data_adocao',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """
        Validação customizada para garantir consistência entre status e data_adocao.
        """
        status = data.get('status')
        data_adocao = data.get('data_adocao')
        
        # Se está atualizando, pegar valores atuais se não foram fornecidos
        if self.instance:
            status = status or self.instance.status
            data_adocao = data_adocao if 'data_adocao' in data else self.instance.data_adocao
        
        # Validações
        if status == 'adotado' and not data_adocao:
            raise serializers.ValidationError({
                'data_adocao': 'Data de adoção é obrigatória quando o status é "adotado".'
            })
        
        if status != 'adotado' and data_adocao:
            raise serializers.ValidationError({
                'data_adocao': 'Data de adoção deve ser nula quando o status não é "adotado".'
            })
        
        return data


class MoneyDonationSerializer(serializers.ModelSerializer):
    """
    Serializer para doações em dinheiro.
    """
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = MoneyDonation
        fields = [
            'id',
            'tipo',
            'tipo_display',
            'data',
            'nome_doador',
            'valor',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['tipo', 'created_at', 'updated_at']
    
    def validate_valor(self, value):
        """
        Validar que o valor é positivo.
        """
        if value <= 0:
            raise serializers.ValidationError('O valor deve ser maior que zero.')
        return value


class ItemDonationSerializer(serializers.ModelSerializer):
    """
    Serializer para doações de itens.
    """
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = ItemDonation
        fields = [
            'id',
            'tipo',
            'tipo_display',
            'data',
            'nome_doador',
            'nome_item',
            'quantidade',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['tipo', 'created_at', 'updated_at']
    
    def validate_quantidade(self, value):
        """
        Validar que a quantidade é positiva.
        """
        if value <= 0:
            raise serializers.ValidationError('A quantidade deve ser maior que zero.')
        return value


class DonationListSerializer(serializers.Serializer):
    """
    Serializer unificado para listagem de todas as doações.
    Combina dados de MoneyDonation e ItemDonation.
    """
    
    id = serializers.IntegerField()
    tipo = serializers.CharField()
    tipo_display = serializers.CharField()
    data = serializers.DateField()
    nome_doador = serializers.CharField()
    
    # Campos específicos de dinheiro (nullable)
    valor = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    # Campos específicos de item (nullable)
    nome_item = serializers.CharField(required=False, allow_null=True)
    quantidade = serializers.IntegerField(required=False, allow_null=True)
    
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
