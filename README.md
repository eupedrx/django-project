<div align="center">

# 🐾 ZePereira - Sistema de Resgate e Adoção

[![Django](https://img.shields.io/badge/Django-6.0.3-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17.1-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietário-yellow.svg)]()

**API REST completa para gerenciamento de instituição de resgate e adoção de animais**

[Funcionalidades](#-funcionalidades) • [Instalação](#-instalação-rápida) • [API Docs](#-api-endpoints) • [Tecnologias](#-stack-tecnológica)

</div>

---

## 📖 Sobre o Projeto

Sistema backend desenvolvido em Django para uma instituição de resgate e adoção de animais. O projeto oferece uma API REST completa e segura para gerenciar animais resgatados, adoções e doações (dinheiro e itens).

### 🎯 Objetivo

Fornecer uma base sólida e escalável para o backend, enquanto o frontend está em desenvolvimento no Figma. O sistema está pronto para integração futura com qualquer framework frontend (React, Vue, Angular, etc.).

## ✨ Funcionalidades

### 🐕 Gestão de Animais
- ✅ Cadastro completo de animais resgatados
- ✅ Controle de status (acolhido, disponível, adotado)
- ✅ Validações automáticas de datas de adoção
- ✅ Filtros avançados por status, raça e data
- ✅ Endpoints customizados para listagens específicas

### 💰 Gestão de Doações
- ✅ Registro de doações em dinheiro
- ✅ Registro de doações de itens (ração, medicamentos, etc.)
- ✅ Suporte a doações anônimas
- ✅ Filtros por tipo de doação
- ✅ Histórico completo de doações

### 🔐 Segurança
- ✅ Autenticação JWT (JSON Web Tokens)
- ✅ Acesso restrito a administradores
- ✅ CORS configurado para frontend
- ✅ Proteção contra ataques comuns
- ✅ Validações em múltiplas camadas

## 🛠 Stack Tecnológica

<table>
<tr>
<td>

**Backend**
- Django 6.0.3
- Django REST Framework 3.17.1
- Python 3.13+

</td>
<td>

**Autenticação**
- Simple JWT 5.5.1
- Token-based auth
- Refresh tokens

</td>
<td>

**Database**

- SQLite
</td>
</tr>
</table>

**Outras ferramentas:**
- `django-filter` - Filtros avançados
- `django-cors-headers` - CORS para SPA
- `psycopg2-binary` - Driver PostgreSQL

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd DjangoProject

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env conforme necessário

# 5. Execute as migrações
python manage.py migrate

# 6. Crie um superusuário
python manage.py createsuperuser

# 7. Inicie o servidor
python manage.py runserver
```

🎉 **Pronto!** A API está rodando em `http://127.0.0.1:8000/`

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Django
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite para desenvolvimento)
DATABASE_URL=sqlite:///db.sqlite3

# Database (PostgreSQL para produção)
# DATABASE_URL=psql://usuario:senha@localhost:5432/zepereira_db

# CORS (URLs do frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```


## 📡 API Endpoints

### 🔑 Autenticação

```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "sua-senha"
}
```

**Resposta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 🐕 Animais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/animals/` | Lista todos os animais |
| `POST` | `/api/animals/` | Cria novo animal |
| `GET` | `/api/animals/{id}/` | Detalhes de um animal |
| `PUT` | `/api/animals/{id}/` | Atualiza animal |
| `PATCH` | `/api/animals/{id}/` | Atualiza parcialmente |
| `DELETE` | `/api/animals/{id}/` | Remove animal |
| `GET` | `/api/animals/disponiveis/` | Animais disponíveis |
| `GET` | `/api/animals/adotados/` | Animais adotados |

**Filtros:**
- `?status=disponivel` - Filtra por status
- `?search=Golden` - Busca por raça
- `?ordering=-data_acolhimento` - Ordenação

### 💰 Doações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/donations/` | Lista todas as doações |
| `GET` | `/api/donations/money/` | Lista doações em dinheiro |
| `POST` | `/api/donations/money/` | Cria doação em dinheiro |
| `GET` | `/api/donations/money/{id}/` | Detalhes da doação |
| `PUT` | `/api/donations/money/{id}/` | Atualiza doação |
| `DELETE` | `/api/donations/money/{id}/` | Remove doação |
| `GET` | `/api/donations/items/` | Lista doações de itens |
| `POST` | `/api/donations/items/` | Cria doação de item |
| `GET` | `/api/donations/items/{id}/` | Detalhes da doação |
| `PUT` | `/api/donations/items/{id}/` | Atualiza doação |
| `DELETE` | `/api/donations/items/{id}/` | Remove doação |

**Filtros:**
- `?tipo=dinheiro` - Apenas doações em dinheiro
- `?tipo=item` - Apenas doações de itens

## 💡 Exemplos de Uso

### Criar um Animal

```bash
curl -X POST http://127.0.0.1:8000/api/animals/ \
  -H "Authorization: Bearer {seu-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "raca": "Golden Retriever",
    "data_acolhimento": "2024-01-15",
    "status": "disponivel"
  }'
```

### Criar Doação em Dinheiro

```bash
curl -X POST http://127.0.0.1:8000/api/donations/money/ \
  -H "Authorization: Bearer {seu-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "2024-03-29",
    "nome_doador": "João Silva",
    "valor": "150.50"
  }'
```

### Listar Animais Disponíveis

```bash
curl -X GET "http://127.0.0.1:8000/api/animals/?status=disponivel" \
  -H "Authorization: Bearer {seu-token}"
```

## 🎨 Interface Admin

Acesse a interface administrativa em: `http://127.0.0.1:8000/admin/`

**Funcionalidades:**
- 📊 Dashboard completo
- 🔍 Filtros e busca avançada
- 📝 Edição em massa
- 📈 Visualização de estatísticas
- 🕒 Histórico de alterações

## 📋 Regras de Negócio

### Animais

1. **Status**: Pode ser `acolhido`, `disponivel` ou `adotado`
2. **Validação**: Se status = `adotado`, a `data_adocao` é **obrigatória**
3. **Validação**: Se status ≠ `adotado`, a `data_adocao` deve ser **null**
4. **Auditoria**: Campos `created_at` e `updated_at` são preenchidos automaticamente

### Doações

1. **Tipos**: `dinheiro` ou `item`
2. **Doador**: Campo opcional (permite doações anônimas)
3. **Validação Dinheiro**: Valor deve ser maior que zero
4. **Validação Item**: Quantidade deve ser maior que zero
5. **Tipo automático**: O campo `tipo` é setado automaticamente pelo sistema

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Testes do app zepereira
python manage.py test zepereira

# Testes com verbose
python manage.py test --verbosity=2

# Testes específicos
python manage.py test zepereira.tests.TestAnimalModel
```

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Shell interativo do Django
python manage.py shell

# Verificar problemas
python manage.py check

# Coletar arquivos estáticos
python manage.py collectstatic
```

## 📁 Estrutura do Projeto

```
DjangoProject/
├── 📁 DjangoProject/          # Configurações do projeto
│   ├── settings.py            # Settings (DRF, JWT, DB, CORS)
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI config
├── 📁 zepereira/              # App principal
│   ├── models.py              # Models (Animal, Donations)
│   ├── serializers.py         # DRF Serializers
│   ├── views.py               # ViewSets
│   ├── permissions.py         # Custom Permissions
│   ├── urls.py                # App URLs
│   └── admin.py               # Admin config
├── 📁 .github/
│   └── copilot-instructions.md
├── .env                       # Variáveis de ambiente (não commitar!)
├── .env.example               # Template de variáveis
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```


<div align="center">

**Desenvolvido com ❤️ para ajudar animais resgatados**

⭐ Se este projeto te ajudou, considere dar uma estrela!

</div>
