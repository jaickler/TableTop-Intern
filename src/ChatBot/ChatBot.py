import openai
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate, Prompt
from langchain.memory import ConversationKGMemory, CombinedMemory, ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.language_model import BaseLanguageModel
from langchain.graphs import NetworkxEntityGraph
import dotenv
import asyncio

class DmIntern:

    # Class Variables
    graph_path:str
    graph:NetworkxEntityGraph
    llm:BaseLanguageModel
    kgmemory:ConversationKGMemory
    conv_memory:ConversationSummaryBufferMemory
    comb_memory:CombinedMemory
    chain:ConversationChain
    template:Prompt

    def __init__(self,
                 graph_path:str=None,
                 llm:BaseLanguageModel=ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=dotenv.get_key(dotenv_path="C:\\Users\\jaick\\source\\repos\\TableTop Intern\\.env", key_to_get="OPENAI_API_KEY"))) -> None:
        """Creates new DmIntern object.
        
        Keyword arguments:

        graph_path:str -- optional path to knowledge graph file. Defaults to env var.
        llm:BaseLanguageMoedl -- optional llm for intern to use. Defaults to gpt-3.5-turbo-16k.

        Return: None
        """
        # load env vars from .env file
        dotenv.load_dotenv()
        
        self.template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

                        Relevent Info:
                        {history}
                        Current conversation:
                        {chat_history_lines}
                        Human: {input}
                        AI:"""

        self.prompt = PromptTemplate(
                input_variables=["history", "input", "chat_history_lines"],
                template=self.template,
                )

        self.load_graph(graph_path)
        self.llm = llm
        self.kgmemory=ConversationKGMemory(llm=self.llm, kg=self.graph, memory_key="history", input_key="input")
        self.conv_memory = ConversationSummaryBufferMemory(llm=self.llm, memory_key="chat_history_lines", input_key="input")
        self.comb_memory = CombinedMemory(memories=[self.conv_memory, self.kgmemory])
        self.chain = ConversationChain(llm=self.llm, memory=self.comb_memory, prompt=self.prompt)

    def __del__(self):
        self.save_graph()

    def load_graph(self, path:str=None) -> None:
        """Loads the knowledge graph from a file or creates one.
        
        Keyword arguments:
        path:str -- optional path to knowledge graph. Defaults to env var.
        Return: None
        """
        
        try:
            if path == None:
                self.graph_path = dotenv.get_key(dotenv_path="C:\\Users\\jaick\\source\\repos\\TableTop Intern\\.env", key_to_get="NETWORX_GRAPH_PATH")
            else:
                self.graph_path = path
            self.graph = NetworkxEntityGraph.from_gml(gml_path=self.graph_path)
        except:
            self.graph = NetworkxEntityGraph()

    async def run(self, input:str):
        return await self.chain.arun(input)
    
    def save_graph(self) -> None:
        self.graph.write_to_gml(path=self.graph_path)
        return


async def main():
    dotenv.load_dotenv()
    intern = DmIntern()

    print(await intern.run("Here is some info for a dnd npc: Reginald Archibald Braddock is an aged human man with an air of authority that matches his high social standing. His fine white hair is combed back perfectly, suspended by the round, wire-rimmed glasses perched on his long hooked nose. He usually sports a tweed waistcoat over his white shirt, carrying a scroll and a thin scribing board in hand to keep track of his dealings."))

    print(await intern.run("Tell me about Mr. Braddock"))

if __name__ == "__main__":
    asyncio.run(main())