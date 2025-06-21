import typer
from typing import Optional,List

from phi.assistant import Assistant
from phi.storage.assistant.postgres import PGAssistantStorage
from phi.knowledge.pdf import PDFURLKnowledgeBase
from phi.vectordb.pgvector import PGVector2

from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# os.emviron["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

knowledge_base = PDFURLKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/thai_recipes.pdf"],
    vector_db=PGVector2(
        collection_name="recipes",
        db_url=DB_URL
    )
)

# knowledge_base.load()
# storage=PGAssistantStorage(
#         table_name="pdf_assistant",
#         db_url=DB_URL
#     )

knowledge_base.load(
    storage=PGAssistantStorage(
        table_name="pdf_assistant",
        db_url=DB_URL
    )
)
    
def pdf_assistant(
    new: bool = False,
    user: str = "user"
) -> None:
    assistant = Assistant(
        run_id="pdf_assistant",
        user_id=user,
        knowledge_base=knowledge_base,
        storage=PGAssistantStorage(
            table_name="pdf_assistant",
            db_url=DB_URL
        ),
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True
    )

    if new or not assistant.run_id:
        assistant.run_id = "pdf_assistant"
    
    assistant.start()
    assistant.cli(markdown=True)

"""
def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]
    
    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        # Show toolcalls in the response
        show_tool_calls=True,
        # Enable the assistant to search the knowledge base
        search_knowledge=True,
        # Enable the assistant to read chat history
        read_chat_history=True
    )
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")
    assistant.cli(markdown=True)
"""

if __name__ == "__main__":
    import typer
    typer.run(pdf_assistant)