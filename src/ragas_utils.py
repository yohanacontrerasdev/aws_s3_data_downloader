import pandas as pd
from datasets import load_dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
    answer_correctness,
    answer_similarity
)

def get_evaluation():
    ragas_dataset = load_dataset('json', data_files='data.json')
    data = ragas_dataset['train']
    #print("-------- DATA ------------")
    #print(data)

    # Metrics
    metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall,
        answer_correctness,
        answer_similarity
    ]

    # Evaluation
    result = evaluate(
    data,
    metrics=metrics,
    raise_exceptions=False
    )

    # Resultado Global
    #print(result)
    df = pd.DataFrame(result, index=[0])
    res_df = df.transpose()
    res_df.columns = ["Result"]
    #st.dataframe(res_df)

    # Resultado por pregunta
    result_df = result.to_pandas()
    return res_df

result = get_evaluation()
print(result)