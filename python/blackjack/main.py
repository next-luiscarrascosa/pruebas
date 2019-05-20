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

def printState(jugador, index):
    print (f"{jugador.nombre} tiene {jugador.saldo}")
    print (f"{jugadores[index - 1].nombre} tiene {jugadores[index - 1].saldo}")

def reviseGame(jugador, tipoVictoria, tipoDerrota):
    if jugador.value()==21:
        index = jugadores.index(jugador)
        jugador.liquidar_apuesta(tipoVictoria)   
        jugadores[index - 1].liquidar_apuesta(tipoDerrota)

        print (f"¡Ha ganado {jugador.nombre}!")
        printState(jugador, index)

        return True
    elif jugador.value() > 21: 
        print (f"¡Se ha pasado {jugador.nombre}!")
        printState(jugador, index)

        return False

def checkSaldo():
    if jugadores[0].saldo == 0 or jugadores[1].saldo == 0:
        return False
    else:
        return True

# Creación de jugadores
saldo_inicial = 2000.0
jugadores = [jugador.Jugador(False, saldo_inicial, "JUGADOR"), jugador.Jugador(True, saldo_inicial, "CRUPIER")]

# Creación de baraja
new_baraja=baraja.Baraja()

# ¿Saldo disponible para apostar?
while(True):
    try:
        apuesta=float(input("Jugador, ingrese su apuesta: "))
    except ValueError:
        print(f"\nApuesta {apuesta} errónea, inténtelo otra vez")
    else:
        retorno1 = jugadores[0].apuesta(apuesta)
        retorno2 = jugadores[1].apuesta(apuesta)

        if(retorno1==True and retorno2==True):
            print(f"\nAceptada la apuesta de {apuesta}")
            break
        else:
            print(f"\nNo cuenta con el saldo necesario para cubir la apuesta de {apuesta}. Inténtelo otra vez")

while(checkSaldo() == True):
    decision=str(input("¿Desea jugar a una partida de Blackjack (S)?: "))

    if decision != "S":
        break
    
    # Barajar
    new_baraja.barajar()

    # Reparto de cartas
    jugadores[0].addCard(new_baraja, True)
    jugadores[0].addCard(new_baraja, True)

    jugadores[1].addCard(new_baraja, True)
    jugadores[1].addCard(new_baraja, False)

    # ¿Blackjack del jugador?
    if(reviseGame(jugadores[0], "S_BLACKJACK", "N_BLACKJACK")):
        continue    

        
    # ¿Posible Blackjack del crupier?
    if jugadores[1].value() == 11:
        if jugadores[1].viewNotVisibleCard() == 10:
            jugadores[0].liquidar_apuesta("N_BLACKJACK")   
            jugadores[1].liquidar_apuesta("S_BLACKJACK") 
            continue
            
    while(True):
        decision=str(input("¿Coge otra carta (S) o se planta?: "))

        if decision == "S":
            jugadores[0].addCard(new_baraja, True)
            reviseGame(jugadores[0], "S", "N")
            continue
        else:
            break


    # Turno del crupier

    # Resolución de la apuesta

    # ¿Volver a jugar?