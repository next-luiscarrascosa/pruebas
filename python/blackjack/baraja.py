"""
Módulo que contiene las clases "Carta" y "Baraja"
"""
from random import shuffle

class Carta:
    """
    Carta tiene un número, un palo
    """

    def __init__(self, numero, palo):
        self.numero = numero
        self.palo = palo

    def __str__(self):
        return f"{self.numero} de {self.palo}"

    def __eq__(self, other):
        return self.numero==other.numero and self.palo==other.palo

    def setVisible(self):
        self.visible = True

    def isVisible(self):
        return self.visible

class Baraja:
    """
    Baraja de cartas
    """
    def __init__(self):
        self.__baraja = []
        self.palos = ["Espadas", "Bastos", "Copas", "Oros"]
    
        for palo in self.palos:
            self.__baraja.append(Carta("As", palo))

            for x in range(2, 11):
               self.__baraja.append(Carta(x, palo))

            self.__baraja.append(Carta("Sota", palo))
            self.__baraja.append(Carta("Caballo", palo))
            self.__baraja.append(Carta("Rey", palo))

        print(f"Creadas las {len(self.__baraja)} cartas de la baraja")

    def barajar(self):
        shuffle(self.__baraja)

    def getCard(self):
        return self.__baraja.pop(0)

    def restantes(self):
        return len(self.__baraja)

    def __str__(self):
        baraja_str = "\n".join([carta.__str__() for carta in self.__baraja])
        return f"Quedan {len(self.__baraja)} cartas\n{baraja_str}"