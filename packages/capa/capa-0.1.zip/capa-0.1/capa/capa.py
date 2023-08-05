def check():
	print("Package Capa IPS charge correctement")
	
def affiche_colonne(x):	
	return list(x.columns)	
	
# Fonction de recherche => Si la colonne 'key1' commence par la valeur 'value1' alors on retourne l'incident 
def maskCOMMENCEPAR(df, key1, value1):
    return df[(df[key1].str.startswith(value1))]

# Fonction de recherche => Si la colonne 'key1' est égale à la valeur 'value1' alors on retourne l'incident 
def maskEGAL(df, key1, value1):
    return df[(df[key1] == value1)]

# Fonction de recherche imbriquée OU + ET
#  Si la colonne 'key1' est égale à la valeur 'value1' et la colonne 'key2' est égale à la valeur 'value2' et si la colonne 'key3' est égale à la valeur 'value3'  alors on retourne l'incident 
def maskOUET(df, key1, value1, key2, value2, key3, value3):
    return df[((df[key1] == value1) | (df[key2] == value2)) & (df[key3] == value3)]

# Fonction de recherche => si la colonne 'key1' est égale à la valeur 'value1' et la colonne 'key2' est égale à la valeur 'value2' alors on retourne l'incident  
def maskET(df, key1, value1, key2, value2):
    return df[((df[key1] == value1) & (df[key2] == value2))]

# Fonction de recherche => si la colonne 'key1' contient la valeur 'value1' alors on retourne l'incident  
def maskCONTIENT(df, key1, value1):
    return df[df[key1].str.contains(value1, case=False)]

def classification(map, df, colname, colnameVal):
	import pandas as pd
	pd.DataFrame.maskCOMMENCEPAR = maskCOMMENCEPAR
	pd.DataFrame.maskEGAL = maskEGAL
	pd.DataFrame.maskET = maskET
	pd.DataFrame.maskOUET = maskOUET
	pd.DataFrame.maskCONTIENT = maskCONTIENT	

	df = df.fillna('NULL')
	df[colname] = colnameVal


	if colname == 'TYPE INC':
		df.loc[df['Regroupement 1'] =="NETCOOL/TRAP", 'TYPE INC'] = df.ANATRAP

		df.loc[(df['Regroupement 1'] !="NETCOOL/TRAP") & (df['Regroupement 1'] == 'LOGWATCHER') & (df.ANATRAP == df.Bp2iappli), 'TYPE INC'] = df['Regroupement 1']

		df.loc[(df['Regroupement 1'] !="NETCOOL/TRAP") & (df['Regroupement 1'] == 'LOGWATCHER') & (df.ANATRAP != df.Bp2iappli), 'TYPE INC'] = df.ANATRAP

		df.loc[((df['Regroupement 1'] !="NETCOOL/TRAP") & (df['Regroupement 1'] != 'LOGWATCHER')) & ((df.ANATRAP == "SGBD") & (df['Regroupement 1'] == 'SYSTEM')), 'TYPE INC'] = df.ANATRAP

		df.loc[((df['Regroupement 1'] !="NETCOOL/TRAP") & (df['Regroupement 1'] != 'LOGWATCHER')) & ((df.ANATRAP != "SGBD") & (df['Regroupement 1'] != 'SYSTEM')) & (df.ANATRAP == "Infrastructure de regroupements des VIOs"), 'TYPE INC'] = "SYSTEM"

		df.loc[((df['Regroupement 1'] !="NETCOOL/TRAP") & (df['Regroupement 1'] != 'LOGWATCHER')) & ((df.ANATRAP != "SGBD") & (df['Regroupement 1'] != 'SYSTEM')) & (df.ANATRAP != "Infrastructure de regroupements des VIOs"), 'TYPE INC'] = df['Regroupement 1']
	
	# Boucle pemrettant la classification par Dictionnaire (map.csv)
	for i in range(len(map)-1,0,-1):
		if map.loc[i].TYPE == 'COMMENCEPAR':
			df.loc[df.maskCOMMENCEPAR(map.loc[i].COL1,map.loc[i].Val_COL1).index, colname] = map.loc[i].CAT
		if map.loc[i].TYPE == 'EGAL':    
			df.loc[df.maskEGAL(map.loc[i].COL1,map.loc[i].Val_COL1).index, colname] = map.loc[i].CAT
		if map.loc[i].TYPE == 'OUET':        
			df.loc[df.maskOUET(map.loc[i].COL1,map.loc[i].Val_COL1,map.loc[i].COL2,map.loc[i].Val_COL2,map.loc[i].COL3,map.loc[i].Val_COL3).index, colname] = map.loc[i].CAT
		if map.loc[i].TYPE == 'ET':
			df.loc[df.maskET(map.loc[i].COL1,map.loc[i].Val_COL1,map.loc[i].COL2,map.loc[i].Val_COL2).index, colname] = map.loc[i].CAT
		if map.loc[i].TYPE == 'CONTIENT':
			df.loc[df.maskCONTIENT(map.loc[i].COL1,map.loc[i].Val_COL1).index, colname] = map.loc[i].CAT	
	print('Classification OK')
	return df		


def selection_colonne(listcol, df):
	import pandas as pd
	return pd.DataFrame(df, columns=listcol)
	
def graph_camembert(df, colname):
    import pandas as pd 
    import matplotlib.pyplot as plt
    import seaborn as sb

    # Create a pie chart
    plt.pie(pd.DataFrame(df[colname].value_counts().reset_index())['Métier'],labels=pd.DataFrame(df[colname].value_counts().reset_index())['index'],autopct='%1.1f%%')

    # View the plot drop above
    plt.axis('equal')

    # View the plot
    plt.tight_layout()
    plt.show()
	
# Data Viz en barplot du nombre d'incident par "Métier"
def graph_barplot_multi(df, colname, colrupture, colwrap, xlabel, ylabel, rotation):
    import pandas as pd 
    import matplotlib.pyplot as plt
    import seaborn as sb
    g = sb.factorplot(colname,col=colrupture,data=df,kind="count",col_wrap=colwrap)
    # On définit les libellés des axes x et y
    g.set(ylabel=ylabel, xlabel=xlabel)

    # On ajoute la rotation des libellés de l'axe x pour une meilleure lisibilité (ici 90°)
    # Attention les libellés de l'axe x n'est affiché que sur le dernier graphique de la colonne (celui le plus bas)
    g.set_xticklabels(rotation=rotation)


def graph_barplot(df,colname,topn, xlabel, ylabel, rotation):
    import pandas as pd 
    import matplotlib.pyplot as plt
    import seaborn as sb

    g = sb.barplot(y=pd.DataFrame(df[colname].value_counts().reset_index()[:topn])[colname],x=pd.DataFrame(df[colname].value_counts().reset_index()[:topn])['index'])
    g.set_ylabel("Nb Incident")
    g.set_xlabel(colname)
    g.set(ylabel=ylabel, xlabel=xlabel)
	
    # On ajoute la rotation des libellés de l'axe x pour une meilleure lisibilité (ici 90°)
    for item in g.get_xticklabels():
        item.set_rotation(rotation)

    for p in g.patches:
        height = p.get_height()
        g.text(p.get_x(), height*1.02, '%.0f'%(height))	

def graph_AnalyseEvolution(df,TitreGraph,colIDIncident,colName,colDate):
    import plotly.plotly as py
    import plotly.graph_objs as go 
    from plotly import __version__
    from plotly.offline import init_notebook_mode, iplot
    from plotly.graph_objs import Scatter
    import plotly.graph_objs as go
    import plotly.tools as tls
    init_notebook_mode()
    from datetime import datetime
    import pandas_datareader 

    df['Day'] = df[colDate].dt.day
    INC2 = df[[colIDIncident,colName,colDate]].groupby([colName,colDate]).count()
    INC2 = INC2.reset_index()

    def Set_Trace(mm):
        trace = go.Scatter(x=INC2[INC2[colName] == mm][colDate], 
                           y=INC2[INC2[colName] == mm][colIDIncident],
                           name=mm,
                           fill='tonexty',

                          )
        return trace

    data = []
    for m in INC2[colName].unique():
        trace = Set_Trace(m)
        data.append(trace)


    layout = dict(
        title=TitreGraph,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            #type='date'
        ),
    )

    fig = dict(data=data, layout=layout)
    iplot(fig)	

def import_SQL(table):
    import pymysql
    pymysql.install_as_MySQLdb()
    import pandas as pd
    import mysql.connector
    from sqlalchemy import create_engine

    # Crꢴion de la connexion ࡬a base de donn꦳ MySQL
    engine = create_engine('mysql+pymysql://readonly:readonly@s00vl9963519/cmis?charset=utf8')

    # Crꢴion de la variable pour la requete SQL
    RequeteSQL = 'select * from ' + table

    # Ligne de code pour charger depuis la base MySQL et la requeteSQL
    File = pd.read_sql(RequeteSQL, engine)
    
    print('Chargement de la table MySQL : ' + table + ' OK')
    return File    

def load_multiMySQL(list):
    import pymysql
    pymysql.install_as_MySQLdb()
    import pandas as pd
    import mysql.connector
    from sqlalchemy import create_engine



    n = 0
    for i in list: 
        # Crꢴion de la connexion ࡬a base de donn꦳ MySQL
        engine = create_engine('mysql+pymysql://readonly:readonly@s00vl9963519/cmis?charset=utf8')
        
        # Crꢴion de la variable pour la requete SQL
        RequeteSQL = 'select * from ' + i

        # Ligne de code pour charger depuis la base MySQL et la requeteSQL
        Filen = pd.read_sql(RequeteSQL, engine)
        
        if  n == 0:
            File = Filen
        else:
            File = File.append(Filen, ignore_index = True)
        n = n + 1
    print('Chargement des tables MySQL OK')
    return File 



# Rꤵp곡tion des colonnes utiles et importation dans le nouveau DataFrame 
def NormalisationColumns(df):
    from string import punctuation
    
    # Remove ponctuation
    def strip_punctuation(s):
        return ''.join(c for c in s if c not in punctuation)     

    for i in df.columns:
        df.rename(columns={i: strip_punctuation(i.replace(' ',''))}, inplace=True)        
       
    return df

def LoadCSV(path, sep=';'):

    import pandas as pd
    
    df = pd.read_csv(path, sep=sep,encoding = "ISO-8859-1")

    from string import punctuation
    
    # Remove ponctuation
    def strip_punctuation(s):
        return ''.join(c for c in s if c not in punctuation)     

    for i in df.columns:
        df.rename(columns={i: strip_punctuation(i.replace(' ',''))}, inplace=True)        
    print('Chargement du fichier CSV : ' + path + ' OK')
    return df
  

def LoadXLS(path, sheetname=0, skiprows =0):

    import pandas as pd
    
    df = pd.read_excel(path, sheetname=sheetname, skiprows = skiprows)

    from string import punctuation
    
    # Remove ponctuation
    def strip_punctuation(s):
        return ''.join(c for c in s if c not in punctuation)     

    for i in df.columns:
        df.rename(columns={i: strip_punctuation(i.replace(' ',''))}, inplace=True)        
    print('Chargement du fichier XLS : ' + path + ' OK')
    return df    
    
def FileSize(df):
    print('Nombre de ligne du fichier : ' + str(df.shape[0]))
    print('Nombre de colonne du fichier : ' + str(df.shape[1]))    


