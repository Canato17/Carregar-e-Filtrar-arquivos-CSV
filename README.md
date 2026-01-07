# Carregar-e-Filtrar-arquivos-CSV
Sobre o Projeto
  Uma aplicação web simples e intuitiva para carregar, filtrar e exportar dados de arquivos CSV. Desenvolvida com Python e Streamlit, permite visualizar e manipular dados de forma interativa.

Funcionalidades
  Upload de CSV: Carrega arquivos CSV com suporte a múltiplos encodings

Filtros Avançados:
  Filtro por nome
  Filtro por gênero (Masculino/Feminino)
  Filtro por país e cidade
  Filtro por ano de nascimento (range)
  Filtro por número de seguidores (range)
  Filtro por permissão de mensagens privadas
Visualização: Dataframe interativo com seleção de colunas
Estatísticas: Visualização de distribuição de dados
Exportação: Download dos dados filtrados em CSV e Excel
Interface Responsiva: Layout limpo e fácil de usar

Estrutura do Código
app.py
├── Configuração da página
├── Funções de carregamento de CSV
├── Funções de conversão de datas
├── Interface Streamlit
│   ├── Sidebar (upload e filtros)
│   ├── Área principal (visualização)
│   └── Exportação de dados
└── Exemplo de dados

Como Executar
  Pré-requisitos
    Python 3.8 ou superior
    pip (gerenciador de pacotes Python)

Instalação
  Clone o repositório:
    git clone https://github.com/seu-usuario/csv-filter-app.git
    cd csv-filter-app

Instale as dependências:
    pip install streamlit pandas openpyxl
  
Execute a aplicação:
  streamlit run app.py



# Instalar dependências
pip install -r requirements.txt

Estrutura de Dados Suportada
A aplicação espera um CSV com as seguintes colunas:

first_name,last_name,id,last_seen,sex,followers_count,country_id,
country_title,city_id,city_title,bdate,byear,contacts,connections,
can_write_private_message,can_post

Tecnologias Utilizadas
Python 3: Linguagem principal
Streamlit: Framework para aplicações web
Pandas: Manipulação de dados

Uso da Aplicação
Upload: Clique em "Browse files" ou arraste um arquivo CSV
Filtragem: Use os filtros na sidebar para refinar os dados
Visualização: Veja os dados filtrados na tabela principal
Estatísticas: Expanda a seção de estatísticas para insights
Exportação: Baixe os dados filtrados em CSV ou Excel


Dica: Para testar rapidamente, use o arquivo test_data.csv incluído no repositório!
