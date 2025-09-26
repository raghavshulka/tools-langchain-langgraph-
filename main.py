from typing import Literal
from dotenv import load_dotenv
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

class Feedback(BaseModel):
    sentiment: Literal['advantage', 'disadvantage'] = Field(description="Classify as advantage or disadvantage")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.8)

parser2= PydanticOutputParser(pydantic_object=Feedback)

classifier_prompt = PromptTemplate(
    template="Classify the following text as either advantage or disadvantage:\n\n{topic}\n{format_instruction}",
    input_variables=["topic"],
    partial_variables={"format_instruction": parser2.get_format_instructions()}
)

classifier_chain = classifier_prompt | llm | parser2 

advantage_prompt = PromptTemplate(
    template="Write advantages of {topic}",
    input_variables=["topic"]
)

disadvantage_prompt = PromptTemplate(
    template="Write disadvantages of {topic}",
    input_variables=["topic"]
)

parser = StrOutputParser()

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "advantage", advantage_prompt | llm | parser),
    (lambda x: x.sentiment == "disadvantage", disadvantage_prompt | llm | parser),
    RunnableLambda(lambda _: "Could not classify sentiment.")
)

chain = classifier_chain | branch_chain

result = chain.invoke({"topic": "what is advantage quantum-computing"})
print(result)

chain.get_graph().print_ascii()
