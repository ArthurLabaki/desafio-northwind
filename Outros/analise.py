import pandas as pd
import matplotlib.pyplot as plt
import locale


# Carregar os dados
df_tabela1 = pd.read_csv('Dados/categories.csv', sep=';')
df_tabela2 = pd.read_csv('Dados/customer_customer_demo.csv', sep=';')
df_tabela3 = pd.read_csv('Dados/customer_demographics.csv', sep=';')
df_tabela4 = pd.read_csv('Dados/customers.csv', sep=';')
df_tabela5 = pd.read_csv('Dados/employee_territories.csv', sep=';')
df_tabela6 = pd.read_csv('Dados/employees.csv', sep=';')
df_tabela7 = pd.read_csv('Dados/order_details.csv', sep=';')
df_tabela8 = pd.read_csv('Dados/orders.csv', sep=';')
df_tabela9 = pd.read_csv('Dados/products.csv', sep=';')
df_tabela10 = pd.read_csv('Dados/region.csv', sep=';')
df_tabela11 = pd.read_csv('Dados/shippers.csv', sep=';')
df_tabela12 = pd.read_csv('Dados/suppliers.csv', sep=';')
df_tabela13 = pd.read_csv('Dados/territories.csv', sep=';')
df_tabela14 = pd.read_csv('Dados/us_states.csv', sep=';')


# Defina a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Número de clientes
num_customers = df_tabela4.shape[0]

# Número de pedidos
num_orders = df_tabela8.shape[0]

# Crie um DataFrame combinando as informações relevantes das tabelas "orders" e "order_details"
order_data = df_tabela8.merge(df_tabela7, on='order_id')

# Quantidade total de produtos vendidos
total_products_sold = order_data['quantity'].sum()

# Venda líquida total (total de valores dos pedidos após descontos)
total_net_sales = (order_data['quantity'] * order_data['unit_price'] * (1 - order_data['discount'])).sum()

# Lucro bruto total (total de valores dos pedidos antes dos descontos)
total_gross_profit = (order_data['quantity'] * order_data['unit_price']).sum()

# Supondo que df_tabela9 seja a tabela de produtos (products)

# Quantidade total de produtos ainda no estoque
total_products_in_stock = df_tabela9['units_in_stock'].sum()

# Formate os valores para a moeda brasileira
total_net_sales_formatted = locale.currency(total_net_sales, grouping=True, symbol=True)
total_gross_profit_formatted = locale.currency(total_gross_profit, grouping=True, symbol=True)

# Exiba as informações
print("Número de Clientes:", num_customers)
print("Número de Pedidos:", num_orders)
print("Quantidade de Produtos Vendidos:", total_products_sold)
print("Venda Líquida Total:", total_net_sales_formatted)
print("Lucro Bruto Total:", total_gross_profit_formatted)
print("Quantidade de Produtos em Estoque:", total_products_in_stock)




# Combine as informações relevantes das tabelas "orders", "order_details" e "employees"
employee_order_data = df_tabela6.merge(df_tabela8, left_on='employee_id', right_on='employee_id')
employee_order_data = employee_order_data.merge(df_tabela7, left_on='order_id', right_on='order_id')
employee_sales = (employee_order_data['quantity'] * employee_order_data['unit_price'] * (1 - employee_order_data['discount'])).groupby(employee_order_data['employee_id']).sum().reset_index()
employee_sales = employee_sales.rename(columns={0: 'Venda Líquida'})
employee_sales = employee_sales.merge(df_tabela6, left_on='employee_id', right_on='employee_id')

# Combine as informações relevantes das tabelas "orders", "order_details", "products" e "categories"
product_order_data = df_tabela8.merge(df_tabela7, on='order_id')
product_order_data = product_order_data.merge(df_tabela9, on='product_id')
product_order_data = product_order_data.merge(df_tabela1, on='category_id')

# Calcule a venda líquida total para cada categoria de produto
category_sales = (product_order_data['quantity'] * product_order_data['unit_price_y'] * (1 - product_order_data['discount'])).groupby(product_order_data['category_name']).sum().reset_index()
category_sales = category_sales.rename(columns={0: 'Venda Líquida'})

# Combine as informações relevantes das tabelas "orders", "order_details" e "shippers"
shipper_order_data = df_tabela8.merge(df_tabela7, on='order_id')
shipper_order_data = shipper_order_data.merge(df_tabela11, left_on='ship_via', right_on='shipper_id')  # Corrigir a coluna de junção

# Calcule a venda líquida total para cada shipper
shipper_sales = (shipper_order_data['quantity'] * shipper_order_data['unit_price'] * (1 - shipper_order_data['discount'])).groupby(shipper_order_data['company_name']).sum().reset_index()
shipper_sales = shipper_sales.rename(columns={0: 'Venda Líquida'})

# Combine as informações relevantes das tabelas "orders", "order_details" e "customers"
country_order_data = df_tabela8.merge(df_tabela7, on='order_id')
country_order_data = country_order_data.merge(df_tabela4, on='customer_id')

# Calcule a venda líquida total para cada país
country_sales = (country_order_data['quantity'] * country_order_data['unit_price'] * (1 - country_order_data['discount'])).groupby(country_order_data['country']).sum().reset_index()
country_sales = country_sales.rename(columns={0: 'Venda Líquida'})

# Ordenar por maior venda líquida
employee_sales = employee_sales.sort_values(by='Venda Líquida', ascending=False)
employee_sales = employee_sales[['first_name', 'last_name', 'Venda Líquida']]
category_sales = category_sales.sort_values(by='Venda Líquida', ascending=False)
shipper_sales = shipper_sales.sort_values(by='Venda Líquida', ascending=False)
country_sales = country_sales.sort_values(by='Venda Líquida', ascending=False)

# Formate os valores da venda líquida para duas casas decimais
def format_decimal(x):
    formatted_value = "R$: {:,.2f}".format(x).replace(",", "X").replace(".", ",").replace("X", ".")
    return round(x, 2)

employee_sales['Venda Líquida'] = employee_sales['Venda Líquida'].apply(format_decimal)
category_sales['Venda Líquida'] = category_sales['Venda Líquida'].apply(format_decimal)
shipper_sales['Venda Líquida'] = shipper_sales['Venda Líquida'].apply(format_decimal)
country_sales['Venda Líquida'] = country_sales['Venda Líquida'].apply(format_decimal)

# Exiba as tabelas
#print("Venda Líquida por Empregado:")
#print(employee_sales)
#print("\nVenda Líquida por Categorias de Produtos:")
#print(category_sales)
#print("\nVenda Líquida por Shippers:")
#print(shipper_sales)
#print("\nVenda Líquida por País:")
#print(country_sales)

###
df_tabela8['order_date'] = pd.to_datetime(df_tabela8['order_date'])
df_tabela8['order_month'] = df_tabela8['order_date'].dt.to_period('M')
df_vendas_mensais = pd.merge(df_tabela7, df_tabela8, on='order_id')
df_vendas_mensais['total_sales'] = df_vendas_mensais['unit_price'] * df_vendas_mensais['quantity'] * (1 - df_vendas_mensais['discount'])
faturamento_mensal = df_vendas_mensais.groupby('order_month')['total_sales'].sum()

#print("Faturamento Mensal:")
#print(faturamento_mensal)
###

# Combine as informações relevantes das tabelas "orders", "order_details" e "customers"
customer_order_data = df_tabela8.merge(df_tabela7, on='order_id')
customer_order_data = customer_order_data.merge(df_tabela4, on='customer_id')

# Agrupe a quantidade de clientes por empregado
customers_per_employee = customer_order_data.groupby('employee_id')['customer_id'].nunique().reset_index()
customers_per_employee = customers_per_employee.rename(columns={'customer_id': 'Clientes'})

# Ordene a tabela de Clientes por Empregado pela quantidade de clientes
customers_per_employee = customers_per_employee.sort_values(by='Clientes', ascending=False)

# Combine as informações dos empregados
customers_per_employee = customers_per_employee.merge(df_tabela6, on='employee_id')
customers_per_employee = customers_per_employee[['first_name', 'last_name', 'Clientes']]

# Combine as informações relevantes das tabelas "orders", "order_details", "products", "categories" e "customers"
customer_category_data = df_tabela8.merge(df_tabela7, on='order_id')
customer_category_data = customer_category_data.merge(df_tabela9, on='product_id')
customer_category_data = customer_category_data.merge(df_tabela1, on='category_id')
customer_category_data = customer_category_data.merge(df_tabela4, on='customer_id')

# Agrupe a quantidade de clientes por categoria de produtos
customers_per_category = customer_category_data.groupby('category_name')['customer_id'].nunique().reset_index()
customers_per_category = customers_per_category.rename(columns={'customer_id': 'Clientes'})

# Ordene a tabela de Clientes por Categoria de Produtos pela quantidade de clientes
customers_per_category = customers_per_category.sort_values(by='Clientes', ascending=False)

# Combine as informações relevantes das tabelas "orders", "order_details", "shippers" e "customers"
customer_shipper_data = df_tabela8.merge(df_tabela7, on='order_id')
customer_shipper_data = customer_shipper_data.merge(df_tabela11, left_on='ship_via', right_on='shipper_id')
customer_shipper_data = customer_shipper_data.merge(df_tabela4, on='customer_id')

# Agrupe a quantidade de clientes por shipper
customers_per_shipper = customer_shipper_data.groupby('company_name_x')['customer_id'].nunique().reset_index()
customers_per_shipper = customers_per_shipper.rename(columns={'customer_id': 'Clientes'})

# Ordene a tabela de Clientes por Shippers pela quantidade de clientes
customers_per_shipper = customers_per_shipper.sort_values(by='Clientes', ascending=False)

# Crie uma coluna 'mes_ano' no DataFrame de pedidos para extrair o mês e o ano
df_tabela8['order_date'] = pd.to_datetime(df_tabela8['order_date'])
df_tabela8['mes_ano'] = df_tabela8['order_date'].dt.to_period('M')

# Combine as informações relevantes das tabelas "orders", "order_details" e "customers"
customer_month_data = df_tabela8.merge(df_tabela7, on='order_id')
customer_month_data = customer_month_data.merge(df_tabela4, on='customer_id')

# Agrupe a quantidade de clientes por mês/ano
customers_per_month = customer_month_data.groupby('mes_ano')['customer_id'].nunique().reset_index()
customers_per_month = customers_per_month.rename(columns={'customer_id': 'Clientes'})


# Exiba as tabelas
#print("Clientes por Empregado:")
#print(customers_per_employee)
#print("Clientes por Categoria de Produtos:")
#print(customers_per_category)
#print("Clientes por Shippers:")
#print(customers_per_shipper)
#print("Clientes por Mês/Ano:")
#print(customers_per_month)

# Suponha que você tenha um DataFrame df_employee com informações dos empregados (tabela "employee")

# Combine as informações relevantes das tabelas "orders" e "employees"
orders_employee_data = df_tabela8.merge(df_tabela6, left_on='employee_id', right_on='employee_id')

# Contagem de pedidos por empregado
orders_per_employee = orders_employee_data.groupby(['first_name', 'last_name'])['order_id'].nunique().reset_index()
orders_per_employee = orders_per_employee.rename(columns={'order_id': 'Pedidos'})

# Ordenar por maior número de pedidos
orders_per_employee = orders_per_employee.sort_values(by='Pedidos', ascending=False)


# Combine as informações relevantes das tabelas "orders", "order_details", "products" e "categories"
orders_product_data = df_tabela8.merge(df_tabela7, on='order_id')
orders_product_data = orders_product_data.merge(df_tabela9, on='product_id')
orders_product_data = orders_product_data.merge(df_tabela1, on='category_id')

# Contagem de pedidos por categoria de produtos
orders_per_category = orders_product_data.groupby('category_name')['order_id'].nunique().reset_index()
orders_per_category = orders_per_category.rename(columns={'order_id': 'Pedidos'})

# Ordenar por maior número de pedidos
orders_per_category = orders_per_category.sort_values(by='Pedidos', ascending=False)

# Combine as informações relevantes das tabelas "orders", "order_details" e "shippers"
orders_shipper_data = df_tabela8.merge(df_tabela7, on='order_id')
orders_shipper_data = orders_shipper_data.merge(df_tabela11, left_on='ship_via', right_on='shipper_id')

# Contagem de pedidos por shipper
orders_per_shipper = orders_shipper_data.groupby('company_name')['order_id'].nunique().reset_index()
orders_per_shipper = orders_per_shipper.rename(columns={'order_id': 'Pedidos'})

# Ordenar por maior número de pedidos
orders_per_shipper = orders_per_shipper.sort_values(by='Pedidos', ascending=False)

# Crie uma coluna 'ano_mes' no DataFrame de pedidos para extrair o ano e o mês
df_tabela8['ano_mes'] = df_tabela8['order_date'].dt.to_period('M')

# Contagem de pedidos por ano/mês
orders_per_year_month = df_tabela8.groupby('ano_mes')['order_id'].nunique().reset_index()
orders_per_year_month = orders_per_year_month.rename(columns={'order_id': 'Pedidos'})

# Ordenar por ano/mês
orders_per_year_month = orders_per_year_month.sort_values(by='ano_mes')

# Combine as informações relevantes das tabelas "orders", "order_details", "products" e "suppliers"
orders_product_supplier_data = df_tabela8.merge(df_tabela7, on='order_id')
orders_product_supplier_data = orders_product_supplier_data.merge(df_tabela9, on='product_id')
orders_product_supplier_data = orders_product_supplier_data.merge(df_tabela12, on='supplier_id')

# Contagem de pedidos por supplier company name
orders_per_supplier = orders_product_supplier_data.groupby('company_name')['order_id'].nunique().reset_index()
orders_per_supplier = orders_per_supplier.rename(columns={'order_id': 'Pedidos'})

# Ordenar por maior número de pedidos
orders_per_supplier = orders_per_supplier.sort_values(by='Pedidos', ascending=False)

#print("Pedidos por Empregado:")
#print(orders_per_employee)
#print("Pedidos por Categoria de Produtos:")
#print(orders_per_category)
#print("Pedidos por Shippers:")
#print(orders_per_shipper)
#print("Pedidos por Ano/Mês:")
#print(orders_per_year_month)
#print("Pedidos por Supplier CompanyName:")
#print(orders_per_supplier)

# Combine as informações relevantes das tabelas "order_details", "orders" e "employees"
product_employee_data = df_tabela7.merge(df_tabela8, on='order_id')
product_employee_data = product_employee_data.merge(df_tabela6, left_on='employee_id', right_on='employee_id')

products_per_employee = product_employee_data.groupby([ 'first_name', 'last_name'])['quantity'].sum().reset_index()
products_per_employee = products_per_employee.rename(columns={'quantity': 'Produtos Vendidos'})
products_per_employee = products_per_employee.sort_values(by='Produtos Vendidos', ascending=False)

product_category_data = df_tabela7.merge(df_tabela8, on='order_id')
product_category_data = product_category_data.merge(df_tabela9, on='product_id')
product_category_data = product_category_data.merge(df_tabela1, on='category_id')

products_per_category = product_category_data.groupby('category_name')['quantity'].sum().reset_index()
products_per_category = products_per_category.rename(columns={'quantity': 'Produtos Vendidos'})
products_per_category = products_per_category.sort_values(by='Produtos Vendidos', ascending=False)

product_shipper_data = df_tabela7.merge(df_tabela8, on='order_id')
product_shipper_data = product_shipper_data.merge(df_tabela11, left_on='ship_via', right_on='shipper_id')

products_per_shipper = product_shipper_data.groupby('company_name')['quantity'].sum().reset_index()
products_per_shipper = products_per_shipper.rename(columns={'quantity': 'Produtos Vendidos'})
products_per_shipper = products_per_shipper.sort_values(by='Produtos Vendidos', ascending=False)

df_tabela8['ano_mes'] = df_tabela8['order_date'].dt.to_period('M')
product_year_month_data = df_tabela7.merge(df_tabela8[['order_id', 'ano_mes']], on='order_id')

products_per_year_month = product_year_month_data.groupby('ano_mes')['quantity'].sum().reset_index()
products_per_year_month = products_per_year_month.rename(columns={'quantity': 'Produtos Vendidos'})
products_per_year_month = products_per_year_month.sort_values(by='ano_mes')

order_data4 = df_tabela8.merge(df_tabela7, on='order_id')
order_data4['total_value'] = (order_data4['quantity'] * order_data4['unit_price']) * (1 - order_data4['discount'])

product_total_revenue = order_data4.groupby('product_id')['total_value'].sum().reset_index()
product_total_quantity = order_data4.groupby('product_id')['quantity'].sum().reset_index()

top_products_info4 = product_total_revenue.merge(df_tabela9[['product_id', 'product_name']], on='product_id')
top_products_info4 = top_products_info4.merge(product_total_quantity, on='product_id')

top_products_info_sorted4 = top_products_info4.sort_values(by='total_value', ascending=False)

top10_produtos_quantidade = product_total_quantity.sort_values(by='quantity', ascending=False).head(10)
bot10_produtos_quantidade = product_total_quantity.sort_values(by='quantity', ascending=True).head(10)

top10_produtos_quantidade_nomes = product_total_quantity.merge(df_tabela9[['product_id', 'product_name']], on='product_id')
bot10_produtos_quantidade_nomes = product_total_quantity.merge(df_tabela9[['product_id', 'product_name']], on='product_id')

top10_produtos_quantidade_nomes = top10_produtos_quantidade.merge(df_tabela9[['product_id', 'product_name']], on='product_id')
bot10_produtos_quantidade_nomes = bot10_produtos_quantidade.merge(df_tabela9[['product_id', 'product_name']], on='product_id')


top10_produtos_quantidade_nomes = top10_produtos_quantidade_nomes[['product_name', 'quantity']]
bot10_produtos_quantidade_nomes = bot10_produtos_quantidade_nomes[['product_name', 'quantity']]

#print("Produtos por Empregado:")
#print(products_per_employee)
#print("Produtos por Categoria de Produtos:")
#print(products_per_category)
#print("Produtos por Shippers:")
#print(products_per_shipper)
#print("Produtos por Ano/Mês:")
#print(products_per_year_month)

#### ---- PLOT DAS TABELAS ---- ####
"""
# Dados da tabela de Produtos por Empregado
names = products_per_employee['first_name'] + ' ' + products_per_employee['last_name']
products_sold = products_per_employee['Produtos Vendidos']
plt.figure(figsize=(10, 6))
plt.bar(names, products_sold)
plt.xlabel('Funcionários')
plt.ylabel('Quantidade de Produtos Vendidos')
plt.title('Produtos Vendidos por Funcionário')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(products_sold):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Produtos por Categoria de Produtos
categories = products_per_category['category_name']
products_sold = products_per_category['Produtos Vendidos']
plt.figure(figsize=(10, 6))
plt.bar(categories, products_sold)
plt.xlabel('Categorias de Produtos')
plt.ylabel('Quantidade de Produtos Vendidos')
plt.title('Produtos Vendidos por Categoria')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(products_sold):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Produtos por Shippers
shippers = products_per_shipper['company_name']
products_sold = products_per_shipper['Produtos Vendidos']
plt.figure(figsize=(10, 6))
plt.bar(shippers, products_sold)
plt.xlabel('Transportadoras')
plt.ylabel('Quantidade de Produtos Vendidos')
plt.title('Produtos Vendidos por Transportadoras')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(products_sold):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Produtos por Ano/Mês
year_month = products_per_year_month['ano_mes'].astype(str)
products_sold = products_per_year_month['Produtos Vendidos']
plt.figure(figsize=(10, 6))
plt.plot(year_month, products_sold, marker='o')
plt.xlabel('Data')
plt.ylabel('Quantidade de Produtos Vendidos')
plt.title('Produtos Vendidos por Mês')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(products_sold):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()
"""


"""
# Dados da tabela de Pedidos por Empregado
employees = orders_per_employee['first_name'] + ' ' + orders_per_employee['last_name']
orders_count = orders_per_employee['Pedidos']
plt.figure(figsize=(10, 6))
plt.bar(employees, orders_count, color='red')
plt.xlabel('Funcionários')
plt.ylabel('Quantidade de Pedidos')
plt.title('Vendas por Funcionário')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(orders_count):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Pedidos por Categoria de Produtos
categories = orders_per_category['category_name']
orders_count = orders_per_category['Pedidos']
plt.figure(figsize=(10, 6))
plt.bar(categories, orders_count, color='red')
plt.xlabel('Categorias de Produtos')
plt.ylabel('Quantidade de Pedidos')
plt.title('Vendas por Categoria de Produtos')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(orders_count):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Pedidos por Shippers
shippers = orders_per_shipper['company_name']
orders_count = orders_per_shipper['Pedidos']
plt.figure(figsize=(10, 6))
plt.bar(shippers, orders_count, color='red')
plt.xlabel('Transportadoras')
plt.ylabel('Quantidade de Pedidos')
plt.title('Pedidos por Transportadoras')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(orders_count):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Pedidos por Ano/Mês
year_month = orders_per_year_month['ano_mes'].astype(str)  # Converta para strings
orders_count = orders_per_year_month['Pedidos']
plt.figure(figsize=(10, 6))
plt.plot(year_month, orders_count, marker='o', color='red')
plt.xlabel('Ano/Data')
plt.ylabel('Quantidade de Pedidos')
plt.title('Pedidos por Mês')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(orders_count):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Dados da tabela de Pedidos por Supplier Company Name
suppliers = orders_per_supplier['company_name']
orders_count = orders_per_supplier['Pedidos']
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(suppliers, orders_count, color='red')
for bar in bars:
    value = bar.get_width()
    ax.text(value + 1, bar.get_y() + bar.get_height() / 2, str(value), va='center')
ax.set_xlabel('Quantidade de Pedidos')
ax.set_ylabel('Fornecedores')
ax.set_title('Pedidos por Fornecedores')
ax.invert_yaxis()
plt.tight_layout()
plt.show()
"""

"""
# Dados da tabela de Clientes por Empregado
employees = customers_per_employee['first_name'] + ' ' + customers_per_employee['last_name']
customers_count_employee = customers_per_employee['Clientes']

# Criar um gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(employees, customers_count_employee, color='green')  # Definindo a cor das barras para verde

# Adicionar os valores acima das barras
for bar in bars:
    value = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, str(value), ha='center', va='bottom')

ax.set_xlabel('Funcionário')
ax.set_ylabel('Quantidade de Clientes')
ax.set_title('Clientes por Funcionário')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# Dados da tabela de Clientes por Categoria de Produtos
categories = customers_per_category['category_name']
customers_count_category = customers_per_category['Clientes']

# Criar um gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, customers_count_category, color='green')  # Definindo a cor das barras para azul

# Adicionar os valores acima das barras
for bar in bars:
    value = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, str(value), ha='center', va='bottom')

ax.set_xlabel('Categoria de Produtos')
ax.set_ylabel('Quantidade de Clientes')
ax.set_title('Clientes por Categoria de Produtos')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# Dados da tabela de Clientes por Shippers
shippers = customers_per_shipper['company_name_x']
customers_count_shipper = customers_per_shipper['Clientes']

# Criar um gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(shippers, customers_count_shipper, color='green')  # Definindo a cor das barras para laranja

# Adicionar os valores acima das barras
for bar in bars:
    value = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, str(value), ha='center', va='bottom')

ax.set_xlabel('Transportadoras')
ax.set_ylabel('Quantidade de Clientes')
ax.set_title('Clientes por Transportadoras')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# Dados da tabela de Clientes por Mês/Ano
year_month = customers_per_month['mes_ano'].astype(str)
customers_count_month = customers_per_month['Clientes']

plt.figure(figsize=(10, 6))  # Defina o tamanho da figura

# Crie um gráfico de linhas com marcadores
plt.plot(year_month, customers_count_month, marker='o', color='green')

plt.xlabel('Data')
plt.ylabel('Quantidade de Clientes')
plt.title('Clientes por Mês')
plt.xticks(rotation=45, ha='right')

# Adicione os valores acima das linhas
for i, value in enumerate(customers_count_month):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')

plt.tight_layout()
plt.show()

"""
"""
# Configurar a localização para o padrão brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Dados da tabela de Venda Líquida por Empregado
employees = employee_sales['first_name'] + ' ' + employee_sales['last_name']
sales_employee = employee_sales['Venda Líquida']
fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(employees, sales_employee, color='yellow')
for bar in bars:
    value = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, locale.currency(value, grouping=True), ha='center', va='bottom')
ax.set_xlabel('Empregado')
ax.set_ylabel('Receita Líquida')
ax.set_title('Receita Líquida por Funcionário')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Dados da tabela de Venda Líquida por Categoria de Produtos
categories = category_sales['category_name']
sales_category = category_sales['Venda Líquida']
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, sales_category, color='yellow')
for bar in bars:
    value = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, locale.currency(value, grouping=True), ha='center', va='bottom')
ax.set_xlabel('Categoria de Produtos')
ax.set_ylabel('Receita Líquida')
ax.set_title('Receita Líquida por Categoria de Produtos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Dados da tabela de Venda Líquida por Shippers
shippers = shipper_sales['company_name']
sales_shipper = shipper_sales['Venda Líquida']
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(shippers, sales_shipper, color='yellow')
for bar in bars:
    value = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, locale.currency(value, grouping=True), ha='center', va='bottom')
ax.set_xlabel('Transportadoras')
ax.set_ylabel('Receita Líquida')
ax.set_title('Receita Líquida por Transportadoras')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Dados da tabela de Venda Líquida por País
countries = country_sales['country']
sales_country = country_sales['Venda Líquida']
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(countries, sales_country, color='yellow') 
for bar in bars:
    value = bar.get_width()
    ax.text(value + 0.05 * max(sales_country), bar.get_y() + bar.get_height() / 2, locale.currency(value, grouping=True), va='center')
ax.set_xlabel('Receita Líquida')
ax.set_ylabel('País')
ax.set_title('Receita Líquida por País')
plt.tight_layout()
plt.show()

# Dados da tabela de Venda Líquida por mes
year_month = faturamento_mensal.index.astype(str)
total_sales_month = faturamento_mensal.values
plt.figure(figsize=(12, 6))  # Defina o tamanho da figura
plt.plot(year_month, total_sales_month, marker='o', color='yellow')
plt.xlabel('Mês/Ano')
plt.ylabel('Total de Vendas')
plt.title('Faturamento Mensal')
plt.xticks(rotation=45, ha='right')
for i, value in enumerate(total_sales_month):
    if i % 2 == 0:  # Posições pares terão o texto mais abaixo
        plt.text(i, value + 2000, locale.currency(value, grouping=True), ha='center', va='bottom', color='black')
    else:  # Posições ímpares terão o texto mais acima
        plt.text(i, value - 2000, locale.currency(value, grouping=True), ha='center', va='top', color='black')
plt.tight_layout()
plt.show()
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

