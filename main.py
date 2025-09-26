from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.8)


prompt = PromptTemplate(
    template='tell me about a{topic}',
    input_variables=['topic']
)


parser = StrOutputParser()


chain = prompt | llm | parser


result = chain.invoke({'topic':'python language'})

print(result)


chain.get_graph().print_ascii()