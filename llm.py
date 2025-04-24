from agno.models.azure.openai_chat import AzureOpenAI
from openai import AsyncAzureOpenAI

# from openai import AsyncAzureOpenAI
from configuration import config

client = AsyncAzureOpenAI(
    azure_deployment=config.AZURE_DEPLOYMENT_NAME,
    api_version=config.AZURE_API_VERSION,
    api_key=config.AZURE_OPENAI_API_KEY,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    timeout=300,
)

model = AzureOpenAI(id=config.AZURE_DEPLOYMENT_NAME, async_client=client)
