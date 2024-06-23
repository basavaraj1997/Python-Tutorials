def process_group(doc_table: pd.DataFrame):
    def is_bad_value(value):
        return pd.isna(value) or value == '' or value == ' '
    
    mask = doc_table.map(is_bad_value)
    df_cleaned_rows = doc_table[~mask.all(axis=1)]
    doc_table = df_cleaned_rows.loc[:, ~mask.all(axis=0)]  
    
    result = []
    group=pd.DataFrame()
    group=doc_table.copy()
    
    if len(group.columns)>=3:
        col=0
        is_last_column = False
        for i in range(0,len(group.columns),1):
            result=[]
            first_Columns = group.iloc[:, :col].copy()
            chunk = group.iloc[:, col:col+3].copy()
            remaining_columns = group.iloc[:, col+3:].copy()
            if len(chunk.columns)<3:
                is_last_column = True
                first_Columns = group.iloc[:, :col-1].copy()
                chunk = group.iloc[:, col-1:col-1+3].copy()
             
            for j, row in enumerate(chunk.values):
                if pd.isna(row[0]) or row[0] == '':
                    new_row=first_Columns.iloc[j].values.tolist()
                    new_row.extend([row[1], row[2]])
                    new_row.extend(remaining_columns.iloc[j].values.tolist())
                    result.append(new_row)
                    continue

                if pd.isna(row[1]) or row[1] == '':
                    new_row=first_Columns.iloc[j].values.tolist()
                    new_row .extend([row[0], row[2]])
                    new_row.extend(remaining_columns.iloc[j].values.tolist())
                    result.append(new_row)
                    continue

                if pd.isna(row[2]) or row[2] == '':
                    new_row=first_Columns.iloc[j].values.tolist()
                    new_row.extend( [row[0], row[1]])
                    new_row.extend(remaining_columns.iloc[j].values.tolist())
                    result.append(new_row)
                    continue
                else:
                    col+=1
                    break
           
            if is_last_column:
                break
            group=pd.DataFrame(result)
            col+=1
    return result
