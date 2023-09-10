from ChatBot.ChatBot import TTRPGIntern
import dotenv
import asyncio
import pathlib

async def main():
    dotenv.load_dotenv()
    intern = TTRPGIntern()
    cont:bool = True
    
    # Main input and response loop.
    while cont:
        user_input = input("Message: ")
        if user_input.lower() == "exit":
            intern.save_graph()
            cont = False
            break
        elif user_input.lower() == "file":
            await intern.parse_file(input("File Path: "))
        else:
            response:str = await intern.run(user_input)
            print("\nIntern:", response, "\n")

if __name__ == "__main__":
    asyncio.run(main())