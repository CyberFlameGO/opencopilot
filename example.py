from typing import List

from langchain.schema import Document

from opencopilot import OpenCopilot

copilot = OpenCopilot()
# copilot.add_prompt("prompt_template.txt")
copilot.add_local_files_dir("data")


@copilot.data_loader
def my_data() -> List[Document]:
    return [Document(
        page_content="Kristjan is from Latvia and is a frontend developer",
        metadata={"source": "internet"}
    )]


copilot()
