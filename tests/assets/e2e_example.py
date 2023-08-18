from langchain.schema import Document

from opencopilot import OpenCopilot

copilot = OpenCopilot()
copilot.add_prompt("tests/assets/e2e_example_prompt.txt")
copilot.add_local_files_dir("tests/assets/e2e_example_data")


@copilot.data_loader
def e2e_data_loader():
    return [
        Document(
            page_content="Estonian last president was Kersti Kaljulaid",
            metadata={"source": "internet"}
        )
    ]


copilot()
