from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent


load_dotenv()

class DocSearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=DocSearchResponse)
prompt = ChatPromptTemplate.from_messages(
    [
       ( "system",
        """
        You are doc based search agent. You will be provided
        context from the documents and you will use only those to generate a response.
        Wrap the output in this format and provide no other text\n{format_instructions}

        """),
         ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_agent(
    model="openai:gpt-4o-mini",
    system_prompt="" \
    "You are a doc based search agent. You will be provided context from the documents and you will use only those to generate a response. Wrap the output in this format and provide no other text\n{format_instructions}",
    tools=[],
    response_format=DocSearchResponse
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "what information do you have in the docs"
        }
    ]
}
    
)
structured_response = response["structured_response"]
print(structured_response)
