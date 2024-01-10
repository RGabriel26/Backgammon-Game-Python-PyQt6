from PyQt6.QtCore import QTimer, QCoreApplication, QElapsedTimer

from random import randint

from checkers import Checkers

from time import sleep


class AILogic:
    def __init__(self, gameLogic):
        print('Initializare AI Logic')
        self.gameLogic = gameLogic
        self.teamAI = self.gameLogic.teamTurn
        self.layouts = self.gameLogic.layouts

    def delay(self, milliseconds) -> None:
        timer = QElapsedTimer()
        timer.start()
        while timer.elapsed() < milliseconds:
            QCoreApplication.processEvents()

    def launchAI(self) -> None:
        if self.gameLogic.canMakeMove():
            return self.aiMove()
        else:
            return self.gameLogic.actionCanMakeMove()


    def aiMove(self) -> None:
        # TODO: implementeaza sistemul de mutari pentru AI
        # Cat timp exista zaruri, aceasta se va reapela
        # aici se verifica daca se pot realiza mutari cu zarurile primite prin functia candMakeMove
        # daca da, se face o lista cu seturi de pozitii posibilie
            # set de pozitie posibila => (pozitia_unde_este_piesa_initial - pozitia_unde_se_va_muta_piesa, zarul_folosit)
            # se va "muta piesa", adica se va sterge de pe pozitia anterioara si se va adauga pe pozitia noua
            # si se va sterge zarul folosit atat din lista care il stocheaza cat si din layout zarurilor destinat afisarii
        # daca mai exista zaruri, functia se va apela recursiv
        # cand nu mai exista piese, sau functia canMakeMove returneaza False, se va apela functia logic pentru a trece la jucatorul urmator
        # se va folosit si functia showPossibleMove pentru a afisa pozitiile posibile de pe pozitia de unde urmeaza sa se realizeze mutarea, pentru 
        # ca celalalt jucator sa inteleaga ce se intampla
        # Se va folosi un DELAY pentru a nu se intampla tot instant
        print("AI-ul face mutari...")
        oponentTeam = 'black' if self.teamAI == 'white' else 'white'


    def createMoveList(self, team) -> None:
        # lista care va fi returnata cu mutarile posibile de unde ai poate realiza mutari
        # forma listei: 
        # [pozitie_piesa_initiala, (pozitie_piesa_finala, zarul_folosit)]
        listMovePossibility = []
        oponentTeam = "black" if team == "white" else "white"
        foundOutMove = False
        possibleMove = []
        positions = self.gameLogic.getPositionsList()
        # navigarea prin pozitiile tablei
        # pentru a cauta pozitii unde sunt piesele Ai-ului
        for pos in positions:
            # daca se gaseste pe pozitia pos piese ale jucatorului
            # se creaza o lista de mutari losibile de pe aceasta pozitie folosind zarurile curente
            # VERIFICARE CA PE POZITIA N SA FIE PIESA AI-ULUI   
            if pos.count() > 0:
                if pos.itemAt(0).widget().objectName() == f"{self.teamAI}Checker":
                    posID = self.gameLogic.getPosID(pos.objectName())
                    possibleMove.clear()
                    # crearea listei cu mutari posibile de pe pozitia n
                    if self.teamAI == "white":
                        for dice in self.gameLogic.getDices():
                            possibleMove.append(posID + dice)
                    else:
                        for dice in self.gameLogic.getDices():
                            possibleMove.append(posID - dice)
                    # pentru fiecare mutare pozibila de pe pozitia de unde s-au gasit piese
                    for move in possibleMove:
                        useDice = self.gameLogic.getUsedDice(move, posID, team)
                        # CONDITIA CA MUTAREA POSIBILA SA FIE IN INTERIORUL TABLEI
                        if move >= 1 and move <= 24:
                            layoutPosition = getattr(self.layouts, f'pos{move}')
                            # cazul in care pe pozitia posibila exista alte piese
                            if layoutPosition.count() > 0:
                                # veificam ca pe pozitia respectica sa existe doar o piesa
                                if layoutPosition.count() == 1:
                                    # daca exista doar o piesa, atunci se verifica daca acesta este a adversarului
                                    if layoutPosition.itemAt(0).widget().objectName() == f'{oponentTeam}Checker':
                                        # daca piesa existenta este a adversarului
                                        # se ia in considerare ca AI ul poate face o mutare peste piesa adversarului
                                        # scotand piesa adversarului pe gard
                                        listMovePossibility.append((pos, (move, useDice)))
                                        # break
                                # excluderea pozitiilor unde exista piese ale opentului si sunt mai mult de 1 piese
                                lastChecker = layoutPosition.count() - 1
                                if layoutPosition.itemAt(lastChecker).widget().objectName() not in [f'{oponentTeam}Checker']:
                                    # DACA NU SUNT PIESE ALE OPONENTELOR, INSEAMNA CA PE POZITIA RESPECTIVA EXISTA MAI MULT DE 1 PIESA A JUCATORULUI ACTUAL
                                    listMovePossibility.append((pos, (move, useDice)))
                                    # break
                            else:
                                #CAZUL CAND PE POZITIA POSIBILA DE MUTARE NU EXISTA ALTE PIESE
                                listMovePossibility.append((pos, (move, useDice)))
                                # break
                        else:
                            # RESTRICTII
                            # se verifica daca jucatorul poate face mutari de scoatere a pieselor din joc
                            # momentul cand zona de scoatere a pieselor devine activa si jucatorul poate realiza mutari in afara tablei, rezultand scoaterea pieselor din joc
                            if self.gameLogic.allCheckersHouse() and not foundOutMove:

                                # cazul in care zarul folosit scoaterii piesei este egal cu pozitia piesei
                                if self.teamAI == "white":
                                    # daca pozitia selectata este corespunzatoare zarului care arunca piesa in afara jocului
                                    position = 25 - useDice
                                    if posID == position:
                                        # verificarea pozitiei mai mari sau egale cu cea a zarului folosit
                                        if getattr(self.layouts, f'pos{position}').count() == 0:
                                            usedDiceForOutCheckers = min(self.getDices())
                                        else:
                                            usedDiceForOutCheckers = useDice
                                        foundOutMove = True
                                        listMovePossibility.append(pos, (move, usedDiceForOutCheckers))
                                        # break
                                    # pentru poztitiile corespunzatoare zarurilor unde nu sunt piese, se activeaza zona de out a pieselor
                                    # pentru a folosi zarul ramas pentru a scoate ultima piesa disponobila
                                    else:
                                        position = 25 - 6
                                        while position < 25:
                                            # restrictie in cazul in care pe o pozitie mai mare decat zarul primit, poti face mutari, nu va permite scoaterea pieselor de pe pozitii mai mici decat zarul curent]
                                            # pentru a se obliga sa fie folosit zarul pentru facut mutari, nu pentru scos piese
                                            if getattr(self.layouts, f'pos{position}').count() > 0 and getattr(self.layouts, f'pos{position}').itemAt(0).widget().objectName() != f'{oponentTeam}Checker':
                                                break
                                            if posID == position + 1:
                                                # DACA PE POZITIA ZARULUI NU SUNT PIESE, INSEAMNA CA SE POT SCOATE PIESE DE PE POZITIA URMATORE
                                                if getattr(self.layouts, f'pos{posID - 1}').count() == 0:
                                                    foundOutMove = True
                                                    usedDiceForOutCheckers = useDice
                                                    listMovePossibility.append(pos, (move, usedDiceForOutCheckers))
                                                    # break
                                            position += 1
                                else:
                                    position = 0 + useDice
                                    if posID == position:
                                        # verificarea pozitiei mai mari sau egale cu cea a zarului folosit
                                        if getattr(self.layouts, f'pos{position}').count() == 0:
                                            usedDiceForOutCheckers = min(self.getDices())
                                        else:
                                            usedDiceForOutCheckers = useDice
                                        listMovePossibility.append(pos, (move, usedDiceForOutCheckers))
                                        foundOutMove = True
                                        # break
                                    # pentru poztitiile corespunzatoare zarurilor unde nu sunt piese, se activeaza zona de out a pieselor
                                    # pentru a folosi zarul ramas pentru a scoate ultima piesa disponobila
                                    else:
                                        position = 0 + 6
                                        while position > 0:
                                            # restrictie in cazul in care pe o pozitie mai mare decat zarul primit, poti face mutari, nu va permite scoaterea pieselor de pe pozitii mai mici decat zarul curent]
                                            # pentru a se obliga sa fie folosit zarul pentru facut mutari, nu pentru scos piese
                                            if getattr(self.layouts, f'pos{position}').count() > 0 and getattr(self.layouts, f'pos{position}').itemAt(0).widget().objectName() != f'{oponentTeam}Checker':
                                                break
                                            if posID == position - 1:
                                                # DACA PE POZITIA ZARULUI NU SUNT PIESE, INSEAMNA CA SE POT SCOATE PIESE DE PE POZITIA URMATORE
                                                if getattr(self.layouts, f'pos{posID + 1}').count() == 0:
                                                    foundOutMove = True
                                                    usedDiceForOutCheckers = useDice
                                                    listMovePossibility.append(pos, (move, usedDiceForOutCheckers))
                                                    # break
                                            position -= 1
            
        return listMovePossibility

        