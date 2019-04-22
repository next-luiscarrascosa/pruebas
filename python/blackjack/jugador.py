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
    __suma = 0
    __apuesta=0.0

    def __init__(self, crupier, saldo):
        self.__is_crupier = crupier
        self.saldo = saldo

    def isCrupier(self):
        return self.__is_crupier

    def addCard(self, baraja, visible):
        new_carta = baraja.getCard()
        self.__cartas.append(new_carta)

        if(visible == True):
            if new_carta.numero in ("Sota", "Caballo", "Rey"):
                self.__suma += 10
            elif new_carta.numero != "As":
                valor = int(new_carta.numero)
                if valor > 1 and valor <11:
                    self.__suma += valor
                else:
                    raise error.ValorCartaErroneo("Excepción en 'if valor > 1 and valor <11:'", "Valor no permitido")
            elif new_carta.numero == "As":
                if self.__suma+11 > 21:
                    self.__suma += 1
                else:
                    self.__suma += 11

    def value(self):
        return self.__suma

    def apuesta(self, apuesta):
        if(self.saldo<apuesta):
            print(f"El saldo actual es de {self.saldo}, inferior a la apuesta de {apuesta}")
            return False
        else:
            self.__apuesta = apuesta
            return True

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