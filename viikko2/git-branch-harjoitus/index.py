from erotus import erotus
from logger import logger
from summa import summa

logger("aloitetaan")

x = int(input("luku 1: "))
y = int(input("luku 2: "))
print(f"{summa(x, y)}")
print(f"{erotus(x, y)}")

logger("lopetetaan")
