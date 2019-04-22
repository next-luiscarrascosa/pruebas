import unittest
import baraja
import jugador

class Tester(unittest.TestCase):
    
    def test_creacion_baraja(self):
        print("creacion_baraja")

        new_baraja=baraja.Baraja()
        self.assertEqual(new_baraja.restantes(), 52, "No están las 52 cartas")

    def test_creacion_baraja_2(self):
        print("creacion_baraja_2")

        new_baraja=baraja.Baraja()
        print(new_baraja.__str__())
        
        print("****************************************")
        
        new_baraja.barajar()
        print(new_baraja.__str__())

        self.assertEqual(True, True, "Esto es solo para probar la vista de la baraja")

    def test_barajar(self):
        print("barajar")

        new_baraja_1=baraja.Baraja()
        primera_1 = new_baraja_1.getCard()
        print(primera_1.__str__)

        new_baraja_2=baraja.Baraja()
        new_baraja_2.barajar()
        primera_2 = new_baraja_2.getCard()
        print(primera_2.__str__)

        self.assertNotEqual(primera_1, primera_2, "No se ha barajado bien!")
    
    def test_apuesta(self):
        saldo_inicial = 1000.0
        apuesta = 1050.0
        
        jugador_humano = jugador.Jugador(False, saldo_inicial)
        
        retorno = jugador_humano.apuesta(apuesta)
        print(f"Retorno apuesta: {retorno}")

        self.assertEqual(retorno, False, "No tenía dinero para apostar esa cantidad!!!")
        
    def test_apuesta_S(self):
        saldo_inicial = 1000.0
        apuesta = 50.0
        
        jugador_humano = jugador.Jugador(False, saldo_inicial)
        jugador_humano.apuesta(apuesta)

        jugador_humano.liquidar_apuesta("S")

        self.assertEqual(jugador_humano.saldo, saldo_inicial+apuesta, "Apuesta S liquidada incorrectamente")

    def test_apuesta_N(self):
        saldo_inicial = 1000.0
        apuesta = 50.0
        
        jugador_humano = jugador.Jugador(False, saldo_inicial)
        jugador_humano.apuesta(apuesta)

        jugador_humano.liquidar_apuesta("N")

        self.assertEqual(jugador_humano.saldo, saldo_inicial-apuesta, "Apuesta N liquidada incorrectamente")

    def test_apuesta_S_BLACKJACK(self):
        saldo_inicial = 1000.0
        apuesta = 50.0
        
        jugador_humano = jugador.Jugador(False, saldo_inicial)
        jugador_humano.apuesta(apuesta)

        jugador_humano.liquidar_apuesta("S_BLACKJACK")

        self.assertEqual(jugador_humano.saldo, saldo_inicial+(apuesta*1.5), "Apuesta S_BLACKJACK liquidada incorrectamente")

    def test_apuesta_N_BLACKJACK(self):
        saldo_inicial = 1000.0
        apuesta = 50.0

        jugador_humano = jugador.Jugador(False, saldo_inicial)
        jugador_humano.apuesta(apuesta)

        jugador_humano.liquidar_apuesta("N_BLACKJACK")

        self.assertEqual(jugador_humano.saldo, saldo_inicial-(apuesta*1.5), "Apuesta S_BLACKJACK liquidada incorrectamente")

    def test_contabilidad_apuesta_S(self):
        saldo_inicial = 1000.0
        apuesta = 50.0

        jugador_humano = jugador.Jugador(False, saldo_inicial)
        crupier = jugador.Jugador(True, saldo_inicial)
         
        jugador_humano.apuesta(apuesta)
        crupier.apuesta(apuesta)

        jugador_humano.liquidar_apuesta("S")
        crupier.liquidar_apuesta("N")

        self.assertEqual(jugador_humano.saldo + crupier.saldo, 2.0*saldo_inicial, "No cuadra, falta pasta")

    def test_contabilidad_apuesta_S_BLACKJACK(self):
        saldo_inicial = 1000.0
        apuesta = 50.0

        jugador_humano = jugador.Jugador(False, saldo_inicial)
        crupier = jugador.Jugador(True, saldo_inicial)
         
        jugador_humano.apuesta(apuesta)
        crupier.apuesta(apuesta)

        jugador_humano.liquidar_apuesta("S_BLACKJACK")
        crupier.liquidar_apuesta("N_BLACKJACK")

        self.assertEqual(jugador_humano.saldo + crupier.saldo, 2.0*saldo_inicial, "No cuadra, falta pasta")



if __name__ == '__main__':
    unittest.main()