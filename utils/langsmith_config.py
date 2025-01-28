from langsmith import Client

def setup_langsmith(project_name: str, enable_tracing: bool = True):
    """
    LangSmith の設定を行う

    Args:
        project_name (str): プロジェクト名
        enable_tracing (bool): トレーシングを有効にするかどうか

    Returns:
        Client: LangSmith クライアントインスタンス
    """
    import os

    if enable_tracing:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"

    os.environ["LANGCHAIN_PROJECT"] = project_name

    client = Client()
    # Create project if it doesn't exist
    if not client.has_project(project_name):
        client.create_project(
            project_name=project_name,
            description="RAG application for PDF question answering"
        )

    return client
