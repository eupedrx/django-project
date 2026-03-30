from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Animal, MoneyDonation, ItemDonation
from .serializers import (
    AnimalSerializer,
    MoneyDonationSerializer,
    ItemDonationSerializer,
    DonationListSerializer
)
from .permissions import IsStaffUser


class AnimalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de animais.
    
    Endpoints:
    - GET /api/animals/ - Lista todos os animais
    - POST /api/animals/ - Cria um novo animal
    - GET /api/animals/{id}/ - Detalhes de um animal
    - PUT/PATCH /api/animals/{id}/ - Atualiza um animal
    - DELETE /api/animals/{id}/ - Remove um animal
    
    Filtros disponíveis:
    - ?status=acolhido
    - ?status=disponivel
    - ?status=adotado
    - ?search=Golden (busca em raça)
    - ?ordering=-data_acolhimento (ordenação)
    """
    
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsStaffUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['raca']
    ordering_fields = ['data_acolhimento', 'data_adocao', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """
        Endpoint customizado para listar apenas animais disponíveis para adoção.
        GET /api/animals/disponiveis/
        """
        animais = self.queryset.filter(status='disponivel')
        serializer = self.get_serializer(animais, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def adotados(self, request):
        """
        Endpoint customizado para listar apenas animais adotados.
        GET /api/animals/adotados/
        """
        animais = self.queryset.filter(status='adotado')
        serializer = self.get_serializer(animais, many=True)
        return Response(serializer.data)


class DonationViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de doações (dinheiro e itens).
    
    Endpoints:
    - GET /api/donations/ - Lista todas as doações
    - GET /api/donations/money/ - Lista doações em dinheiro
    - POST /api/donations/money/ - Cria doação em dinheiro
    - GET /api/donations/items/ - Lista doações de itens
    - POST /api/donations/items/ - Cria doação de item
    - GET /api/donations/money/{id}/ - Detalhes de doação em dinheiro
    - PUT/PATCH /api/donations/money/{id}/ - Atualiza doação em dinheiro
    - DELETE /api/donations/money/{id}/ - Remove doação em dinheiro
    - GET /api/donations/items/{id}/ - Detalhes de doação de item
    - PUT/PATCH /api/donations/items/{id}/ - Atualiza doação de item
    - DELETE /api/donations/items/{id}/ - Remove doação de item
    
    Filtros disponíveis:
    - ?tipo=dinheiro ou ?tipo=item (na lista geral)
    """
    
    permission_classes = [IsStaffUser]
    
    def list(self, request):
        """
        Lista todas as doações (dinheiro + itens) de forma unificada.
        """
        tipo_filter = request.query_params.get('tipo', None)
        
        # Buscar doações de dinheiro
        money_donations = MoneyDonation.objects.all()
        if tipo_filter == 'dinheiro':
            item_donations = []
        else:
            item_donations = ItemDonation.objects.all()
            if tipo_filter == 'item':
                money_donations = []
        
        # Combinar e serializar
        all_donations = []
        
        for donation in money_donations:
            all_donations.append({
                'id': donation.id,
                'tipo': donation.tipo,
                'tipo_display': donation.get_tipo_display(),
                'data': donation.data,
                'nome_doador': donation.nome_doador,
                'valor': donation.valor,
                'nome_item': None,
                'quantidade': None,
                'created_at': donation.created_at,
                'updated_at': donation.updated_at,
            })
        
        for donation in item_donations:
            all_donations.append({
                'id': donation.id,
                'tipo': donation.tipo,
                'tipo_display': donation.get_tipo_display(),
                'data': donation.data,
                'nome_doador': donation.nome_doador,
                'valor': None,
                'nome_item': donation.nome_item,
                'quantidade': donation.quantidade,
                'created_at': donation.created_at,
                'updated_at': donation.updated_at,
            })
        
        # Ordenar por data (mais recente primeiro)
        all_donations.sort(key=lambda x: x['data'], reverse=True)
        
        serializer = DonationListSerializer(all_donations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'post'])
    def money(self, request):
        """
        Lista ou cria doações em dinheiro.
        """
        if request.method == 'GET':
            donations = MoneyDonation.objects.all()
            serializer = MoneyDonationSerializer(donations, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = MoneyDonationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path='money/(?P<pk>[^/.]+)')
    def money_detail(self, request, pk=None):
        """
        Detalhes, atualização ou remoção de doação em dinheiro.
        """
        try:
            donation = MoneyDonation.objects.get(pk=pk)
        except MoneyDonation.DoesNotExist:
            return Response({'detail': 'Doação não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = MoneyDonationSerializer(donation)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = MoneyDonationSerializer(donation, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            donation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get', 'post'])
    def items(self, request):
        """
        Lista ou cria doações de itens.
        """
        if request.method == 'GET':
            donations = ItemDonation.objects.all()
            serializer = ItemDonationSerializer(donations, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = ItemDonationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path='items/(?P<pk>[^/.]+)')
    def items_detail(self, request, pk=None):
        """
        Detalhes, atualização ou remoção de doação de item.
        """
        try:
            donation = ItemDonation.objects.get(pk=pk)
        except ItemDonation.DoesNotExist:
            return Response({'detail': 'Doação não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = ItemDonationSerializer(donation)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = ItemDonationSerializer(donation, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            donation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

