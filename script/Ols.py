# %% [markdown]
# # Relação entre desempenho escolar e nível sócioeconômico

# %% [markdown]
# Código para instalar o pacote "basedosdados" no computador

# %%
#!pip install basedosdados

# %%
#!pip install -U sidrapy

# %%
#!pip install python-docx

# %%
from docx import Document
import sidrapy
import basedosdados as bd
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from numpy import NaN
from sklearn import linear_model
from scipy import stats

# %%
#bd.list_datasets()

# %%
idesp = bd.read_table(dataset_id='br_sp_seduc_idesp',
                   table_id='escola',
                   billing_project_id="projetoapp-340617") #No campo "PROJECT-ID" vc coloca o ID de seu projeto no google cloud

# %%
idesp

# %%
idesp = idesp[idesp["ano"] == 2018]

# %%
idesp

# %%
idesp = idesp.reset_index()

# %%
idesp = idesp.drop(['index', 'ano', 'id_municipio', 'id_escola_sp'], axis=1)

# %%
idesp

# %%
nivel_sociecon = bd.read_table(dataset_id='br_sp_seduc_inse',
                               table_id='escola',
                               billing_project_id="projetoapp-340617")

# %%
nivel_sociecon

# %%
nivel_sociecon = nivel_sociecon.drop(["id_municipio", "rede", "diretoria", "id_escola_sp"], axis=1)

# %%
nivel_sociecon

# %%
idesp.info()

# %%
nivel_sociecon.info()

# %%
cols_int = ["id_escola"]

idesp[cols_int] = idesp[cols_int].astype(int)

# %%
cols_int = ["id_escola"]

nivel_sociecon[cols_int] = nivel_sociecon[cols_int].astype(int)

# %%
idesp.info()

# %%
nivel_sociecon.info()

# %%
df = idesp.merge(nivel_sociecon, left_on="id_escola", right_on="id_escola", how="outer", indicator=True)
df = df[df["_merge"] == 'both']
df = df.drop(['_merge'], axis=1)
df

# %%
#ver as tabelas
#bd.get_table_columns(
    #dataset_id='br_ibge_pib',
    #table_id='municipio'
    #)

# %%
#ver o tamanho da tabela
#bd.get_table_size(dataset_id="br_ibge_pib", 
              #table_id="municipio", 
              #billing_project_id = 'projetoapp-340617')

# %%
df.info()

# %%
#Quais foram as escolas de sp com maior nível sócio-econômico?
#df[df["ano"] == 2019]`: Filtra apenas os registros com 2019 na coluna "ano".
#sort_values(by="nivel_socio_economico", ascending=False)`: Ordena os resultados pela coluna "nivel_socio_economico" de forma descendente.
#head(10): Mostra só os dez primeiros resultados.


df.sort_values(by="nivel_socio_economico", ascending=False).head(10) 

# %%
df.tail()

# %%
fig = px.scatter(
    df.sort_values(by="nivel_socio_economico", ascending=False, ignore_index=True).loc[1:], #Classifica os valores
    x="nivel_socio_economico", #Coluna que ficará no eixo X
    y="nota_idesp_em", #Coluna que ficará no eixo Y
    title="Nota IDESP para anos do ensino médio VS Nível socioeconômico da escola", #Título do gráfico
    trendline="ols", #linha de tendência
    hover_name="id_escola", hover_data=["nivel_socio_economico", "nota_idesp_em"] # Configuramos os campos que irão aparecer ao passar o mouse sobre os pontos
)

# Outro jeito de redefinir titulos dos eixos...
fig.update_layout(dict(xaxis=dict(title="Nível socioeconômico da escola"),
                       yaxis=dict(title="Nota IDESP para anos do ensino médio")))

fig.show()

# %%
results = px.get_trendline_results(fig)

results.px_fit_results.iloc[0].summary()

# %%
y = df['nota_idesp_em']
x = df['nivel_socio_economico']
x = sm.add_constant(x)

# %%
model = sm.OLS(y, x, missing='drop')

# %%
results = model.fit()
predictions = results.predict(x)
print(results.summary())

# %%



