import pandas as pd
import io

def export_to_excel(syntactic_analysis, semantic_analysis=None):
    df_syn = pd.DataFrame(syntactic_analysis, columns=[
        "Слово", "Часть речи", "Зависимость", "Родитель", "Часть речи родителя"
    ])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_syn.to_excel(writer, sheet_name="Синтаксический анализ", index=False)

        if semantic_analysis is not None:
            df_sem = pd.DataFrame(semantic_analysis, columns=["Сущность", "Тип"])
            df_sem.to_excel(writer, sheet_name="Семантический анализ", index=False)

    output.seek(0)
    return output