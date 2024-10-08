import pandas as pd

def convert_csv_to_arff(csv_file, arff_file):
    df = pd.read_csv(csv_file)

    # Create ARFF header
    with open(arff_file, 'w',encoding='utf-8') as f:
        f.write(f"@relation {csv_file.split('.')[0]}\n\n")
        
        # Add attribute section
        for col in df.columns:
            if df[col].dtype == 'bool':
                # Categorical attribute
                unique_values = ','.join(map(str, [True, False]))
                f.write(f"@attribute {col} {{{unique_values}}}\n")
            elif df[col].dtype == 'object':
                # Nominal attrubute
                f.write(f"@attribute {col} string\n")
            else:
                if col == 'author_id':
                    unique_values = ','.join(map(str,range(0,10)))
                    f.write(f"@attribute {col} {{{unique_values}}}\n")
                else: 
                    # Numeric attribute
                    f.write(f"@attribute {col} numeric\n")
        
        f.write("\n@data\n")
        
        # Add data section
        for _, row in df.iterrows():
            processed_values = []
            for value in row.values:
                # Replace double quotes with single quotes
                str_value = str(value).replace("\"", "'")
                
                # Check if the value contains commas; if so, wrap it in double quotes
                if isinstance(value, str):
                    str_value = f'"{str_value}"'
                
                processed_values.append(str_value)
            
            f.write(','.join(processed_values) + '\n')
# Example usage:
convert_csv_to_arff('musiccaps-public.csv', 'dataset.arff')
