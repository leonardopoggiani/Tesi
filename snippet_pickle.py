with open('dati_riorganizzati.pkl', 'wb') as output:
  pickle.dump(df_list, output, pickle.HIGHEST_PROTOCOL)
