
# OpenCopilot back-end

To see a development setup guide, please visit the main README in the root of the project.

Below is detailed information on how to run and setup evaluation manually, i.e. without using the `opencopilot` CLI.

### Evaluation

There are two major components of opencopilot: **retrieval** and **generation**. You can evaluate either one of those in isolation, or the copilot as a whole.

Currently you can evaluate retrieval or the copilot as a whole.

**Evaluating retrieval on auto-generated examples**

Without doing the difficult work of coming up with test examples manually, you can auto-generate examples for evaluating retrieval, using GPT-4.

1. Auto-generate a retrieval dataset by running `python scripts/generate_eval_questions.py`. It will be saved within your copilot config dir as `eval_data/retrieval_auto.json`. This only needs to be done once, or whenever your ingested document set significantly changes and you want to re-generate the questions.
1. Run evaluation against this dataset: `python scripts/eval_retrieval.py --dataset_path ../copilots/{copilot_name}/eval_data/retrieval_auto.json`.

When finished, the script will print the average precision and recall across all examples. For more options, see the `--help` flag.

**Evaluating retrieval on your own examples**

1. Add some evaluation examples into `../copilots/{copilot_name}/eval_data/retrieval_human.json`.
1. Run `python scripts/eval_retrieval.py` -- the script will use the file you just edited by default as the dataset.

When finished, the script will print the average precision and recall across all examples. For more options, see the `--help` flag.

**Evaluating end-to-end on your own examples**

1. Add some evaluation examples into `../copilots/{copilot_name}/eval_data/endtoend_human.json`.
1. Run `python scripts/eval_endtoend.py` -- the script will use the file you just edited by default as the dataset.

When finished, the script will print the average grade. For more options, see the `--help` flag.




