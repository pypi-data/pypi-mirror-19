"""Dies ist das Modul "schachtler.py". Es stellt eine Funktion namens print_lvl() bereit,
   die eine Liste mit beliebig vielen eingebetteten Listen ausgibt."""

def print_lvl(liste, einzug = False, ebene=0):
    """Diese Funktion erwartet ein positionelles Argument names "liste", das eine
    beliebige Python-Liste (mit eventuellen eingebetteten Listen) ist. Jedes Element
    der Liste wird (rekursiv) auf dem Bildschirm jeweils in einer eigenen Zeile ausgegeben.
    Mit dem zweiten Argument "einzug" kann eine Einrückung der inneren Listen aktiviert werden.
    Mit dem dritten Argument "ebene" können bei eingebetteten Listen Tabulatoren eingesetzt werden."""

    for element in liste:
        if isinstance(element, list):
            print_lvl(element, einzug, ebene+1)
        else:
            if einzug:
                for tab in range(ebene):
                    print("\t", end='')
            print(element)
