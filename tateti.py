#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import copy

CELLS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
TURN = {0: 'La computadora va', 1: 'Vas'}
SUCCESS = [
    (7, 8, 9), # Horizontal superior.
    (4, 5, 6), # Horizontal medio.
    (1, 2, 3), # Horizontal inferior.
    (7, 4, 1), # Vertical izquierda.
    (8, 5, 2), # Vertical centro.
    (9, 6, 3), # Vertical derecha.
    (9, 5, 1), # Diagonal superior izquierda.
    (7, 5, 3)  # Diagonal inferior izquierda.
]

class Tateti:

    def __init__(self):
        self.inProgress = True
        self.turn = random.randint(0, 1)

    def play(self):
        print('¡Jugate un Ta-Te-Ti!')
        play = True
        while play:
            playerLetter, computerLetter = self.selectLetter()
            table = [' '] * 10
            self.inProgress = True
            print(TURN.get(self.turn) + ' primero.')
            while self.inProgress:
                if self.turn:
                    # Turno del jugador
                    print(self.getTableStr(table))
                    move = self.getPlayerMove(table)
                    self.makeMove(table, playerLetter, move)
                    if self.isWinner(table, playerLetter):
                        self.finishPlay(table, '¡Felicidades, ganaste!')
                    elif self.fullTable(table):
                        self.finishPlay(table, '¡Es un empate!')
                    self.turn = 0
                else:
                    # Turno de la computadora
                    move = self.getComputerMove(table, computerLetter, playerLetter)
                    self.makeMove(table, computerLetter, move)
                    if self.isWinner(table, computerLetter):
                        self.finishPlay(table, '¡La computadora te ganó!')
                    elif self.fullTable(table):
                        self.finishPlay(table, '¡Es un empate!')
                    self.turn = 1
            if not self.rePlay():
                play = False

    def getTableStr(self, table):
        """
            Descripción: Arma una variable que contiene la tabla en
                         formato string.
            Parámetros:
                1 - table: Lista que contiene los valores de la partida.
            Retorna:
                1 - Tabla en formato string.
        """
        emptyRow = ' ' * 9
        tab = '    |    '
        tableStr =  '7' + (' ' * 8) + '|8' + (' ' * 8) + '|9' + (' ' * 8) + '\n'
        tableStr += '    ' + table[7] + tab + table[8] + tab + table[9] + '    \n'
        tableStr += emptyRow + '|' + emptyRow + '|' + emptyRow + '\n'
        tableStr += '---------+---------+---------\n'
        tableStr += '4' + (' ' * 8) + '|5' + (' ' * 8) + '|6' + (' ' * 8) + '\n'
        tableStr += '    ' + table[4] + tab + table[5] + tab + table[6] + '    \n'
        tableStr += emptyRow + '|' + emptyRow + '|' + emptyRow + '\n'
        tableStr += '---------+---------+---------\n'
        tableStr += '1' + (' ' * 8) + '|2' + (' ' * 8) + '|3' + (' ' * 8) + '\n'
        tableStr += '    ' + table[1] + tab + table[2] + tab + table[3] + '    \n'
        tableStr += emptyRow + '|' + emptyRow + '|' + emptyRow + '\n'
        return tableStr

    def selectLetter(self):
        """
            Descripción: Brinda al jugador la posibilidad de
                         seleccionar la letra que desea usar.
            Retorna:
                1 - Una lista que contiene dos elementos. El primero la
                    letra del jugador y el segundo la letra de la
                    computadora.
        """
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('¿Deseas ser X o O?')
            letter = input().upper()
        return ['X', 'O'] if letter == 'X' else ['O', 'X']

    def getPlayerMove(self, table):
        """
            Descripción: Permite al jugador ingresar su jugada.
            Parámetros:
                1 - table: Lista que contiene los valores de la partida.
            Retorna:
                1 - El siguiente movimiento del jugador.
        """
        move = ' '
        while True:
            print('¿Cuál es tu próxima jugada? (1-9)')
            move = input()
            if move not in CELLS or not self.hasFreeSpace(table, int(move)):
                move = ' '
                print('¡Elegí una opción válida!')
            else:
                break
        return int(move)

    def getComputerMove(self, table, computerLetter, playerLetter):
        """
            Descripción: Determina la siguiente jugada de la computadora.
                         Simula una IA (Inteligencia Artificial), la cual
                         decide que movimiento realizar, siguiendo los
                         siguintes pasos:
                         1 - Evalúa si puede ganar en el siguiente movimiento,
                             de ser posible, efectúa el movimiento.
                         2 - Evalúa si el jugador puede ganar en el siguiente
                             movimiento, de ser así, lo bloquea.
                         3 - Evalúa si alguna de las esquinas se encuentra
                             libre para ocuparla.
                         4 - Evalúa si el centro se encuentra disponible para
                             ocuparlo.
                         5 - Evalúa si alguno de los lados se encuentra libre
                             para ocuparlo.
            Parámetros:
                1 - table: Lista que contiene los valores de la partida.
                2 - computerLetter: Letra seleccionada por la computadora.
                3 - playerLetter: Letra seleccionada por el jugador.
            Retorna:
                1 - El siguiente movimiento de la computadora.
        """
        move = self.canWin(table, computerLetter)
        if move: return move
        move = self.canWin(table, playerLetter)
        if move: return move
        move = self.selectRandom(table, [1, 3, 7, 9])
        if move is not None: return move
        if self.hasFreeSpace(table, 5): return 5
        return self.selectRandom(table, [2, 4, 6, 8])

    def hasFreeSpace(self, table, move):
        """
            Descripción: Evalúa si la celda está disponible o no.
            Parámetros:
                1 - table: Lista que contiene los valores de la partida.
                2 - move: índice de la lista, con el cual se accederá a esta.
            Retorna:
                1 - True en el caso de que haya espacio y False en caso contrario.
        """
        return table[move] == ' '

    def canWin(self, table, letter):
        """
            Descripción: Predice el siguiente movimiento correcto.
            Parámetros:
                1 - table: Lista que contiene los valores de la partida.
                2 - letter: Letra con la cual se simulará si puede ganar
                            o bloquear el movimiento.
            Retorna:
                1 - El siguiente movimiento que permitirá ganar o bloquear dependiendo de su uso.
        """
        cell = 0
        for i in range(1, 10):
            copyTable = copy.copy(table)
            if self.hasFreeSpace(copyTable, i):
                self.makeMove(copyTable, letter, i)
                if self.isWinner(copyTable, letter):
                    cell = i
        return cell

    def selectRandom(self, table, plays):
        """
            Descripción: Selecciona una jugada al azar de una lista de jugadas
                         recibida.
                         Si el espacio se encuentra libre, lo agrega a la lista
                         de posibilidades.
            Parámetros:
                1 - table: Lista que contiene los valores de la partida.
                2 - plays: Lista de jugadas posibles a analizar (contiene
                           índices de la tabla).
            Retorna:
                1 - Si hay posibilidades, una jugada al azar, en caso contrario,
                    None.
        """
        possibilities = [i for i in plays if self.hasFreeSpace(table, i)]
        if len(possibilities):
            return random.choice(possibilities)
        return None

    def makeMove(self, table, letter, move):
        """
            Descripción: Completa la lista de la partida con el siguiente
                         movimiento.
            Parámetros:
                1 - table: Lista que contiene los valores seleccionados
                           en el juego.
                2 - letter: Letra con la que se completará el siguiente
                            movimiento.
                3 - move: Índice de la lista donde se agregará el valor.
        """
        table[move] = letter

    def isWinner(self, table, letter):
        """
            Descripción: Dados los valores de la tabla y una letra,
                         verifica si ganó o no.
            Parámetros:
                1 - table: Lista que contiene los valores
                           seleccionados en el juego.
                2 - letter: Letra con la que se evalúa si
                            ganó.
            Retorna:
                1 - True si ganó con alguna de las posibles combinaciones,
                    en caso contrario False.
        """
        return any(all(table[i] == letter for i in tup) for tup in SUCCESS)

    def fullTable(self, table):
        """
            Descripción: Evalúa si la tabla está completa o no.
            Parámetros:
                1 - table: Lista que contiene los valores seleccionados
                           en el juego.
            Retorna:
                1 - True en el caso de que se encuentre completa la lista
                    y False en caso contrario.
        """
        auxTable = list()
        for i, cell in enumerate(table):
            if not i:
                continue
            auxTable.append(cell)
        return all(cell in ['X', 'O'] for cell in auxTable)

    def finishPlay(self, table, message):
        """
            Descripción: Muestra la tabla en pantalla y un mensaje que indica
                         que el juego finalizó.
            Parámetros:
                1 - table: Lista que contiene los valores
                           seleccionados en el juego.
                2 - message: Contiene un mensaje en particular que se quiere
                             mostrar en pantalla.
        """
        print(self.getTableStr(table))
        print(message)
        self.inProgress = False

    def rePlay(self):
        """
            Descripción: Consulta al jugador si desea volver a jugar o no.
            Retorna:
                1 - True en caso de que el jugador haya seleccionado "S" y False en caso de seleccionar otra letra.
        """
        option = ''
        while True:
            print('¿Querés volver a jugar? Presioná "S" (Sí) o "N" (No)')
            option = input().lower()
            if option not in ['s', 'n']:
                option = ' '
                print('¡Elegí una opción válida!')
            else:
                break
        return option.startswith('s')

if __name__ == '__main__':
    game = Tateti()
    game.play()
