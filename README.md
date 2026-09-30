# Cantina do IFSP - CJO

Sistema desktop desenvolvido em **Python + PySide6 + SQLite** para organizar o atendimento da cantina do **IFSP – Campus Campos do Jordão (CJO)**.

O projeto foi desenvolvido como atividade acadêmica com o objetivo de reduzir os tumultos nos períodos de maior demanda, permitindo que os clientes realizem seus próprios pedidos e que os responsáveis pela cantina acompanhem o preparo, a entrega e as informações financeiras.

> **Projeto acadêmico:** sistema desenvolvido para fins educacionais.

---

## 📋 Sobre o projeto

Durante os períodos de maior movimento, a cantina pode apresentar filas e concentração de pessoas no atendimento. A proposta deste sistema é separar as etapas do processo:

**Cliente → Pedido → Pagamento → Fila de preparo → Entrega**

Além disso, o sistema possui uma área administrativa para gerenciamento de produtos, acompanhamento dos pedidos e controle financeiro.

---

## 🎯 Objetivos

- Reduzir filas e o tempo gasto no atendimento.
- Permitir que o próprio cliente realize seu pedido.
- Organizar os pedidos em uma fila de preparo.
- Facilitar o acompanhamento dos pedidos pelos funcionários.
- Controlar a retirada dos pedidos.
- Registrar pagamentos.
- Permitir o cadastro de despesas.
- Exibir informações de receitas, despesas e saldo.
- Centralizar as informações da cantina em um único sistema.

---

## ✨ Funcionalidades

### 🛒 Atendimento ao cliente

- Totem de autoatendimento.
- Identificação do cliente pelo nome.
- Cardápio organizado por categorias.
- Seleção de produtos.
- Seleção de variações dos produtos quando disponíveis.
- Adição e remoção de itens do carrinho.
- Alteração da quantidade de itens.
- Cálculo automático do total.
- Seleção da forma de pagamento.
- Confirmação do pedido.
- Geração de número do pedido.
- Consulta dos próprios pedidos.

### 👨‍🍳 Operação da cantina

- Visualização da fila de pedidos.
- Atualização do status dos pedidos.
- Painel de atendimento/preparo.
- Controle dos pedidos aguardando retirada.
- Organização da etapa de entrega.

### 📦 Administração de produtos

- Consulta dos produtos cadastrados.
- Cadastro/alteração de preços.
- Organização dos produtos por categoria.
- Controle de produtos ativos.
- Cadastro de variações de produtos.

### 💰 Controle financeiro

- Registro de pagamentos.
- Registro de despesas.
- Consulta das receitas.
- Consulta das despesas.
- Cálculo do saldo.
- Quantidade de pedidos realizados.
- Dashboard com indicadores da cantina.

---

## 🖥️ Telas do sistema

O sistema possui diferentes telas para separar as funções do cliente e do administrador.

| Tela | Função |
|---|---|
| Login | Entrada no sistema e acesso ao modo administrador |
| Totem | Início do autoatendimento |
| Cardápio | Escolha dos produtos |
| Carrinho | Revisão dos itens do pedido |
| Pagamento | Escolha da forma de pagamento |
| Pedido confirmado | Exibição do número do pedido |
| Meus pedidos | Consulta dos pedidos realizados pelo cliente |
| Fila | Acompanhamento dos pedidos em preparo |
| Atendimento | Controle do atendimento da cantina |
| Entregas | Controle dos pedidos aguardando retirada |
| Produtos | Gerenciamento dos produtos |
| Financeiro | Controle de receitas e despesas |
| Dashboard | Visualização dos principais indicadores |

---

## 🔄 Fluxo principal

```text
┌──────────────┐
│    TOTEM     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   CARDÁPIO   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   CARRINHO   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  PAGAMENTO   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    PEDIDO    │
│  CONFIRMADO  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│     FILA     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  ATENDIMENTO │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   ENTREGA    │
└──────────────┘
```

---

## 🧑‍💼 Área administrativa

O administrador possui acesso às principais funções de gerenciamento:

- Fazer pedidos;
- Acompanhar a fila;
- Controlar o atendimento;
- Controlar as entregas;
- Gerenciar produtos;
- Consultar o financeiro;
- Visualizar o dashboard.

### Acesso padrão

O banco cria automaticamente um usuário administrativo padrão:

```text
Usuário: admin
Senha: admin123
```

> **Importante:** essa credencial é apenas para o ambiente acadêmico/desenvolvimento. Em uma implantação real, a senha deverá ser alterada e armazenada de forma segura.

---

## 🗄️ Banco de dados

O sistema utiliza **SQLite**, sem necessidade de instalar um servidor de banco de dados.

O arquivo é armazenado em:

```text
dados/cantina.db
```

### Principais tabelas

- `usuarios`
- `categorias`
- `produtos`
- `variacoes`
- `pedidos`
- `itens_pedido`
- `pagamentos`
- `despesas`

O banco é inicializado automaticamente pelo sistema e possui dados iniciais cadastrados pelo arquivo `banco/seed.py`.

---

## 🛠️ Tecnologias utilizadas

- **Python**
- **PySide6**
- **SQLite**
- **Qt Widgets**
- **SQL**
- **Git/GitHub**

### Dependência

A versão utilizada do PySide6 está especificada no `requirements.txt`:

```text
PySide6==6.11.2
```

---

## 📁 Estrutura do projeto

```text
cantina_pablo/
│
├── banco/
│   ├── __init__.py
│   ├── database.py
│   └── seed.py
│
├── dados/
│   └── cantina.db
│
├── servicos/
│   ├── __init__.py
│   ├── financeiro_service.py
│   ├── pedido_service.py
│   └── produto_service.py
│
├── telas/
│   ├── __init__.py
│   ├── atendimento.py
│   ├── cardapio.py
│   ├── carrinho.py
│   ├── dashboard.py
│   ├── entrega.py
│   ├── fila.py
│   ├── financeiro.py
│   ├── login.py
│   ├── meus_pedidos.py
│   ├── pagamento.py
│   ├── pedido_confirmado.py
│   ├── principal.py
│   ├── produtos_admin.py
│   └── totem.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 Como executar

### 1. Clone o repositório

Substitua o endereço abaixo pelo endereço do repositório público do projeto:

```bash
git clone <LINK_DO_REPOSITORIO>
```

Entre na pasta:

```bash
cd cantina_pablo
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o sistema

```bash
python main.py
```

## 🍬 Produtos cadastrados

O banco inicial possui produtos divididos em categorias como:

- Doces
- Salgados
- Bebidas
- Cup Noodles

Alguns produtos possuem variações, como sabores ou tipos diferentes.

Exemplos:

```text
Trento
├── Mousse de maracujá
├── Torta de limão
├── Dark
└── Chocolate
```

```text
Caldo
├── Mandioca
├── Abóbora
├── Verde
└── Feijão
```

---

## 💳 Pagamentos

Os pedidos possuem registro de:

- Pedido associado;
- Forma de pagamento;
- Valor;
- Status;
- Data.

Após a confirmação do pedido, o sistema registra o pagamento e gera o número do pedido.

---

## 📊 Financeiro

O módulo financeiro permite acompanhar:

```text
Receita
- Despesas
= Saldo
```

Também é possível registrar despesas informando:

- Descrição;
- Categoria;
- Valor;
- Data.

O dashboard apresenta informações resumidas para facilitar o acompanhamento da situação da cantina.

---

## 🧩 Organização do código

O projeto foi dividido em três partes principais:

### `banco/`

Responsável pela criação e inicialização do banco de dados.

### `servicos/`

Concentra operações relacionadas a:

- Pedidos;
- Produtos;
- Financeiro.

### `telas/`

Contém as interfaces gráficas desenvolvidas com PySide6.

Essa divisão ajuda a separar a interface gráfica das operações de negócio e do acesso ao banco de dados.

---

## 📚 Contexto acadêmico

Este projeto foi desenvolvido para uma atividade acadêmica envolvendo o desenvolvimento de uma solução computacional para um problema identificado no contexto da cantina do **IFSP – Campus Campos do Jordão**.

A proposta considera as dificuldades enfrentadas durante os horários de maior demanda e busca utilizar o autoatendimento e o gerenciamento digital dos pedidos para organizar o fluxo da cantina.

---

## 👥 Autores

**Benjamin Mandla**  
Projeto acadêmico – IFSP Campus Campos do Jordão

> Se o projeto for desenvolvido em dupla, adicione aqui o nome do segundo integrante.

---

## 📄 Documentação

O relatório do projeto apresenta:

- Contextualização do problema;
- Dores do cliente;
- Objetivos;
- Requisitos;
- Solução proposta;
- Fluxo do sistema;
- Explicação das telas;
- Banco de dados;
- Prints da aplicação;
- Conclusão.

