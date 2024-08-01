import os
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
	# Load the dataset from a JSON file
	data_file = os.path.join(os.path.dirname(__file__), 'data.json')
	ragas_dataset = load_dataset('json', data_files=data_file)
	data = ragas_dataset['train']

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

	 # Global Result
	df = pd.DataFrame(result, index=[0])
	res_df = df.transpose()
	res_df.columns = ["Result"]

	# Result by question
	result_df = result.to_pandas()

	return res_df, result_df