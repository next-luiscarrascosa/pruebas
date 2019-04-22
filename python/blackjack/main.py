"""
Juego de Blackjack en Python 3
Jugador humano contra programa que hace de crupier (52)
Se apuesta el principio de cada juego si se va a ganar o no
Hay una cuenta con dinero para apuestas

1. Crupier con dos cartas, una boca arriba y otra boca abajo
2. Humano con dos cartas boca arriba y empieza primero. Si con las dos cartas iniciales saca 21 la jugada es "Blackjack" y se paga a 1,5 la apuesta
3. El objetivo es acercarse mas a 21. Solo cuentan las cartas boca arriba
4. Posibles acciones: "Otra" para coger otra carta y "Paro" para plantarse
5. Si el jugador se pasa de 21 pierde y el crupier recoge el dinero de la apuesta
6. El crupier está obligado a pedir carta hasta superar al jugador. Si se pasa el jugador gana
7. Sota, caballo y rey cuentan como 10
8. Ases cuentan como 11 siempre que no se pase de 21. Si se pasa contará como 1
"""

import baraja, jugador

# Creación de jugadores
saldo_inicial = 2000.0
jugador_humano = jugador.Jugador(False, saldo_inicial)
crupier = jugador.Jugador(True, saldo_inicial)

# Creación de baraja
new_baraja=baraja.Baraja()

# ¿Saldo disponible para apostar?
while(True):
    try:
        apuesta=float(input("Jugador, ingrese su apuesta: "))
    except ValueError:
        print(f"\nApuesta {apuesta} errónea, inténtelo otra vez")
    else:
        retorno1 = jugador_humano.apuesta(apuesta)
        retorno2 = crupier.apuesta(apuesta)

        if(retorno1==True or retorno2==True):
            print(f"\nAceptada la apuesta de {apuesta}")
            break
        else:
            print(f"\nNo cuenta con el saldo necesario para cubir la apuesta de {apuesta}. Inténtelo otra vez")

# Barajar
new_baraja.barajar()
print(new_baraja.__str__())
# Reparto de cartas

# ¿Blackjack del crupier?

# ¿Blackjack del jugador?

# Turno del jugador

# Turno del crupier

# Resolución de la apuesta

# ¿Volver a jugar?