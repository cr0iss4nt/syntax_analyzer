import pandas as pd
import io

def export_to_excel(analysis):
    df = pd.DataFrame(analysis, columns=["Слово", "Часть речи", "Зависимость", "Родитель", "Часть речи родителя"])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output