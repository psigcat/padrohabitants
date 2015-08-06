#!/usr/bin/python
# -*- coding: utf-8 -*-

# Estructura de los ficheros .txt
# 2015-07-13

# Transcripció literal de la feina d'interpretació d'en Jordi Segon, tècnic SIG de Sant Joan de Vilatorrada

padro_estruc = {}

# Model de dades del padró d'habitants de la Diputació de Barcelona
padro_estruc[1] = [
	[1, 2,   'N', 'codi_provincia'],
	[3, 3,   'N', 'codi_municipi'],
	[6, 20,  'X', 'nom'],
	[26, 6,  'X', 'part_cognom1'],
	[32, 25, 'X', 'cognom1'],
	[57, 6,  'X', 'part_cognom1'],
	[63, 25, 'X', 'cognom1'],
	[88, 2,  'N', 'neix_codi_provincia'],
	[90, 3,  'N', 'neix_codi_municipi'],
	[93, 4,  'N', 'neix_any'],
	[97, 2,  'N', 'neix_mes'],
	[99, 2,  'N', 'neix_dia'],
	[101, 1,  'N', 'tipus_doc'],
	[102, 1,  'X', 'lletra_estrager'],
	[103, 9,  'X', 'doc_identitat'],
	[112, 20,  'N', 'passaport'],
	[132, 8,  'N', 'nia'],
	[147, 11,  'N', 'nie'],
	[161, 4,  'N', 'variacio_any'],
	[165, 2,  'N', 'variacio_mes'],
	[167, 2,  'N', 'variacio_dia'],
	[172, 2,  'N', 'districte'],
	[174, 3,  'N', 'seccio'],
	[178, 2,  'N', 'codi_entitat_colectiva'],
	[180, 2,  'N', 'codi_entitat_singular'],
	[182, 1,  'N', 'codi_digit_control'],
	[183, 2,  'N', 'codi_ncli_disseminat'],
	[210, 25,  'X', 'nom_entitat_singular'],
	[235, 25,  'X', 'nom_nucli_disseminat'],
	[260, 5,  'N', 'codi_via'],
	[265, 5,  'N', 'tipus_via'],
	[270, 25,  'X', 'nom_via'],
	[295, 5,  'N', 'altres'],
	[350, 1,  'N', 'tipus_numero'],
	[351, 5,  'X', 'numero'],
	[356, 5,  'N', 'numero_superior'],
	[361, 3,  'N', 'punt_quilometric'],
	[364, 1,  'N', 'hm'],
	[365, 1,  'X', 'bloc'],
	[369, 2,  'X', 'escala'],
	[371, 3,  'X', 'planta'],
	[374, 4,  'N', 'porta'],
	[378, 1,  'N', 'tipus_domicili'],
	[394, 10,  'N', 'full_padronal'],
	[497, 1,  'N', 'sexe'],
	[542, 2,  'N', 'nivell_estudis'],
	[544, 3,  'N', 'pais_nacionalitat'],
	[547, 2,  'N', 'procedencia_codi_provincia'],
	[549, 3,  'N', 'procedencia_codi_municipi'],
	[553, 3,  'N', 'procedencia_codi_consolat'],
]
