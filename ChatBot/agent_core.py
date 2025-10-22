import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults

# Cargar variables de entorno
load_dotenv()

# 1. Inicializar el LLM
# Usamos Llama 3 vía Groq. Es rápido y potente.
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.3
)

# 2. Definir Herramientas (Opcional pero recomendado)
# El agente podrá decidir si usar esta herramienta o no.
# NOTA: Requiere TAVILY_API_KEY en el .env
# tools = [TavilySearchResults(max_results=3)]
# Para un taller más simple, podemos empezar sin herramientas:
tools = []

# 3. Crear el Prompt
# Este prompt guía al agente.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente de IA útil. Responde al usuario de forma concisa. "
     "Si usas una herramienta, resume los resultados."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Crear el Agente
# create_tool_calling_agent es el estándar moderno
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. Crear el Ejecutor del Agente
# El Executor maneja el 'loop' de Pensar -> Actuar -> Observar
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # Poner en True para ver 'pensamientos' del agente
)

# Función para invocar al agente
def invoke_agent(user_input, chat_history_messages):
    """
    Invoca al agente con la entrada del usuario y el historial.
    """
    return agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history_messages
    })