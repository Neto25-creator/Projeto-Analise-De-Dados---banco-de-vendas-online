import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo Excel
df_raw = pd.read_excel('data/OnlineRetail.xlsx')

# Conferir tipo da coluna InvoiceDate no raw (antes dos filtros)
print(f"Tipo InvoiceDate antes do filtro: {df_raw['InvoiceDate'].dtype}")

# Mostrar contagem de registros por dia da semana ANTES dos filtros
print("Contagem de registros por dia da semana (antes dos filtros):")
print(df_raw['InvoiceDate'].dt.day_name().value_counts().sort_index())

# Conferir se InvoiceDate está datetime, se não converter
if not pd.api.types.is_datetime64_any_dtype(df_raw['InvoiceDate']):
    df_raw['InvoiceDate'] = pd.to_datetime(df_raw['InvoiceDate'])

# Copiar para df para limpar e analisar depois
df = df_raw.copy()

# Mostrar as primeiras linhas
print(df.head())

# Informações gerais do dataset
print(df.info())

# Estatísticas básicas
print(df.describe())

# Verificar valores nulos
print(df.isnull().sum())

# Remover linhas sem descrição
df = df.dropna(subset=['Description'])

# Remover linhas com quantidade <= 0 (devoluções e erros)
df = df[df['Quantity'] > 0]

# Remover linhas com preço <= 0 (possíveis erros)
df = df[df['UnitPrice'] > 0]

# Criar coluna de receita
df['Revenue'] = df['Quantity'] * df['UnitPrice']

print(f'Tamanho após limpeza: {df.shape}')
print(df.head())

# Verificar registros para sábado após filtros
print("Descrição estatística para sábado após filtros:")
print(df[df['InvoiceDate'].dt.day_name() == 'Saturday'][['Quantity', 'UnitPrice', 'Revenue']].describe())

print("Contagem de registros por dia da semana (após os filtros):")
print(df['InvoiceDate'].dt.day_name().value_counts().sort_index())

#####################################################################################

# 1. Receita total por país
revenue_by_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
top_countries = revenue_by_country.head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
plt.title('Top 10 países por receita total')
plt.xlabel('Receita Total')
plt.ylabel('País')
plt.show()

#####################################################################################

# 2. Produtos mais vendidos (quantidade)
top_products_qty = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_products_qty.values, y=top_products_qty.index, palette='magma')
plt.title('Top 10 produtos mais vendidos (quantidade)')
plt.xlabel('Quantidade Vendida')
plt.ylabel('Produto')
plt.show()

#####################################################################################

# 3. Receita mensal ao longo do tempo
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
revenue_by_month = df.groupby('YearMonth')['Revenue'].sum()

plt.figure(figsize=(12, 6))
revenue_by_month.plot(kind='line')
plt.title('Receita mensal ao longo do tempo')
plt.xlabel('Mês/Ano')
plt.ylabel('Receita Total')
plt.grid(True)
plt.show()

#####################################################################################

# 4. Ticket médio dos produtos — (corrigido com .agg para evitar DeprecationWarning)
ticket_medio_produtos = df.groupby('Description').agg({
    'Revenue': 'sum',
    'Quantity': 'sum'
})
ticket_medio_produtos['TicketMedio'] = ticket_medio_produtos['Revenue'] / ticket_medio_produtos['Quantity']
ticket_medio_produtos = ticket_medio_produtos['TicketMedio'].sort_values(ascending=False).head(10)

print("Ticket médio dos 10 produtos com maior ticket:")
print(ticket_medio_produtos)

#####################################################################################

# 5. Análise de vendas por dia da semana
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()

# Dias da semana para reindexar e garantir ordem correta
dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
vendas_por_dia = df.groupby('DayOfWeek')['Revenue'].sum().reindex(dias_semana)

print("Receita total por dia da semana:")
print(vendas_por_dia)

# Plotar gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x=vendas_por_dia.index, y=vendas_por_dia.values, palette='coolwarm')
plt.title('Receita total por dia da semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Receita Total')
plt.xticks(rotation=45)
plt.show()