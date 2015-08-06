#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import csv
from padro_estruc import padro_estruc

def padro2csv(fitxer_padro):
	# current path
	path = os.getcwd()
	#input and write files
	inputfile = path + "\\" + fitxer_padro + ".txt"
	writefile = path + "\\" + fitxer_padro + ".csv"
	
	# Avisem de la creació del fitxer de sortida
	print 'Generant ........ ' + fitxer_padro + ".csv"
	
	#Open file for read txt (from padro habitants)
	rf = open(inputfile) # input file
	
	#Openfile to write csv
	with open(writefile, 'wb') as wf:
		writer = csv.writer(wf)
		writer.writerow(zip(*padro_estruc[1])[3])
		# read lines from txt
		for line in rf.readlines():
			row = []
			# Recorremos todos los registros
			for campos in padro_estruc[1]:
				ini = campos[0]-1 # offset
				fin = ini + campos[1] # longitud
				valor = line[ini:fin].strip() # valor
				row.append(valor)
			#write text into csv file
			writer = csv.writer(wf)
			writer.writerow(row[0:len(padro_estruc[1])])
		# close input file handle
		rf.close()

	# close output file handle
	wf.close()
	
	print "Finalitzat"