"""
Vendas e Receita:

Total de vendas (somatório do valor total de todas as ordens)
Receita total (somatório do valor total de todas as ordens, considerando descontos)
Clientes e Demografia:

Número total de clientes
Taxa de crescimento de clientes (comparando períodos)
Distribuição de tipos de clientes (demografia)
Produtos:

Produtos mais vendidos (com base nas unidades vendidas)
Margem de lucro por produto (diferença entre o preço de venda e o custo)
Estoque:

Nível médio de estoque
Taxa de rotatividade de estoque
Itens em falta (unidades que estão abaixo do nível de estoque mínimo)
Desempenho de Funcionários:

Número total de funcionários
Número de vendas por funcionário
Taxa de rotatividade de funcionários
Frete e Logística:

Custo médio de frete
Tempo médio de entrega
Número de pedidos entregues dentro do prazo
Regiões e Territórios:

Distribuição de vendas por região/território
Crescimento de vendas em cada região/território
Análise de Vendas:

Taxa de conversão (número de pedidos/número de visitantes)
Valor médio do pedido
Clientes recorrentes versus novos clientes
Análise de Produtividade:

Pedidos processados por hora/dia/semana/mês
Tempo médio de processamento de pedidos
Satisfação do Cliente:

Número de reclamações/sugestões recebidas
Índice de satisfação do cliente (por meio de pesquisas)
Descontinuação de Produtos:

Número de produtos descontinuados
Motivos para descontinuação
Cobertura de Mercado:

Distribuição geográfica de clientes
Cobertura de mercado por região/território


Número de clientes:
Número de Pedidos:
Quantidade de Produtos armazenados:
Venda líquida:

Venda liquida por empregado:
Venda liquida por categorias de produtos:
Venda liquida por shippers:
Venda liquida por pais:

Clientes por empregado:
Clientes por categoria de produtos:
Clientes por shippers:
Clientes por mes/ano:

Pedidos por empregado:
Pedidos por categoria de produtos:
Pedidos por shippers:
Pedidos por ano/mes:
Pedidos por suppliers comanyname:

Produtos por empregado:
Produtos por categoria de produtos:
produtos por shippers:
produtos por mes/ano:

"""


"""
# Exemplos de cálculos de indicadores

# Ticket Médio por Cliente
df_pedidos_produtos = pd.merge(df_tabela8, df_tabela7, on='order_id')
df_pedidos_produtos['total_value'] = df_pedidos_produtos['unit_price'] * df_pedidos_produtos['quantity'] * (1 - df_pedidos_produtos['discount'])
ticket_medio_por_cliente = df_pedidos_produtos.groupby('customer_id')['total_value'].mean()
#print(df_pedidos_produtos)
#print("Ticket Médio por Cliente:")
#print(ticket_medio_por_cliente)


# Taxa de Churn
df_tabela8['order_date'] = pd.to_datetime(df_tabela8['order_date'])
primeira_data_pedido = df_tabela8['order_date'].min()
data_referencia = primeira_data_pedido + pd.DateOffset(years=1)
clientes_finais = df_tabela8[df_tabela8['order_date'] > data_referencia]['customer_id'].nunique()
clientes_iniciais = df_tabela4['customer_id'].nunique()
churn_rate = (clientes_iniciais - clientes_finais) / clientes_iniciais
#print(clientes_iniciais, " - ", clientes_finais)
#print("Taxa de Churn:")
#print(taxa_churn)

# Vendas por Categoria de Produto
df_vendas_por_categoria = pd.merge(pd.merge(df_tabela7, df_tabela8, on='order_id'), df_tabela9, on='product_id')
df_vendas_por_categoria['total_sales'] = df_vendas_por_categoria['unit_price_x'] * df_vendas_por_categoria['quantity']
df_vendas_por_categoria = pd.merge(df_vendas_por_categoria, df_tabela1, on='category_id')
vendas_por_categoria = df_vendas_por_categoria.groupby('category_name').agg({'total_sales': 'sum', 'quantity': 'sum'})
#print("Vendas por Categoria de Produto:")
#print(vendas_por_categoria)

# Faturamento Mensal
df_tabela8['order_date'] = pd.to_datetime(df_tabela8['order_date'])
df_tabela8['order_month'] = df_tabela8['order_date'].dt.to_period('M')
df_vendas_mensais = pd.merge(df_tabela7, df_tabela8, on='order_id')
df_vendas_mensais['total_sales'] = df_vendas_mensais['unit_price'] * df_vendas_mensais['quantity']
faturamento_mensal = df_vendas_mensais.groupby('order_month')['total_sales'].sum()
#print("Faturamento Mensal:")
#print(faturamento_mensal)

# Análise de Margem de Lucro
df_tabela8['order_date'] = pd.to_datetime(df_tabela8['order_date'])
df_analise_margem = pd.merge(pd.merge(df_tabela7, df_tabela8, on='order_id'), df_tabela9, on='product_id')
df_analise_margem['total_sales'] = df_analise_margem['unit_price_x'] * df_analise_margem['quantity']
df_analise_margem['total_cost'] = df_analise_margem['unit_price_y'] * df_analise_margem['quantity']
df_analise_margem['gross_profit'] = df_analise_margem['total_sales'] - df_analise_margem['total_cost']
margem_media = df_analise_margem['gross_profit'].mean()
#print("Margem de Lucro Bruta Média:")
#print(margem_media)

# Criar um gráfico de barras para o ticket médio por cliente
plt.figure(figsize=(10, 6))
ticket_medio_por_cliente.plot(kind='bar')
plt.title('Ticket Médio por Cliente')
plt.xlabel('Cliente')
plt.ylabel('Ticket Médio (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Criar um gráfico de pizza para a taxa de churn
plt.figure(figsize=(6, 6))
plt.pie([churn_rate, 1 - churn_rate], labels=['Churn', 'Retenção'], autopct='%1.1f%%', colors=['red', 'green'])
plt.title('Taxa de Churn')
plt.show()

# ... (cálculo das vendas por categoria)

# Criar um gráfico de barras para as vendas por categoria de produto
plt.figure(figsize=(10, 6))
vendas_por_categoria.plot(kind='bar')
plt.title('Vendas por Categoria de Produto')
plt.xlabel('Categoria')
plt.ylabel('Vendas (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ... (cálculo do faturamento mensal)

# Criar um gráfico de linha para o faturamento mensal
plt.figure(figsize=(10, 6))
faturamento_mensal.plot(kind='line', marker='o')
plt.title('Faturamento Mensal')
plt.xlabel('Mês')
plt.ylabel('Faturamento (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ... (cálculo da margem de lucro)

# Criar um gráfico de barra para a margem de lucro bruta média
plt.figure(figsize=(6, 6))
plt.bar(['Margem de Lucro Bruta Média'], [margem_media], color='blue')
plt.title('Margem de Lucro Bruta Média')
plt.ylabel('Margem de Lucro (%)')
plt.ylim(min(margem_media - 10, 0), max(margem_media + 10, 100))
plt.tight_layout()
plt.show()

####################################################################NOVO

# Total de vendas mensal
order_data1 = df_tabela8.merge(df_tabela7, on='order_id')
order_data1['total_value'] = order_data1['quantity'] * order_data1['unit_price']
order_data1['order_date'] = pd.to_datetime(order_data1['order_date'])
order_data1['order_month'] = order_data1['order_date'].dt.to_period('M')
total_mensal = order_data1.groupby('order_month')['total_value'].sum()
print(total_mensal)

# Receita total mensal
order_data2 = df_tabela8.merge(df_tabela7, on='order_id')
order_data2['total_value'] = (order_data2['quantity'] * order_data2['unit_price']) * (1 - order_data2['discount'])
order_data2['order_date'] = pd.to_datetime(order_data2['order_date'])
order_data2['order_month'] = order_data2['order_date'].dt.to_period('M')
receita_total_mensal = order_data2.groupby('order_month')['total_value'].sum()
#print(receita_total_mensal)

# Diferenca entre total - receita
discontos = total_mensal - receita_total_mensal
discontos_df = pd.DataFrame({
    'Month': discontos.index,
    'Difference': discontos.values
})
#print(discontos_df)

# Ganho com categorias de produtos por mes e total
product_data3 = df_tabela9.merge(df_tabela1, on='category_id')
order_data3 = df_tabela8.merge(df_tabela7, on='order_id')
order_data3['total_value'] = (order_data3['quantity'] * order_data3['unit_price']) * (1 - order_data3['discount'])
order_data3['order_date'] = pd.to_datetime(order_data3['order_date'])
order_data3['order_month'] = order_data3['order_date'].dt.to_period('M')
order_data3 = order_data3.merge(product_data3[['product_id', 'category_name']], on='product_id')
total_categorias_mensal = order_data3.groupby(['order_month', 'category_name'])['total_value'].sum().reset_index()
total_categorias = order_data3.groupby('category_name')['total_value'].sum().reset_index()
total_categorias_ordenado = total_categorias.sort_values(by='total_value', ascending=False)
#print(total_categorias_mensal)
#print(total_categorias_ordenado)

# Top 10 produtos mais e menos vendidos
order_data4 = df_tabela8.merge(df_tabela7, on='order_id')
order_data4['total_value'] = (order_data4['quantity'] * order_data4['unit_price']) * (1 - order_data4['discount'])
product_total_revenue = order_data4.groupby('product_id')['total_value'].sum().reset_index()
product_total_quantity = order_data4.groupby('product_id')['quantity'].sum().reset_index()
top_products_info4 = product_total_revenue.merge(df_tabela9[['product_id', 'product_name']], on='product_id')
top_products_info4 = top_products_info4.merge(product_total_quantity, on='product_id')
top_products_info_sorted4 = top_products_info4.sort_values(by='total_value', ascending=False)
top10_produtos = top_products_info_sorted4.head(10)
bot10_produtos = top_products_info_sorted4.tail(10)
#print(top10_produtos)
#print(bot10_produtos)

# Produto mais e menos vendido em cada mes
order_data5 = df_tabela8.merge(df_tabela7, on='order_id')
order_data5['total_value'] = (order_data5['quantity'] * order_data5['unit_price']) * (1 - order_data5['discount'])
order_data5['order_date'] = pd.to_datetime(order_data5['order_date'])
order_data5['order_month'] = order_data5['order_date'].dt.to_period('M')
product_monthly_quantity = order_data5.groupby(['order_month', 'product_id'])['quantity'].sum().reset_index()
top_products_info5 = product_monthly_quantity.merge(df_tabela9[['product_id', 'product_name']], on='product_id')
top_products_info_sorted5 = top_products_info5.sort_values(by=['order_month', 'quantity'], ascending=[True, False])
top_produtos_mensal = top_products_info_sorted5.groupby('order_month').first()
bot_produtos_mensal = top_products_info_sorted5.groupby('order_month').last()
#print(top_produtos_mensal)
#print(bot_produtos_mensal)

# Top 10 clientes mais e menos compraram
order_data6 = df_tabela8.merge(df_tabela7, on='order_id')
customer_total_quantity = order_data6.groupby('customer_id')['quantity'].sum().reset_index()
top_customers_info6 = customer_total_quantity.merge(df_tabela4[['customer_id', 'contact_name']], on='customer_id')
top_customers_info_sorted6 = top_customers_info6.sort_values(by='quantity', ascending=False)
top_10_customers = top_customers_info_sorted6.head(10)
bottom_10_customers = top_customers_info_sorted6.tail(10)
#print(top_10_customers)
#print(bottom_10_customers)

# Clientes que mais e menos compraram em cada mes
order_data7 = df_tabela8.merge(df_tabela7, on='order_id')
order_data7['order_date'] = pd.to_datetime(order_data7['order_date'])
order_data7['order_month'] = order_data7['order_date'].dt.to_period('M')
monthly_customer_total_quantity = order_data7.groupby(['order_month', 'customer_id'])['quantity'].sum().reset_index()
top_customers_info7 = monthly_customer_total_quantity.merge(df_tabela4[['customer_id', 'contact_name']], on='customer_id')
top_customers_info_sorted7 = top_customers_info7.sort_values(by=['order_month', 'quantity'], ascending=[True, False])
top_customers_per_month = top_customers_info_sorted7.groupby('order_month').first()
bottom_customers_info_sorted7 = top_customers_info7.sort_values(by=['order_month', 'quantity'], ascending=[True, True])
bottom_customers_per_month = bottom_customers_info_sorted7.groupby('order_month').first()
#print(top_customers_per_month)
#print(bottom_customers_per_month)

# Clientes que mais e menos compraram em cada ano
order_data8 = df_tabela8.merge(df_tabela7, on='order_id')
order_data8['order_date'] = pd.to_datetime(order_data8['order_date'])
order_data8['order_year'] = order_data8['order_date'].dt.year
yearly_customer_total_quantity = order_data8.groupby(['order_year', 'customer_id'])['quantity'].sum().reset_index()
top_customers_info8 = yearly_customer_total_quantity.merge(df_tabela4[['customer_id', 'contact_name']], on='customer_id')
top_customers_info_sorted8 = top_customers_info8.sort_values(by=['order_year', 'quantity'], ascending=[True, False])
top_customers_per_year = top_customers_info_sorted8.groupby('order_year').first()
bottom_customers_info_sorted8 = top_customers_info8.sort_values(by=['order_year', 'quantity'], ascending=[True, True])
bottom_customers_per_year = bottom_customers_info_sorted8.groupby('order_year').first()
#print(top_customers_per_year)
#print(bottom_customers_per_year)

# Empregados e suas vendas
employee_order_data = df_tabela6.merge(df_tabela8, left_on='employee_id', right_on='employee_id')
employee_order_data = employee_order_data.merge(df_tabela7, left_on='order_id', right_on='order_id')
employee_order_data['total_value'] = (employee_order_data['quantity'] * employee_order_data['unit_price']) * (1 - employee_order_data['discount'])
employee_sales_info = employee_order_data.groupby('employee_id').agg({
    'first_name': 'first',
    'last_name': 'first',
    'quantity': 'sum',
    'total_value': 'sum'
}).reset_index()
employee_sales_info_sorted = employee_sales_info.sort_values(by='total_value', ascending=False)
#print(employee_sales_info_sorted)


product_order_data = df_tabela9.merge(df_tabela7, on='product_id')
# Agrupe os dados por produto e calcule a quantidade total de produtos vendidos
product_total_sold = product_order_data.groupby('product_id')['quantity'].sum().reset_index()

# Calcule a quantidade total de produtos ainda em estoque
product_total_in_stock = df_tabela9[['product_id', 'units_in_stock']].copy()

# Combine as informações de produtos vendidos e produtos em estoque
product_inventory_info = product_total_sold.merge(product_total_in_stock, on='product_id')

# Calcule as somas totais de produtos vendidos e produtos em estoque
total_sold_sum = product_inventory_info['quantity'].sum()
total_in_stock_sum = product_inventory_info['units_in_stock'].sum()

# Adicione uma linha extra à tabela para mostrar as somas totais
total_row = pd.DataFrame({'product_id': ['Total'], 'quantity': [total_sold_sum], 'units_in_stock': [total_in_stock_sum]})
product_inventory_info = pd.concat([product_inventory_info, total_row], ignore_index=True)

# Exiba a tabela com a quantidade total de produtos vendidos e em estoque, incluindo as somas totais na última linha

#print(product_inventory_info)
"""

# Tabela de Produtos mais vendidos
top_products_names = top10_produtos_quantidade_nomes['product_name']
top_products_quantity = top10_produtos_quantidade_nomes['quantity']
plt.figure(figsize=(10, 6))
plt.bar(top_products_names, top_products_quantity)
plt.xlabel('Produtos')
plt.ylabel('Quantidade Vendida')
plt.title('Top 10 Produtos Mais Vendidos por Quantidade')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(top_products_quantity):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()
print("\n\n")

#Tabela de Produtos menos vendidos
bot_products_names = bot10_produtos_quantidade_nomes['product_name']
bot_products_quantity = bot10_produtos_quantidade_nomes['quantity']
plt.figure(figsize=(10, 6))
plt.bar(bot_products_names, bot_products_quantity)
plt.xlabel('Produtos')
plt.ylabel('Quantidade Vendida')
plt.title('Top 10 Produtos Menos Vendidos por Quantidade')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(bot_products_quantity):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()
print("\n\n\n")