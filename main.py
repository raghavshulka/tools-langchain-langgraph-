from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.8)



prompt = PromptTemplate(
    template='tell me about a{topic}',
    input_variables=['topic']
)

prompt1 = PromptTemplate(
    template='Generate 5 short question  from the following topic \n {topic}',
    input_variables=['topic']
)

prompt3 = PromptTemplate(
    template='Merge the provided notes and quiz into a single document \n notes -> {essay} and quiz -> {points}',
    input_variables=['essay', 'points']
)


parser = StrOutputParser()

parallel = RunnableParallel({
    'essay': prompt | llm | parser ,
    'points': prompt1 | llm | parser
})

mergeChain = prompt3 | llm | parser

chain = parallel | mergeChain

result = chain.invoke({'topic':'what is quantum-computing'})

print(result)
chain.get_graph().print_ascii()