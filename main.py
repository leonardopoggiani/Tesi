import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# 1) caricare il csv come dataframe e mettere ad 1 le i valori della colonna "Anomalous" delle giornate riportate nella
# tabella del documento docx in allegato.

# apertura del file csv tramite costrutto with che ne gestisce la chiusura in automatico

csv_path = 'C:/Users/leona/OneDrive/Desktop/Tesi/timeSeries2015HotspotD.csv'
with open(csv_path) as csv_file:
    # lettura del file csv (comma separeted values) con delimitatore la virgola
    csv_reader = csv.reader(csv_file, delimiter=',')

    # creo dataframe leggendo csv
    df = pd.read_csv(csv_path)

    # apro il file excel con le tabelle word convertite
    excel_path = 'C:/Users/leona/OneDrive/Desktop/Tesi/doc-convertiti.xlsx'

    # ottengo le anomalie divise per cluster omettendo la descrizione dell'anomalia
    cluster0 = pd.read_excel(excel_path, sheet_name='Cluster0', usecols=['Data', 'Cluster'])
    cluster1 = pd.read_excel(excel_path, sheet_name='Cluster1', usecols=['Data', 'Cluster'])
    cluster2 = pd.read_excel(excel_path, sheet_name='Cluster2', usecols=['Data', 'Cluster'])

    # creo un dataframe per ogni cluster
    cluster0["Data"] = pd.to_datetime(cluster0["Data"])
    cluster1["Data"] = pd.to_datetime(cluster1["Data"])
    cluster2["Data"] = pd.to_datetime(cluster2["Data"])

    # itero per riga e colonna
    for i, j in df.iterrows():
        for k in cluster0["Data"]:
            if k.day == j['Day'] and k.month == j['Month'] and j['Cluster'] == 0:
                df.at[i, 'Anomalous'] = 1

        for k in cluster1["Data"]:
            if k.day == j['Day'] and k.month == j['Month'] and j['Cluster'] == 1:
                df.at[i, 'Anomalous'] = 1

        for k in cluster2["Data"]:
            if k.day == j['Day'] and k.month == j['Month'] and j['Cluster'] == 2:
                df.at[i, 'Anomalous'] = 1

    # 2) Salvare su csv il dataframe risultante dal punto 1
    df.to_csv('out1.csv')

# 3) Eliminare dal dataframe (risultante dal punto 1) tutte le righe con Anomalous a 1

out1_path = 'C:/Users/leona/PycharmProjects/analisi_dataframe/out1.csv'
with open(out1_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    df = pd.read_csv(out1_path)

    for i, j in df.iterrows():
        if df.at[i, 'Anomalous'] == 1:
            df.drop(i, inplace=True)

    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)

    # 4) Salvare su csv il dataframe risultante dal punto 3
    df.to_csv('out2.csv', index=False)

out2_path = 'C:/Users/leona/PycharmProjects/analisi_dataframe/out2.csv'
with open(out2_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    df = pd.read_csv(out2_path)

    target_cols = ['Cluster']
    data_cols = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14',
                'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

    X = df[data_cols]
    Y = df[target_cols]

    X, y = make_classification(n_samples=328)

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(max_depth=2, random_state=0)

    clf.fit(X, y)

    Y_pred = clf.predict(X)

    print("Precisione:", clf.score(X, Y, sample_weight=None))

