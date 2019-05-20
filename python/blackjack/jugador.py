"""
Módulo que contiene la clase "Jugador"
"""
import baraja
import error

class Jugador:
    """
    Clase jugador
    """
    __cartas = []
    __is_crupier = False
    __apuesta=0.0
    __valores1 = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Sota": 10, "Caballo": 10, "Rey": 10, "As": 1}
    __valores11 = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Sota": 10, "Caballo": 10, "Rey": 10, "As": 11}

    def __init__(self, crupier, saldo, nombre):
        self.__is_crupier = crupier
        self.saldo = saldo
        self.nombre = nombre

    def isCrupier(self):
        return self.__is_crupier

    def viewNotVisibleCard(self):
        return [carta for carta in self.__cartas if carta.isVisible() == False]

    def addCard(self, baraja, visible):
        new_carta = baraja.getCard()
        new_carta.setVisible(visible)
        self.__cartas.append(new_carta)

    def value(self):
        suma = sum([self.__valores11[carta.numero] for carta in self.__cartas if carta.isVisible() == True])
        if(suma>21):
            suma = sum([self.__valores1[carta.numero] for carta in self.__cartas if carta.isVisible() == True])        

        return suma

    def apuesta(self, apuesta):
        if(self.saldo<apuesta):
            print(f"El saldo actual es de {self.saldo}, inferior a la apuesta de {apuesta}")
            return False
        else:
            self.__apuesta = apuesta
            return True

    def empate(self):
        self.__apuesta = 0.0

    def liquidar_apuesta(self, resultado):
        '''
        Resultados posibles: 'S', 'S_BLACKJACK', 'N', 'N_BLACKJACK'
        '''
        if "S" == resultado:
            self.saldo+= self.__apuesta
        elif "S_BLACKJACK" == resultado:
            self.saldo+=(self.__apuesta*1.5)
        elif "N_BLACKJACK" == resultado:
            self.saldo-=(self.__apuesta*1.5)
        elif "N" == resultado:
            self.saldo-=self.__apuesta
        else:
            raise error.CodigoVictoriaErroneo("liquidar_apuesta(self, victoria)", f"Resultado {resultado}, pero los valores permitidos son 'S', 'S_BLACKJACK', 'N', 'N_BLACKJACK'")

        self.__apuesta = 0.0