from dotenv import load_dotenv
import os

load_dotenv()
mnemonic = os.getenv("MNEMONIC")

print(mnemonic)