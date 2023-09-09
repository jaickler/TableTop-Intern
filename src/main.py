from ChatBot.ChatBot import DmIntern
import dotenv
import asyncio

async def main():
    dotenv.load_dotenv()
    intern = DmIntern()
    cont:bool = True
    
    # Main input and response loop.
    while cont:
        user_input = input("Message: ")
        if user_input.lower() == "exit":
            intern.save_graph()
            cont = False
            break
        else:
            response:str = await intern.run(user_input)
            print("\nIntern:", response, "\n")

if __name__ == "__main__":
    asyncio.run(main())