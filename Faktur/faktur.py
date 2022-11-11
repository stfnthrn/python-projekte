# Programm zur Anpassung der Rechnungsdatei aus Landwehr zur Übergabe an Diamant

from dataclasses import replace
import re

def datei_analysieren():

    za = 0      # Zähler Zeilen in Datei (Rückgabewert)
    zf = 0      # Zähler Faktursatz
    zg = 0      # Zähler Gegenkontosatz
    zk = 0      # Zähler Kostenstellensatz
    gegenkonto = ''
    kostenstelle = ''
    satz = 'F'  # Nächster erwarteter Satz

    with open('./in/infile.txt', 'r') as infile:
        infile_contents = infile.readline()

        if infile_contents[0 : 1] == satz:
            zf += 1
        else:
            print('Achtung! Datei beginnt nicht mit Faktursatz!')
    
        while infile_contents >= ' ':
            infile_contents = infile.readline()
            if infile_contents[0 : 1]  == 'F':
                if satz == 'K':
                    print('Achtung! Fehlender K-Satz in Zeile ' + str(za + 2) + '!')
                satz = 'G'
                zf += 1
            if infile_contents[0 : 1]  == 'G':
                gegenkonto = infile_contents[4 : 8]
                satz = 'K'
                zg += 1
            if infile_contents[0 : 1]  == 'K':
                kostenstelle = infile_contents[4 : 7]
                satz = 'F'
                zk += 1
            za += 1
            
    print()
    print('Gegenkonto:          ' + gegenkonto)
    print('Kostenstelle:        ' + kostenstelle)
    print()
    print('Faktursätze:         ' + str(zf))
    print('Gegenkontosätze:     ' + str(zg))
    print('Kostenstellensätze:  ' + str(zk))
    print('Zeilen gesamt:       ' + str(za) + '    Soll: ' + str(3 * zg))
    print()
    return za

def datei_schreiben():
    
    i = 1         # Zähler
    zao = 0       # Anzahl geschriebener Zeilen
    satz = 'F'    # Nächster erwarteter Satz
    g_betrag = '' # Betrag G-Satz
    k_betrag = '' # Betrag K-Satz
    g_summe = 0.0   # Summe aus G-Satz
    k_summe = 0.0   # Summe aus K-Satz
    
    with open('./in/infile.txt', 'r') as infile:
        while i < za+1:
            infile_contents = infile.readline()
            if infile_contents[0 : 1] == 'G':
                g_betrag = re.search(';19.00;(.+?);', infile_contents).group(1)
                g_summe += float(g_betrag.replace(',' , '.'))
            if infile_contents[0 : 1] == 'K':
                k_betrag = re.search('0;;;;;;(.+?);;;', infile_contents).group(1)
                k_summe += float(k_betrag.replace(',' , '.'))
            if infile_contents[0 : 1] == satz:
                if satz == 'F':
                    with open('./out/outfile.txt', 'a') as outfile:
                        outfile.write(infile_contents.replace(';\"R\";',';;'))
                        zao += 1
                        satz = 'G'
                else:
                    if satz == 'G':
                        with open('./out/outfile.txt', 'a') as outfile:
                            outfile.write(infile_contents.replace(';6;19.00',';;19.00'))
                            zao += 1
                            satz = 'K'
                    else:
                        if satz == 'K':
                            with open('./out/outfile.txt', 'a') as outfile:
                                outfile.write(infile_contents.replace(k_betrag , g_betrag))
                                zao += 1
                                satz = 'F'
            i += 1
    
        print('Geschriebene Zeilen: ' + str(zao))
        print('Kontrolle Summe der G-Beträge: ' + str(g_summe) + ' Euro')
        print('Kontrolle Summe der K-Beträge: ' + str(k_summe) + ' Euro')
        print()

# Hauptprogramm

steuerung = ''

while steuerung != 'e':
    za = datei_analysieren()

    steuerung = input('Mit schreiben fortfahren? j/w/e: ')
    if steuerung == 'j':
        print()
        datei_schreiben()
    if steuerung == 'w':
        print()

# Programmende
