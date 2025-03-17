import numpy as np
import os, time, msvcrt, math, random
from random import randint
import Pokemon_Graphics

#dict of map environments (for type weakness/strength)
#environment_decider = {0:"building", 1:"building"} 

# DATABASE INFORMATION
#------------------------------------------

#pokedex of pokemon (base stats) [name, type, hp, atk, def, sp.atk, sp.def, speed]
pokedex = {1 : ['CHIKORITA', 'gra', 45, 49, 65, 49, 65, 45], 2 : ['BAYLEEF', 'gra', 60, 62, 80, 63, 80, 60], 
           3 : ['MEGANIUM', 'gra', 80, 82, 100, 83, 100, 80], 4 : ['CYNDAQUIL', 'fir', 39, 52, 43, 60, 50, 65], 
           5 : ['QUILAVA', 'fir', 58, 64, 58, 80, 65, 80], 6 : ['TYPHLOSION', 'fir', 78, 84, 78, 109, 85, 100],
           7 : ['TOTODILE', 'wat', 50, 65, 64, 44, 48, 43], 8 : ['CROCONAW', 'wat', 65, 80, 80, 59, 63, 58], 
           9 : ['FERALIGATR', 'wat', 85, 105, 100, 79, 83, 78], 10 : ['PIDGEY','nor+fly', 40, 45, 40, 35, 35, 56], 
           11 : ['PIDGEOTTO','nor+fly', 63, 60, 55, 50, 50, 71], 12 : ['PIDGEOT','nor+fly', 83, 80, 75, 70, 70, 101],
           13 : ['SPEAROW','nor+fly', 40, 60, 30, 31, 31, 70], 14 : ['FEAROW', 'nor+fly', 65, 90, 65, 61, 61, 100], 
           15 : ['HOOTHOOT', 'nor+fly', 60, 30, 30, 36, 56, 50], 16 : ['NOCTOWL', 'nor+fly', 100, 50, 50, 76, 96, 70],
           17 : ['RATTATA', 'nor', 30, 56, 35, 25, 35, 72], 18 : ['RATICATE', 'nor', 55, 81, 60, 50, 70, 97],
           19 : ['SENTRET', 'nor', 35, 46, 34, 35, 45, 20], 20 : ['FURRET', 'nor', 85, 76, 64, 45, 55, 90],
           21 : ['PICHU', 'ele', 20, 40, 15, 35, 35, 60], 22 : ['PIKACHU', 'ele', 35, 55, 40, 50, 50, 90],
           23 : ['RAICHU', 'ele', 60, 90, 55, 90, 80, 110], 24 : ['CATERPIE', 'bug', 45, 30, 35, 20, 20, 45],
           25 : ['METAPOD', 'bug', 50, 20, 55, 25, 25, 30], 26 : ['BUTTERFREE', 'bug+fly', 60, 45, 50, 90, 80, 70],
           27 : ['WEEDLE', 'bug+poi', 40, 35, 30, 20, 20, 50], 28 : ['KAKUNA', 'bug+poi', 45, 25, 50, 25, 25, 35],
           29 : ['BEEDRILL', 'bug+poi', 65, 90, 40, 45, 80, 75], 30 : ['LEDYBA', 'bug+fly', 40, 20, 30, 40, 80, 55],
           31 : ['LEDIAN', 'bug+fly', 55, 35, 50, 55, 110, 85], 32 : ['SPINARAK', 'bug+poi', 40, 60, 40, 40, 40, 30],
           33 : ['ARIADOS', 'bug+poi', 70, 90, 70, 60, 60, 40], 34 : ['GEODUDE', 'rck+gro', 40, 80, 100, 30, 30, 20],
           35 : ['GRAVELER', 'rck+gro', 55, 95, 115, 45, 45, 35], 36 : ['GOLEM', 'rck+gro', 80, 120, 130, 55, 65, 45],
           37 : ['ZUBAT', 'poi+fly', 40, 45, 35, 30, 40, 55], 38 : ['GOLBAT', 'poi+fly', 75, 80, 70, 65, 75, 90],
           39 : ['CROBAT', 'poi+fly', 85, 90, 80, 70, 80, 130], 40 : ['CLEFFA', 'nor', 50, 25, 28, 45, 55, 15],
           41 : ['CLEFAIRY', 'nor', 70, 45, 48, 60, 65, 35], 42 : ['CLEFABLE', 'nor', 95, 70, 73, 95, 90, 60],
           43 : ['IGGLYBUFF', 'nor', 90, 30, 15, 40, 20, 15], 44 : ['JIGGLYPUFF', 'nor', 115, 45, 20, 45, 25, 20],
           45 : ['WIGGLYTUFF', 'nor', 140, 70, 45, 85, 50, 45], 46 : ['TOGEPI', 'nor', 35, 20, 65, 40, 65, 20],
           47 : ['TOGETIC', 'nor+fly', 55, 40, 85, 80, 105, 40], 48 : ['SANDSHREW', 'gro', 50, 75, 85, 20, 30, 40],
           49 : ['SANDSLASH', 'gro', 75, 100, 110, 45, 55, 65], 50 : ['EKANS', 'poi', 35, 60, 44, 40, 54, 55],
           51 : ['ARBOK', 'poi', 60, 85, 69, 65, 79, 80], 52 : ['DUNSPARCE', 'nor', 100, 70, 70, 65, 65, 45],
           53 : ['MAREEP', 'ele', 55, 40, 40, 65, 45, 35], 54 : ['FLAAFFY', 'ele', 70, 55, 55, 80, 60, 45],
           55 : ['AMPHAROS', 'ele', 90, 75, 85, 115, 90, 55], 56 : ['WOOPER', 'wat+gro', 55, 45, 45, 25, 25, 15],
           57 : ['QUAGSIRE', 'wat+gro', 95, 85, 85, 65, 65, 35], 58 : ['GASTLY', 'gho+poi', 30, 35, 30, 100, 35, 80],
           59 : ['HAUNTER', 'gho+poi', 45, 50, 45, 115, 55, 95], 60 : ['GENGAR', 'gho+poi', 60, 65, 60, 130, 75, 110],
           61 : ['UNOWN', 'psy', 48, 72, 48, 72, 48, 48], 62 : ['ONIX', 'rck+gro', 35, 45, 160, 30, 45, 70],
           63 : ['STEELIX', 'ste+gro', 75, 85, 200, 55, 65, 30], 64 : ['BELLSPROUT', 'gra+poi', 50, 75, 35, 70, 30, 40],
           65 : ['WEEPINBELL', 'gra+poi', 65, 90, 50, 85, 45, 55], 66 : ['VICTREEBEL', 'gra+poi', 80, 105, 65, 100, 70, 70],
           67 : ['HOPPIP', 'gra+fly', 35, 35, 40, 35, 55, 50], 68 : ['SKIPLOOM', 'gra+fly', 55, 45, 50, 45, 65, 80],
           69 : ['JUMPLUFF', 'gra+fly', 75, 55, 70, 55, 95, 110], 70 : ['PARAS', 'bug+gra', 35, 70, 55, 45, 55, 25],
           71 : ['PARASECT', 'bug+gra', 60, 95, 80, 60, 80, 30], 72 : ['POLIWAG', 'wat', 40, 50, 40, 40, 40, 90],
           73 : ['POLIWHIRL', 'wat', 65, 65, 65, 50, 50, 90], 74 : ['POLIWRATH', 'wat+fgt', 90, 95, 95, 70, 90, 70],
           75 : ['POLITOED', 'wat', 90, 75, 75, 90, 100, 70], 76 : ['MAGIKARP', 'wat', 20, 10, 55, 15, 20, 80],
           77 : ['GYARADOS', 'wat+fly', 95, 125, 79, 60, 100, 81], 78 : ['GOLDEEN', 'wat', 45, 67, 60, 35, 50, 63],
           79 : ['SEAKING', 'wat', 80, 92, 65, 65, 80, 68], 80 : ['SLOWPOKE', 'wat+psy', 90, 65, 65, 40, 40, 15],
           81 : ['SLOWBRO', 'wat+psy', 95, 75, 110, 100, 80, 30], 82 : ['SLOWKING', 'wat+psy', 95, 75, 80, 100, 110, 30],
           83 : ['ODDISH', 'gra+poi', 45, 50, 55, 75, 65, 30], 84 : ['GLOOM', 'gra+poi', 60, 65, 70, 85, 75, 40],
           85 : ['VILEPLUME', 'gra+poi', 75, 80, 85, 110, 90, 50], 86 : ['BELLOSSOM', 'gra', 75, 80, 95, 90, 100, 50],
           87 : ['DROWZEE', 'psy', 60, 48, 45, 43, 90, 42], 88 : ['HYPNO', 'psy', 85, 73, 70, 73, 115, 67],
           89 : ['ABRA', 'psy', 25, 20, 15, 105, 55, 90], 90 : ['KADABRA', 'psy', 40, 35, 30, 120, 70, 105],
           91 : ['ALAKAZAM', 'psy', 55, 50, 45, 135, 95, 120], 92 : ['DITTO', 'nor', 48, 48, 48, 48, 48, 48],
           93 : ['PINECO', 'bug', 50, 65, 90, 35, 35, 15], 94 : ['FORRETRESS', 'bug+ste', 75, 90, 140, 60, 60, 40],
           95 : ['NIDORAN(F)', 'poi', 55, 47, 52, 40, 40, 41], 96 : ['NIDORINA', 'poi', 70, 62, 67, 55, 55, 56],
           97 : ['NIDOQUEEN', 'poi+gro', 90, 92, 87, 75, 85, 76], 98 : ['NIDORAN(M)', 'poi', 46, 57, 40, 40, 40, 50],
           99 : ['NIDORINO', 'poi', 61, 72, 57, 55, 55, 65], 100 : ['NIDOKING', 'poi+gro', 81, 102, 77, 85, 75, 85],
           101 : ['YANMA', 'bug+fly', 65, 65, 45, 75, 45, 95], 102 : ['YANMEGA', 'bug+fly', 86, 76, 86, 116, 56, 95],
           103 : ['SUNKERN', 'gra', 30, 30, 30, 30, 30, 30], 104 : ['SUNFLORA', 'gra', 75, 75, 55, 105, 85, 30],
           105 : ['EXEGGCUTE', 'gra+psy', 60, 40, 80, 60, 45, 40], 106 : ['EXEGGUTOR', 'gra+psy', 95, 95, 85, 125, 75, 55],
           107 : ['SUDOWOODO', 'rck', 70, 100, 115, 30, 65, 30], 108 : ['WOBBUFFET', 'psy', 190, 33, 58, 33, 58, 33],
           109 : ['VENONAT', 'bug+poi', 60, 55, 50, 40, 55, 45], 110 : ['VENOMOTH', 'bug+poi', 70, 65, 60, 90, 75, 90],
           111 : ['SCYTHER', 'bug+fly', 70, 110, 80, 55, 80, 105], 112 : ['SCIZOR', 'bug+ste', 70, 130, 100, 55, 80, 65],
           113 : ['PINSIR', 'bug', 65, 125, 100, 55, 70, 85], 114 : ['HERACROSS', 'bug+fgt', 80, 125, 75, 40, 95, 85],
           115 : ['KOFFING', 'poi', 40, 65, 95, 60, 45, 35], 116 : ['WEEZING', 'poi', 65, 90, 120, 85, 70, 60],
           117 : ['GRIMER', 'poi', 80, 80, 50, 40, 50, 25], 118 : ['MUK', 'poi', 105, 105, 75, 65, 100, 50],
           119 : ['MAGNEMITE', 'ele+ste', 25, 35, 70, 95, 55, 45], 120 : ['MAGNETON', 'ele+ste', 50, 60, 95, 120, 70, 70],
           121 : ['VOLTORB', 'ele', 40, 30, 50, 55, 55, 100], 122 : ['ELECTRODE', 'ele', 60, 50, 70, 80, 80, 150],
           123 : ['AIPOM', 'nor', 55, 70, 55, 40, 55, 85], 124 : ['AMBIPOM', 'nor', 75, 100, 66, 60, 66, 115],
           125 : ['SNUBULL', 'nor', 60, 80, 50, 40, 40, 30], 126 : ['GRANBULL', 'nor', 90, 120, 75, 60, 60, 45],
           127 : ['VULPIX', 'fir', 38, 41, 40, 50, 65, 65], 128 : ['NINETALES', 'fir', 73, 76, 75, 81, 100, 100],
           129 : ['GROWLITHE', 'fir', 55, 70, 45, 70, 50, 60], 130 : ['ARCANINE', 'fir', 90, 110, 80, 100, 80, 95],
           131 : ['STANTLER', 'nor', 73, 95, 62, 85, 65, 85], 132 : ['MARILL', 'wat', 70, 20, 50, 20, 50, 40],
           133 : ['AZUMARILL', 'wat', 100, 50, 80, 60, 80, 50], 134 : ['DIGLETT', 'gro', 10, 55, 25, 35, 45, 95],
           135 : ['DUGTRIO', 'gro', 35, 100, 50, 50, 70, 120], 136 : ['MANKEY', 'fgt', 40, 80, 35, 35, 45, 70],
           137 : ['PRIMEAPE', 'fgt', 65, 105, 60, 60, 70, 95], 138 : ['MEOWTH', 'nor', 40, 45, 35, 40, 40, 90],
           139 : ['PERSIAN', 'nor', 65, 70, 60, 65, 65, 115], 140 : ['PSYDUCK', 'wat', 50, 52, 48, 65, 50, 55],
           141 : ['GOLDUCK', 'wat', 80, 82, 78, 95, 80, 85], 142 : ['MACHOP', 'fgt', 70, 80, 50, 35, 35, 35],
           143 : ['MACHOKE', 'fgt', 80, 100, 70, 50, 60, 45], 144 : ['MACHAMP', 'fgt', 90, 130, 80, 65, 85, 55],
           145 : ['TYROGUE', 'fgt', 35, 35, 35, 35, 35, 35], 146 : ['HITMONLEE', 'fgt', 50, 120, 53, 35, 110, 87],
           147 : ['HITMONCHAN', 'fgt', 50, 105, 79, 35, 110, 76], 148 : ['HITMONTOP', 'fgt', 50, 95, 95, 35, 110, 70],
           149 : ['GIRAFARIG', 'nor+psy', 70, 80, 65, 90, 65, 85], 150 : ['TAUROS', 'nor', 75, 100, 95, 40, 70, 110],
           151 : ['MILTANK', 'nor', 95, 80, 105, 40, 70, 100], 152 : ['MAGBY', 'fir', 45, 75, 37, 70, 55, 83],
           153 : ['MAGMAR', 'fir', 65, 95, 57, 100, 85, 93], 154 : ['SMOOCHUM', 'ice+psy', 45, 30, 15, 85, 65, 65],
           155 : ['JYNX', 'ice+poi', 65, 50, 35, 115, 95, 95], 156 : ['ELEKID', 'ele', 45, 63, 37, 65, 55, 95],
           157 : ['ELECTABUZZ', 'ele', 65, 83, 57, 95, 85, 105], 158 : ['MR.MIME', 'psy', 40, 45, 65, 100, 120, 90],
           159 : ['SMEARGLE', 'nor', 55, 20, 35, 20, 45, 75], 160 : ["FARFETCH'D", 'nor+fly', 52, 90, 55, 58, 62, 60],
           161 : ['NATU', 'psy+fly', 40, 50, 45, 70, 45, 70], 162 : ['XATU', 'psy+fly', 65, 75, 70, 95, 70, 95],
           163 : ['QWILFISH', 'wat+poi', 65, 95, 85, 55, 55, 85], 164 : ['TENTACOOL', 'wat+psy', 40, 40, 35, 50, 100, 70],
           165 : ['TENTACRUEL', 'wat+poi', 80, 70, 65, 80, 120, 100], 166 : ['KRABBY', 'wat', 30, 105, 90, 25, 25, 50],
           167 : ['KINGLER', 'wat', 55, 130, 115, 50, 50, 75], 168 : ['SHUCKLE', 'bug+rck', 20, 10, 230, 10, 230, 5],
           169 : ['STARYU', 'wat', 30, 45, 55, 70, 55, 85], 170 : ['STARMIE', 'wat+psy', 60, 75, 85, 100, 85, 115],
           171 : ['SHELLDER', 'wat', 30, 65, 100, 45, 25, 40], 172 : ['CLOYSTER', 'wat+ice', 50, 95, 180, 85, 45, 70],
           173 : ['CORSOLA', 'wat+rck', 65, 55, 95, 65, 95, 35], 174 : ['REMORAID', 'wat', 35, 65, 35, 65, 35, 65],
           175 : ['OCTILLERY', 'wat', 75, 105, 75, 105, 75, 45], 176 : ['CHINCHOU', 'wat+ele', 75, 38, 38, 56, 56, 67],
           177 : ['LANTURN', 'wat+ele', 125, 58, 58, 76, 76, 67], 178 : ['SEEL', 'wat', 65, 45, 55, 45, 70, 45],
           179 : ['DEWGONG', 'wat+ice', 90, 70, 80, 70, 95, 70], 180 : ['LICKITUNG', 'nor', 90, 55, 75, 60, 75, 30],
           181 : ['LICKILICKY', 'nor', 110, 85, 95, 80, 95, 50], 182 : ['TANGELA', 'gra', 65, 55, 115, 100, 40, 60],
           183 : ['TANGROWTH', 'gra', 100, 100, 125, 110, 50, 50], 184 : ['EEVEE', 'nor', 55, 55, 50, 45, 65, 55],
           185 : ['VAPOREON', 'wat', 130, 65, 60, 110, 95, 65], 186 : ['JOLTEON', 'ele', 65, 65, 60, 110, 95, 130],
           187 : ['FLAREON', 'fir', 65, 130, 60, 95, 110, 65], 188 : ['ESPEON', 'psy', 65, 65, 60, 130, 95, 110],
           189 : ['UMBREON', 'dar', 95, 65, 110, 60, 130, 65], 190 : ['HORESEA', 'wat', 30, 40, 70, 70, 25, 60],
           191 : ['SEADRA', 'wat', 55, 65, 95, 95, 45, 85], 192 : ['KINGDRA', 'wat+drg', 75, 95, 95, 95, 95, 85],
           193 : ['GLIGAR', 'gro+fly', 65, 75, 105, 35, 65, 85], 194 : ['DELIBIRD', 'ice+fly', 45, 55, 45, 65, 45, 75],
           195 : ['SWINUB', 'ice+gro', 50, 50, 40, 30, 30, 50], 196 : ['PILOSWINE', 'ice+gro', 100, 100, 80, 60, 60, 50],
           197 : ['MAMOSWINE', 'ice+gro', 110, 130, 80, 70, 60, 80], 198 : ['TEDDIURSA', 'nor', 60, 80, 50, 50, 50, 40],
           199 : ['URSARING', 'nor', 90, 130, 75, 75, 75, 55], 200 : ['PHANPY', 'nor', 90, 60, 60, 40, 40, 40],
           201 : ['DONPHAN', 'gro', 90, 120, 120, 60, 60, 50], 202 : ['MANTINE', 'wat+fly', 65, 40, 70, 80, 140, 70],
           203 : ['SKARMORY', 'ste+fly', 65, 80, 140, 40, 70, 70], 204 : ['DODUO', 'nor+fly', 35, 85, 45, 35, 35, 75],
           205 : ['DODRIO', 'nor+fly', 60, 110, 70, 60, 60, 100], 206 : ['PONYTA', 'fir', 50, 85, 55, 65, 65, 90],
           207 : ['RAPIDASH', 'fir', 65, 100, 70, 80, 80, 105], 208 : ['CUBONE', 'gro', 50, 50, 95, 40, 50, 35],
           209 : ['MAROWAK', 'gro', 60, 80, 110, 50, 80, 45], 210 : ['KANGASKHAN', 'nor', 105, 95, 80, 40, 80, 90],
           211 : ['RHYHORN', 'gro+rck', 80, 85, 95, 30, 30, 25], 212 : ['RHYDON', 'gro+rck', 105, 130, 120, 45, 45, 40],
           213 : ['MURKROW', 'dar+fly', 60, 85, 42, 85, 42, 91], 214 : ['HOUNDOUR', 'dar+fir', 45, 60, 30, 80, 50, 65],
           215 : ['HOUNDOOM', 'dar+fir', 75, 90, 50, 110, 80, 95], 216 : ['SLUGMA', 'fir', 40, 40, 40, 70, 40, 20],
           217 : ['MAGCARGO', 'fir+rck', 50, 50, 120, 80, 80, 30], 218 : ['SNEASEL', 'dar+ice', 55, 95, 55, 35, 75, 115],
           219 : ['MISDREAVUS', 'gho', 60, 60, 60, 85, 85, 85], 220 : ['PORYGON', 'nor', 65, 60, 70, 85, 75, 40],
           221 : ['PORYGON2', 'nor', 85, 80, 90, 105, 95, 60], 222 : ['CHANSEY', 'nor', 250, 5, 5, 35, 105, 50],
           223 : ['BLISSEY', 'nor', 255, 10, 10, 75, 135, 55], 224 : ['LAPRAS', 'wat+ice', 130, 85, 80, 85, 95, 60],
           225 : ['OMANYTE', 'rck+wat', 35, 40, 100, 90, 55, 35], 226 : ['OMASTAR', 'rck+wat', 70, 60, 125, 115, 70, 55],
           227 : ['KABUTO', 'rck+wat', 30, 80, 90, 55, 45, 55], 228 : ['KABUTOPS', 'rck+wat', 60, 115, 105, 65, 70, 80],
           229 : ['AERODACTYL', 'rck+fly', 80, 105, 65, 60, 75, 130], 230 : ['SNORLAX', 'nor', 160, 110, 65, 65, 110, 30],
           231 : ['BULBASAUR', 'gra+poi', 45, 49, 49, 65, 65, 45], 232 : ['IVYSAUR', 'gra+poi', 60, 62, 63, 80, 80, 60],
           233 : ['VENUSAUR', 'gra+poi', 80, 82, 83, 100, 100, 80], 234 : ['CHARMANDER', 'fir', 39, 52, 43, 60, 50, 65],
           235 : ['CHARMELEON', 'fir', 58, 64, 58, 80, 65, 80], 236 : ['CHARIZARD', 'fir+fly', 78, 84, 78, 109, 85, 100],
           237 : ['SQUIRTLE', 'wat', 44, 48, 65, 50, 64, 43], 238 : ['WARTORTLE', 'wat', 59, 63, 80, 65, 80, 58],
           239 : ['BLASTOISE', 'wat', 79, 83, 100, 85, 105, 78], 240 : ['ARTICUNO', 'ice+fly', 90, 85, 100, 95, 125, 85],
           241 : ['ZAPDOS', 'ele+fly', 90, 90, 85, 125, 90, 100], 242 : ['MOLTRES', 'fir+fly', 90, 100, 90, 125, 85, 90],
           243 : ['RAIKOU', 'ele', 90, 85, 75, 115, 100, 115], 244 : ['ENTEI', 'fir', 115, 115, 85, 90, 75, 100],
           245 : ['SUICUNE', 'wat', 100, 75, 115, 90, 115, 85], 246 : ['DRATINI', 'drg', 41, 64, 45, 50, 50, 50],
           247 : ['DRAGONAIR', 'dgr', 61, 84, 65, 70, 70, 70], 248 : ['DRAGONITE', 'drg+fly', 91, 134, 95, 100, 100, 80],
           249 : ['LARVITAR', 'rck+gro', 50, 64, 50, 45, 50, 41], 250 : ['PUPITAR', 'rck+gro', 70, 84, 70, 65, 70, 51],
           251 : ['TYRANITAR', 'rck+dar', 100, 134, 110, 95, 100, 61], 252 : ['LUGIA', 'psy+fly', 106, 90, 130, 90, 154, 110],
           253 : ['HO-OH', 'fir+fly', 106, 130, 90, 110, 154, 90], 254 : ['MEWTWO', 'psy', 106, 110, 90, 154, 90, 130],
           255 : ['MEW', 'psy', 100, 100, 100, 100, 100, 100], 256 : ['CELEBI', 'psy+gra', 100, 100, 100, 100, 100, 100]}

# dict of pokemon moves [description, type, category, power, accuracy, PP, (opt) special effect]
moves_dict = {'Bite' : ["The foe is bitten with viciously sharp fangs. It may make the target flinch.",
                        'dar', 'phy', 60, 100, 25, 'stat opnt_fln_30'],
              'Crunch' : ["The user crunches up the foe with sharp fangs. It may also lower the target's Defense stat.",
                          'dar', 'phy', 80, 100, 15, 'stat opnt_def_dn1_20'],
              'Ember' : ["The foe is attacked with small flames. The target may also be left with a burn.",
                         'fir', 'spc', 40, 100, 25, 'stat opnt_brn_10'],
              'Flame Wheel' : ["The user cloaks itself in fire and charges at the foe. It may also leave the target with a burn.",
                    'fir', 'phy', 60, 100, 25, 'stat opnt_brn_10'],
              #'Foresight' : ["Enables the user to hit a Ghost type with any type of move. It also enables the user to hit an evasive foe.",
              #               'nor', 'sta', 0, 100, 40, 'stat user_acc_up100_100+attk ghost'],         
              'Fury Attack' : ["The foe is jabbed repeatedly with a horn or beak two to five times in a row.",
                               'nor', 'phy', 15, 85, 20, 'attk fury'],
              'Glare' : ["The user intimidates the foe with the pattern on its belly to cause paralysis.",
                         'nor', 'sta', 0, 75, 30, 'stat opnt_par_100'],              
              'Grass Whistle' : ["The user plays a pleasant melody that lulls the foe into a deep sleep.", 
                                 'gra', 'sta', 0, 55, 15, 'stat opnt_slp_100'],              
              'Growl' : ["The user growls in an endearing way, making the foe less wary. The target's Attack stat is lowered.", 
                         'nor', 'sta', 0, 100, 40, 'stat opnt_atk_dn1_100'],
              'Gust' : ["A gust of wind is whipped up by wings and launched at the foe to inflict damage.",
                        'fly', 'spc', 40, 100, 35, ''],
              'Hypnosis' : ["The user employs hypnotic suggestion to make the target fall into a deep sleep.",
                            'psy','sta', 0, 60, 20, 'stat opnt_slp_100'],
              'Ice Fang' : ["The user bites with cold-infused fangs. It may also make the foe flinch or freeze.",
                    'ice', 'phy', 65, 95, 15, 'stat opnt_frz_10+stat opnt_fln_10'],
              'Leer' : ["The foe is given an intimidating leer with sharp eyes. The target's Defense stat is reduced.",
                        'nor', 'sta', 0, 100, 30, 'stat opnt_def_dn1_100'],
              'Lovely Kiss' : ["With a scary face, the user forces a kiss on the foe. It may make the target fall asleep.",
                               'nor', 'sta', 0, 75, 10, 'stat opnt_slp_100'],              
              'Magical Leaf' : ["The user scatters curious leaves that chase the foe. This attack will not miss.",
                                'gra', 'spc', 50, 100, 20, 'attk no_miss'],
              'Peck' : ["The foe is jabbed with a sharply pointed beak or horn.",
                        'fly','phy', 35, 100, 35, ''],
              'Poison Gas' : ["A cloud of poison gas is sprayed in the foe's face. It may poison the target.", 
                              'poi', 'sta', 0, 55, 40, 'stat opnt_psn_100'],              
              'Poison Powder' : ["A cloud of poisonous dust is scattered on the foe. It may poison the target.", 
                                 'poi', 'sta', 0, 75, 35, 'stat opnt_psn_100'],
              'Quick Attack' : ["The user lunges at the foe at a speed that makes it almost invisible. It is sure to strike first.",
                                'nor', 'phy', 40, 100, 30, 'attk first'],              
              'Razor Leaf' : ["Sharp-edged leaves are launched to slash at the foe. It has a high critical-hit ratio.",
                              'gra', 'phy', 55, 95, 25, 'attk crit_12.5'],
              #'Rest' : ["The user goes to sleep for two turns. It fully restores the user's HP and heals any status problem.",
              #          'psy', 'sta', 0, 100, 10, 'stat opnt_slp_100+stat user_hp _up10_100'],              
              #'Sand Attack' : ["Sand is hurled in the foe's face, reducing its accuracy.",
              #                 'gro', 'sta', 0, 100, 15, 'stat opnt_acc_dn20_100'],            
              'Scary Face' : ["The user frightens the foe with a scary face to sharply reduce its Speed stat.",
                              'nor', 'sta', 0, 90, 10, 'stat opnt_spe_dn2_100'],
              'Scratch' : ["Hard, pointed, and sharp claws rake the foe to inflict damage.",
                           'nor', 'phy', 40, 100, 35, ''],
              #'Secret Power' : ["The user attacks the target with a secret power. Its added effects vary depending on the user's environment.",
                                #'nor', 'phy', 70, 100, 20, 'a lot of conditions depending on environment'],                 
              'Sing' : ["A soothing lullaby is sung in a calming voice that puts the foe into a deep slumber.",
                        'nor', 'sta', 0, 55, 15, 'stat opnt_slp_100'],   
              'Sleep Powder' : ["The user scatters a big cloud of sleep-inducing dust around the foe.",
                                'gra', 'sta', 0, 75, 15, 'stat opnt_slp_100'],  
              #'Smokescreen' : ["The user releases an obscuring cloud of smoke or ink. It reduces the foe's accuracy.",
              #                 'nor', 'sta', 0, 100, 20, 'stat opnt_acc_dn20_100'],      
              'Spore' : ["The user scatters bursts of spores that induce sleep.",
                         'gra', 'sta', 0, 100, 15, 'stat opnt_slp_100'], 
              'Stun Spore' : ["The user scatters a cloud of paralyzing powder. It may paralyze the target.",
                              'gra', 'sta', 0, 75, 30, 'stat opnt_par_100'],               
              'Synthesis' : ["The user restores its own HP. The amount of HP regained varies with the weather.",
                             'gra', 'sta', 0, 100, 5, 'stat user_hp _up5_100'],
              'Tackle' : ["A physical attack in which the user charges and slams into the foe with its whole body.",
                          'nor', 'phy', 35, 95, 35, ''],
              'Thunder Wave' : ["A weak electric charge is launched at the foe. It causes paralysis if it hits.",
                                'ele', 'sta', 0, 100, 20, 'stat opnt_par_100'],              
              #'Toxic' : ["A move that leaves the target badly poisoned. Its poison damage worsens every turn.",
                         #'poi', 'sta', 0, 90, 10, 'stat opnt_bpn_100'],      
              #'Toxic Spikes' : ["The user lays a trap of poison spikes at the foe's feet. They poison foes that switch into battle.",
                                #'poi', 'sta', 0, 90, 10, 'two layers of poison'],                
                         
              ##What about badly poisoned?           
                         
              'Twister' : ["The user whips up a vicious tornado to tear at the foe. It may also make the foe flinch.",
                           'drg', 'spc', 40, 100, 20, 'stat opnt_fln_30'],
              'Water Gun' : ["The foe is blasted with a forceful shot of water.",
                             'wat', 'spc', 40, 100, 25, ''],
              'Will-O-Wisp' : ["The user shoots a sinister, bluish white flame at the foe to inflict a burn.",
                               'fir', 'sta', 0, 75, 15, 'stat opnt_brn_100'],              
              #'Yawn' : ["The user lets loose a huge yawn that lulls the target into falling asleep on the next turn.",
                        #'nor', 'sta', 0, 100, 10, 'opponent sleeps next turn'],              
              #'' : [],
              '' : []}

#dict of names of stats
stats_names = {'atk': 'Attack', 'def': 'Defense', 'spa': 'Special Attack', 'spd': 'Special Defense', 'spe': 'Speed'} 

#dicts of attacks' strength, weakness, and immunity based on type
super_effective = {'bug':['dar','gra','psy'], 'dar':['gho','psy'], 'drg':['drg'],
                   'ele':['fly','wat'], 'fgt':['dar','ice','nor','rck','ste'], 'fir':['bug','gra','ice','ste'],
                   'fly':['bug','fgt','gra'], 'gho':['gho','psy'], 'gra':['gro','rck','wat'],
                   'gro':['ele','fir','poi','rck','ste'], 'ice':['drg','fly','gra','gro'], 'nor':[],
                   'poi':['gra'], 'psy':['fgt','poi'], 'rck':['bug','fir','fly','ice'],
                   'ste':['ice','rck'], 'wat':['fir','rck','gro']}

not_effective = {'bug':['fgt','fir','fly','gho','poi','ste'], 'dar':['dar','fgt'], 'drg':['ste'],
                 'ele':['drg','ele','gra'], 'fgt':['bug','fly','poi','psy'], 'fir':['drg','fir','rck','wat'],
                 'fly':['ele','rck','ste'], 'gho':['dar'], 'gra':['bug','drg','fir','fly','gra','poi','ste'],
                 'gro':['bug','gra'], 'ice':['fir','ice', 'ste', 'wat'], 'nor':['rck','ste'],
                 'poi':['gho','gro','poi','rck'], 'psy':['psy','ste'], 'rck':['fgt','gro','ste'],
                 'ste':['ele','fir','ste','wat'], 'wat':['drg','gra','wat']}    

immune = {'bug':[], 'dar':[], 'drg':[],
          'ele':['gro'], 'fgt':['gho'], 'fir':[],
          'fly':[], 'gho':['nor'], 'gra':[],
          'gro':['fly'], 'ice':[], 'nor':['gho'],
          'poi':['ste'], 'psy':['dar'], 'rck':[],
          'ste':[], 'wat':[]}

print_type = {'nor':'NORMAL', 'fir':'FIRE', 'fgt':'FIGHT', 'wat':'WATER', 'fly':'FLY', 'gra':'GRASS', 'poi':'POISON', 'ele':'ELECTRIC', \
              'gro':'GROUND', 'psy':'PSYCHIC', 'rck':'ROCK', 'ice':'ICE', 'bug':'BUG', 'drg':'DRAGON', 'gho':'GHOST', 'dar':'DARK', \
              'ste':'STEEL'}

#dict of bag items [description, effect]
bag_dict = {"Burn Heal": ['Blah', 'rem_brn'],
             "Chesto Berry": ['Blah', 'rem_slp']}

# number of times tried to escape
C = 0

# opnt team (change from base stats) [pokedex #, hp, atk, def, sp.atk, sp.def, speed, lv, 4*[moves, PP], condition], no duplicate moves allowed
opponents = {1002 : [[248, 50, 200, 20, 20, 20, 10, 40, 'Ice Fang', moves_dict['Ice Fang'][5], 'Flame Wheel', moves_dict['Flame Wheel'][5],
                     'Sleep Powder', moves_dict['Sleep Powder'][5],'Twister', moves_dict['Twister'][5], '', 'opnt1', ''], #248
             
                    [22, 20, 100, 10, 10, 10, 10, 15, 'Growl', moves_dict['Growl'][5], 'Quick Attack', moves_dict['Quick Attack'][5],
                     'Stun Spore', moves_dict['Stun Spore'][5],'Synthesis', moves_dict['Synthesis'][5], '', 'opnt2', '']]}

# player team (change from base stats) [pokedex #, hp, atk, def, sp.atk, sp.def, speed, lv, 4*[moves, PP], condition], no duplicate moves allowed
new_team = [[3, 20, 20, 20, 20, 20, 20, 35, 'Crunch', moves_dict['Crunch'][5], 'Poison Powder', moves_dict['Poison Powder'][5], 
              'Magical Leaf', moves_dict['Magical Leaf'][5], 'Fury Attack', moves_dict['Fury Attack'][5], '', 'user1', ''],
             
             [130, 0, 0, 0, 0, 0, 0, 25, 'Flame Wheel', moves_dict['Flame Wheel'][5], 'Scratch', moves_dict['Scratch'][5], 
              'Bite', moves_dict['Bite'][5], 'Will-O-Wisp', moves_dict['Will-O-Wisp'][5], '', 'user2', '']]

#items currently in user_bag [name, quantity left]
user_bag = [["Burn Heal", 1], ["Chesto Berry", 2]]


# INTRODUCTION FUNCTIONS
#------------------------------------------
def sex():
    gender = str.upper(input("Are you a boy?\nOr are you a girl? "))
    if gender == "BOY" or gender == "GIRL": 
        ans = str.upper(input("\nSo you are a "+gender+" then? "))
        print('')
        if ans == "YES":
            time.sleep(1)
            return gender
        else: 
            return sex()
    else: 
        return sex()
    
    
def name():
    p_name = input("Please tell me your name. ")
    ans = str.upper(input("\nYour name is "+p_name+"? "))
    print('')
    if ans == "YES": 
        time.sleep(1)
        return p_name
    else: 
        return name()


# MOVEMENT FUNCTIONS
#------------------------------------------
def step(a, b, n_map, previous_team): 
    time.sleep(0.2)
    msvcrt.getch()
    direction = str(msvcrt.getch()) #prompt user to input a keyboard direction
    
    b_max = map_lays[n_map][0] #set max column number as b_max
    a_max = map_lays[n_map] #set max row number as a_max
    
    if direction == "b'M'": #check if direction is right
        if b+1 < len(b_max): #check if movement passes over right boundary of map
            c = a 
            d = b+1 #right is valid
        else:         
            os.system('cls')
            print(map_lays[n_map])        
            return step(a, b, n_map, previous_team) #retry
    
    elif direction == "b'K'": #check if direction is left
        if b-1 >= 0: #check if movement passes over left boundary of map
            c = a
            d = b-1 #left is valid
        else:
            os.system('cls')
            print(map_lays[n_map])       
            return step(a, b, n_map, previous_team) #retry
        
    elif direction == "b'H'": #check if direction is up
        if a-1 >= 0: #check if movement passes over upper boundary of map
            c = a-1 #up is valid
            d = b
        else:      
            os.system('cls')
            print(map_lays[n_map])
            return step(a, b, n_map, previous_team) #retry
        
    elif direction == "b'P'": #check if direction is down
        if a+1 < len(a_max): #check if movement passes over lower boundary of map
            c = a+1 #down is valid
            d = b
        else:
            os.system('cls')
            print(map_lays[n_map])         
            return step(a, b, n_map, previous_team) #retry
    else:
        os.system('cls')
        print(map_lays[n_map])    
        return step(a, b, n_map, previous_team) #retry
    
    p = map_lays[n_map][c][d] #set value of new position as p 
    if p != 0: #check if there is an object/exit in the way 
        os.system('cls')
        
        a, b, n_map = change_map(a,b,c,d,n_map) #check if map changes
        print(map_lays[n_map])
        
        for key in dict_lays[n_map]: #convert p to a message if applicable
            if p == key: 
                msg = dict_lays[n_map][p]
                
                if 'battle' in msg: #check if battle sequence is needed
                    print('\n'+msg[2]) #print opponent message
                    time.sleep(msg[3]) 
                    global environment
                    
                    environment = environment_decider[n_map]
                    winner, previous_team = battle_main(p, new_team, previous_team, msg) #initiate battle sequence   
                    
                    if winner == 'user': #check if player won battle
                        os.system('cls')
                        print(map_lays[n_map])
                        
                        post_msg = post_battle_msg[p]
                        for x in post_msg:
                            print(x)
                            time.sleep(3)
                        
                        dict_lays[n_map][p] = replace_battle_msg[p]
                        
                    else:
                        map_lays[n_map][a][b] = 0 #set old position to 0
                        map_lays[checkpoint_map][checkpoint_row][checkpoint_col] = 100 #set new position to 100
                        previous_team = [] #wipe battle history
                        
                        os.system('cls')
                        print(map_lays[checkpoint_map])
                        return step(checkpoint_row, checkpoint_col, checkpoint_map, previous_team) #relocate to checkpoint
                else:
                    print('\n'+msg)
                
        return step(a, b, n_map, previous_team) #loop to beginning again
    else:
        map_lays[n_map][a][b] = 0 #set old position to 0
        map_lays[n_map][c][d] = 100 #set new position to 100
        
        os.system('cls')
        print(map_lays[n_map])
        return step(c, d, n_map, previous_team) #retry   
    
    
def change_map(a,b,c,d,n_map):
    if n_map == 0: #check if map is player house second floor
        if m_1[c][d] == 2 and a == 0 and b == 2: #check if location is staircase 
            m_1[0][2] = 0
            a = 0; b = 2; n_map = 1
            
        ##What about the animation for mom when player comes down for the first time?
        
    elif n_map == 1: #check if map is player house first floor
        if m_2[c][d] == 2 and a == 0 and b == 2: #check if location is staircase
            m_2[0][2] = 0
            a = 0; b = 2; n_map = 0
        elif m_2[c][d] == 2 and a == 7 and b == 2: #check if location is door to outside
            m_2[7][2] = 0
            a = 0; b = 2; n_map = 1
            print("\nNot programmed.\n") 
            
            ##What happens if player wants to leave house?
            
    map_lays[n_map][a][b] = 100 #set new position in new map to 100
    return a, b, n_map


# SUPPORTING CLASS 
#------------------------------------------------------------------------------------------------------------
class Battle:
    def __init__(self, stats):
        #stats is the increase/decrease of stats from base due to leveling up and accumulated damage from past battles
        self.no = stats[0] #number in pokedex
        
        if stats[17][0:4] == "opnt": 
            self.name = "Foe's " + pokedex[self.no][0] #opnt pokemon print name
        else:
            self.name = pokedex[self.no][0] #player or wild pokemon print name
            
        self.typ = pokedex[self.no][1] #type
        self.hp = stats[1] + pokedex[self.no][2] #hp stat
        self.atk = stats[2] + pokedex[self.no][3] #attack stat
        self.defs = stats[3] + pokedex[self.no][4] #defense stat
        self.spatk = stats[4] + pokedex[self.no][5] #special attack stat
        self.spdefs = stats[5] + pokedex[self.no][6] #special defense stat
        self.speed = stats[6] + pokedex[self.no][7] #speed stat
        self.lv = stats[7] #level
        self.move1 = stats[8:10] #move 1 [name, pp]
        self.move2 = stats[10:12] #move 2 [name, pp]
        self.move3 = stats[12:14] #move 3 [name, pp]
        self.move4 = stats[14:16] #move 4 [name, pp]
        self.moves = [self.move1, self.move2, self.move3, self.move4] #list of all moves
        self.condition = stats[16] #conditions present
        self.order = stats[17] #unique indentifier 
        self.priority = stats[18] #priority in battle 

    def create_print_stats(self):
        stats = "(LV "+str(self.lv)+") "+ self.name +'\'s hp: '+str(self.hp)+' '
        if self.condition != '': #check if there are conditions (SLP, BRN, FRZ, etc)
            print_condition = self.condition
            print_condition = print_condition.replace('fln','')
            
            if 'slp' in self.condition: #check if sleep is in conditions
                slp_index = self.condition.index('slp') + 3 #find index of moves until awake (+3 due to "slp#")
                print_condition = print_condition[:slp_index] + print_condition[slp_index+1:] #remove moves from conditon
                
            if 'con' in self.condition: #check if confusion is in conditions
                con_index = self.condition.index('con') + 3 #find index of moves until unconfused (+3 due to "con#")
                print_condition = print_condition[:con_index] + print_condition[con_index+1:] #remove moves from condition
        
            conditions_number = int(len(print_condition) / 3) #check for number of conditions
            for index in range(0,conditions_number):
                stats += '['+str.upper(print_condition[3*index : 3*(index+1)])+']' #add conditions to stats (each condition is 3 characters)

        return stats
    
    def fight(self, user_battle, opnt_current):
        #first move formatting
        move1_line1 = self.move1[0]+"\t\t\t" #format moves for printing
        move1_line2 = print_type[moves_dict[self.move1[0]][1]]+" PP "+str(self.move1[1])+"/"+str(moves_dict[self.move1[0]][5])+"\t\t"
        
        if len(move1_line1) > 16: #if first line of first move is more than 16 characters, remove 2 tabs
            move1_line1 = move1_line1.replace("\t",'',2)
        elif len(move1_line1) > 12: #if first line of first move is more than 12 characters, remove 1 tab
            move1_line1 = move1_line1.replace("\t",'',1) 
        
        #second move formatting
        move2_line1 = self.move2[0]
        move2_line2 = print_type[moves_dict[self.move2[0]][1]]+" PP "+str(self.move2[1])+"/"+str(moves_dict[self.move2[0]][5])
        
        #third move formatting
        if self.move3[0] != '': #check if pokemon has third move
            move3_line1 = self.move3[0]+"\t\t\t" #format moves for printing
            move3_line2 = print_type[moves_dict[self.move3[0]][1]]+" PP "+str(self.move3[1])+"/"+str(moves_dict[self.move3[0]][5])+"\t\t"
            
            if len(move3_line1) > 16: #if first line of third move is more than 16 characters, remove 2 tabs
                move3_line1 = move3_line1.replace("\t",'',2)
            elif len(move3_line1) > 12: #if first line of third move is more than 12 characters, remove 1 tab
                move3_line1 = move3_line1.replace("\t",'',1)            
        
        #fourth move formatting
        if self.move4[0] != '': #check if pokemon has fourth move
            move4_line1 = self.move4[0]
            move4_line2 = print_type[moves_dict[self.move4[0]][1]]+" PP "+str(self.move4[1])+"/"+str(moves_dict[self.move4[0]][5])
        
        print(' ' + move1_line1 + move2_line1) #print pokemon move options
        print(' ' + move1_line2 + move2_line2)
        if self.move3[0] != '':
            print("\n " + move3_line1 + move4_line1)
            print(' ' + move3_line2 + move4_line2 + "\n")
        
        choice = input("Input move or CANCEL (case sensitive): ") #prompt input of pokemon move or CANCEL
    
        invalid = True
        while invalid: #check if input is valid
            if choice not in self.move1+self.move2+self.move3+self.move4 and choice != "CANCEL":
                choice = input("Please try again. Input move or CANCEL (case sensitive): ")
            else:
                if (choice == str.upper(self.move1[0]) and self.move1[1] == 0) or (choice == str.upper(self.move2[0]) and self.move2[1] == 0) or \
                      (choice == str.upper(self.move3[0]) and self.move3[1] == 0) or (choice == str.upper(self.move4[0]) and self.move4[1] == 0): 
                    #check if PP == 0
                    choice = input("Move is out of PP. Input another move or CANCEL (case sensitive): ")     
                else:
                    invalid = False
            
        if choice == "CANCEL": #check if user wants to be redirected back to first start menu
            os.system('cls')
            return user_turn(self, user_battle, opnt_current)
        else:    
            for move in self.moves:
                if choice == move[0]:
                    move[1] -= 1 #subtract 1 from PP of move
        return ["fight", choice]
        
    def bag(self, user_battle, opnt_current):
        global user_bag
        
        if user_bag == []: #check if bag is empty
            print(p_name+"'s BAG is empty.\n")
            choice = str.upper(input("Please input BACK: ")) #prompt input of BACK
            while choice != "BACK": #check if input is valid
                choice = str.upper(input(p_name+"'s BAG is empty. Please input BACK: ")) 
        else:
            items_list = []
            for item in user_bag:
                print(item[0] + ' (x' + str(item[1]) + '): ' + bag_dict[item[0]][0]) #name, quantity, description
                items_list.append(item[0]) #list of item names only  
            
            choice = str.upper(input('\nPlease select an item to use or input BACK: '))
            while choice != 'BACK' and choice not in items_list: #check if input is valid
                choice = str.upper(input('Please select an item to use or input BACK: ')) 
                
        if choice == 'BACK':    
            os.system('cls')
            return user_turn(self, user_battle, opnt_current)
        else:
            print('')
            potential_targets = []
            for pokemon in user_battle: #loop process for each pokemon on team
                if pokemon.hp > 0: 
                    potential_targets.append(pokemon.name)
                    print(pokemon.create_print_stats())
                    
                ##code possibility to revive and do stuff to fainted pokemon            
                
            target = str.upper(input('\nPlease select Pokemon would you like to use ' + choice + ' on, or input BACK: '))
            while target not in potential_targets and target != 'BACK': #check if input is valid
                target = str.upper(input('Please select Pokemon would you like to use ' + choice + ' on, or input BACK: '))             
            
            if target == 'BACK':
                os.system('cls')
                return user_turn(self, user_battle, opnt_current)
            else:
                item_index = -1
                for item in user_bag:
                    item_index += 1
                    if choice == item[0]:
                        user_bag[item_index][1] -= 1 #decrease item quantity
                        
                        if user_bag[item_index][1] == 0: #if item quantity is 0 after use, remove item completely
                            user_bag.remove(user_bag[item_index])
        return ["bag", '']
                
                ##code effects of using item        
    
    def run(self, user_battle, opnt_current):
        global C
        
        if "Foe's " in opnt_current.name: 
            print(p_name + ' is unable to run away!\n')
            choice = str.upper(input('Please input BACK: ')) #prompt input of BACK
            while choice != "BACK": #check if input is valid
                choice = str.upper(input('Player is unable to run away! Please input BACK: '))  
        else:
            F = (self.speed*28)/(opnt_current.speed) + (30*C) #formula for running away
            i = randint(0,255)
            
            if i < F:
                print('Got away safely!\n')
                C = 0
                return ["run", "success"]
            else:
                print(p_name + ' failed to run away!\n')
                C += 1
                return ["run", "unsuccessful"]
            
        if choice == 'BACK':    
            os.system('cls')
            return user_turn(self, user_battle, opnt_current)  
    
    def switch_out(self, user_battle, opnt_current):
        ##What if players want to only see their pokemon's stats/summaries?
        
        available_pokemon = [] 
        for pokemon in user_battle: #loop process for each pokemon on team
            print(pokemon.create_print_stats())
            if self.name != pokemon.name and pokemon.hp > 0: 
                available_pokemon.append(pokemon.name)
                
        if available_pokemon == []: #check if all other pokemon have fainted
            choice = str.upper(input('\nNo available pokemon to switch out. Please input BACK: ')) #prompt input of BACK
            while choice != 'BACK': #check if input is valid
                choice = str.upper(input('No available pokemon to switch out. Please input BACK: ')) 
        else:
            choice = str.upper(input('\nInput Pokemon to switch in or BACK: ')) #prompt input of pokemon name or BACK
            while choice not in available_pokemon and choice != "BACK": #check if input is valid
                choice = str.upper(input('Please try again. Input Pokemon to switch in or BACK: ')) 
        
        if choice == 'BACK': #check if user wants to be redirected back to first start menu
            os.system('cls')
            return user_turn(self, user_battle, opnt_current)
    
        return ["switch", choice]
    
    def move_attack(self, attacker_battle, attacker_team, target, target_battle, attack):
        attacker = self
        paralyzed = False; frozen = False; confused = False; sleep = False 
        self_damage = 0
        
        ##What about inf (infatuation)?
        
        # 1 BEFORE MOVE CONDITION EVALUATION
        #------------------------------------------------------------------------------------ 
        if 'slp' in attacker.condition: #check if attacker's condition includes sleep
            slp_index = attacker.condition.index('slp') + 3 #find index of moves until awake
            slp_move = int(attacker.condition[slp_index])
            if slp_move == 1: #check if moves until awake is 1
                attacker.condition = attacker.condition.replace('slp1','') #remove sleep condition 
                print(attacker.name+" woke up!\n")
                sleep = False
                time.sleep(3) 
            else: 
                attacker.condition = attacker.condition[:slp_index] + str(slp_move-1) + attacker.condition[slp_index+1:] #-1 on moves before awake
                sleep = True #attacker is asleep and will be unable to attack  
            
        if 'par' in attacker.condition: #check if attacker's condition includes paralysis
            if evaluate_percent(25): #check if attacker will be paralyzed (25% chance)
                paralyzed = True #attacker is paralyzed and will be unable to attack
                
        if 'frz' in attacker.condition: #check if attacker's condition includes frozen
            if evaluate_percent(20) or moves_dict[attack][1] == 'fir': #check if attacker will be frozen (80% chance), automatic thaw with fire
                print(attacker.name+" thawed out!\n") #attacker is unfrozen
                time.sleep(3)      
                attacker.condition = attacker.condition.replace('frz','') #remove frozen condition                
            else:
                frozen = True #attacker is frozen and will be unable to attack
        
        if 'con' in attacker.condition: #check if attacker's condition includes confusion       
            con_index = attacker.condition.index('con') + 3 #find index of moves until no longer confused 
            con_move = int(attacker.condition[con_index])
            if con_move == 1: #check if moves until not confused is 1
                attacker.condition = attacker.condition.replace('con1','') #remove confusion 
                print(attacker.name+" snapped out of confusion!\n")
                time.sleep(3)    
            else: 
                attacker.condition = attacker.condition[:con_move_index] + str(con_move- 1) + attacker.condition[con_move_index+1:]
                print(attacker.name+" is confused!\n")
                time.sleep(3)                
                if evaluate_percent(50): #check if attacker will be paralyzed (50% chance)
                    confused = True #attacker is confused and will hurt itself               
        
        # 2 MOVE ELIGIBILITY AND TARGET DAMAGE/STAT CHANGE
        #------------------------------------------------------------------------------------        
        if ('fln' in attacker.condition) or (sleep == True) or (paralyzed == True) or (frozen == True) or (confused == True):
            if 'fln' in attacker.condition: 
                print(attacker.name+" flinched!\n")
                attacker.condition = attacker.condition.replace('fln','') #remove flinch
            elif sleep == True: 
                print(attacker.name+" is fast\nasleep.\n")
                time.sleep(3)
            elif paralyzed == True: 
                print(attacker.name+" is paralyzed!\nIt can't move!\n")
                time.sleep(3)
            elif frozen == True: 
                print(attacker.name+" is\nfrozen solid!\n") 
                time.sleep(3)
            
            for move in attacker.moves: 
                if move[0] == attack: 
                    move[1] += 1 #add 1 back to PP of move             
            
        else:
            print(attacker.name+" used\n"+attack+"!\n")                                                            
            time.sleep(3)         
            
            if (not evaluate_percent(moves_dict[attack][4])) and ('no_miss' not in moves_dict[attack][6]): #check whether move misses
                print(attacker.name+"'s attack missed!\n") 
                time.sleep(3)            
            else:   
                damage = attacker.attack_damage(attacker_battle, attacker_team, target, target_battle, attack) #calculate damage
                
                target.hp -= damage #target receives attack damage 
                
                if target.hp > 0 or (('stat' in moves_dict[attack][6]) and ('user' in moves_dict[attack][6] or 'hp' in moves_dict[attack][6])):
                    attacker.attack_stats(attacker_battle, attacker_team, target, target_battle, attack) #change stats/conditions based on attack 
                
                if moves_dict[attack][1] == 'fir' and 'frz' in target.condition and target.hp > 0: #fire moves remove frz from target
                    target_condition = target_condition.replace('frz','')
                    print(target.name+" thawed out!\n")        
                    time.sleep(3)                
        
        # 2 SELF DAMAGE
        #------------------------------------------------------------------------------------  
        if 'con' in attacker.condition: #check if attacker is confused and hurt itself
            print(attacker.name+" hurt itself in its confusion!\n")
            time.sleep(3)         
            
            A = attacker.lv
            B = attacker.atk
            C = 40
            D = attacker.defs
            X = 1; Y = 1; Z = randint(217,255)
            
            self_damage += math.floor(((((2*A)/5+2) * B * C / D)/50 +2)* X * Y * (Z/255)) + 1            
        
        if ('brn' in attacker.condition or 'psn' in attacker.condition): #check if attacker is burned
            if 'brn' in attacker.condition:
                print(attacker.name+" is hurt\nby its burn!\n")   
                time.sleep(3)   
            if 'psn' in attacker.condition: 
                print(attacker.name+" is hurt\nby poison!\n")   
                time.sleep(3)   
                
            for pokemon in attacker_team: 
                pokemon = Battle(pokemon)
                if attacker.order == pokemon.order:
                    base_hp = pokedex[attacker.no][2] #base hp of attacker
                    max_hp = pokemon.hp #max hp of attacker
                    break        
                
            if 'brn' in attacker.condition and 'psn' in attacker.condition:
                self_damage += int(0.25 * max_hp) #add damage to self-inflicted      
            else:
                self_damage += int(0.125 * max_hp) #add damage to self-inflicted              
        
        ##What about recoil?  
        
        attacker.hp -= self_damage #attacker receives self inflicted damage
        
        # 4 FAINT EVALUATION
        #------------------------------------------------------------------------------------              
        target_new = target.is_fainted(target_battle)           
        attacker_new = attacker.is_fainted(attacker_battle)       

        return attacker_new, target_new
    
    def attack_stats(self, attacker_battle, attacker_team, target, target_battle, attack):
        attacker = self
        
        if '+' in moves_dict[attack][6]: #check if move has more than 1 special effect
            special_fx = moves_dict[attack][6].split('+') #split special effects into a list if applicable
        else:
            special_fx = [moves_dict[attack][6]]    
        
        for effect in special_fx: #loop process for each special effect
            if effect != '': #check if move has no special effects   
                if 'stat' in effect: #check if move affects condition/stat 
                    percent_index = effect.rfind('_') #find index of special effect accuracy 
                    if evaluate_percent(int(effect[percent_index+1:])): #check if special effect hits based on accuracy 
                        
                        if 'hp' in effect: #check if effect changes hp of attacker
                            for pokemon in attacker_team: 
                                pokemon = Battle(pokemon)
                                if attacker.order == pokemon.order: #find same pokemon in new_team (full hp)
                                    base_hp = pokedex[self.no][2]
                                    max_hp = pokemon.hp #find max hp of attacker
                                    break
                            if attacker.hp < max_hp: #check if attacker is below max hp
                                amount_index = effect.index('up') + 2 #find index of amount healed ((base hp*amount*10)%)
                                attacker.hp += int(base_hp * int(effect[amount_index:percent_index])/10) 
                                
                                if attacker.hp > max_hp: #check if attacker is above max hp after healing
                                    attacker.hp = max_hp #set attacker hp to max hp                                
                        
                        elif 'atk' in effect or 'def' in effect or 'spa' in effect or 'spd' in effect or 'spe' in effect: 
                            if 'user' in effect: #check if stat change affects attacker
                                if 'dn' in effect: #check if there is a decrease in attacker stats
                                    amount_index = effect.index('dn') + 2 #find index of amount decreased 
                                    change = (1-int(effect[amount_index:percent_index])/10) #100% - amount*10% 
                                    if int(effect[amount_index:percent_index]) == 1:
                                        print(attacker.name+"'s "+stats_names[effect[10:13]]+"\nfell!\n") #10%
                                    else:
                                        print(attacker.name+"'s "+stats_names[effect[10:13]]+"\nharshly fell!\n") #>10%
                                        
                                elif 'up' in effect: #check if there is a increase in attacker stats
                                    amount_index = effect.index('up') + 2 #find index of amount increased 
                                    change = (1+int(effect[amount_index:percent_index])/10) #100% + amount*10% 
                                    if int(x[amount_index:percent_index]) == 1:
                                        print(attacker.name+"'s "+stats_names[effect[10:13]]+"\nrose!\n") #10%
                                    else:
                                        print(attacker.name+"'s "+stats_names[effect[10:13]]+"\nsharply rose!\n") #>10%

                                if 'atk' in effect: attacker.atk *= change
                                elif 'def' in effect: attacker.defs *= change
                                elif 'spa' in effect: attacker.spatk *= change
                                elif 'spd' in effect: attacker.spdefs *= change
                                elif 'spe' in effect: attacker.speed *= change  
                                time.sleep(3)
                                        
                            elif 'opnt' in effect: #check if stat change affects target
                                if 'dn' in effect: #check if there is a decrease in target stats
                                    amount_index = effect.index('dn') + 2 #find index of amount decreased 
                                    change = (1-int(effect[amount_index:percent_index])/10) #100% - amount*10% 
                                    if int(effect[amount_index:percent_index]) == 1:
                                        print(target.name+"'s "+stats_names[effect[10:13]]+"\nfell!\n") #10%
                                    else:
                                        print(target.name+"'s "+stats_names[effect[10:13]]+"\nharshly fell!\n") #>10%
                                        
                                elif 'up' in effect: #check if there is a increase in target stats
                                    amount_index = effect.index('up') + 2 #find index of amount increased
                                    change = (1+int(effect[amount_index:percent_index])/10) #100% + amount*10%   
                                    if int(effect[amount_index:percent_index]) == 1:
                                        print(target.name+"'s "+stats_names[effect[10:13]]+"\nrose!\n") #10%
                                    else:
                                        print(target.name+"'s "+stats_names[effect[10:13]]+"\nsharply rose!\n") #>10%
                                
                                if 'atk' in effect: target.atk *= change
                                elif 'def' in effect: attacker.defs *= change
                                elif 'spa' in effect: attacker.spatk *= change
                                elif 'spd' in effect: attacker.spdefs *= change
                                elif 'spe' in effect: attacker.speed *= change  
                                time.sleep(3)     
                                
                        else: #attack changes target condition
                            if 'slp' in effect: #check if move will induce sleep 
                                if 'slp' not in target.condition: #check if sleep is not already present 
                                    target.condition += ('slp'+str(randint(2,4))) #include condition and set move timer (2-4 turns)
                                    print(target.name+" fell\nasleep!\n")                                            
                                else:
                                    print(target.name+" is already asleep.\n")
                                time.sleep(3)  
                                
                            elif 'con' in effect and 'con' not in target.condition: #check if move will induce confusion
                                target.condition += ('con'+str(randint(2,4))) #include confusion and set move timer (2-4 turns) 
                                print(target.name+" is\nconfused!\n")
                                time.sleep(3)
                        
                            elif 'fln' in effect: #check if move will induce flinching
                                if 'slp' not in target.condition: #check if sleep is not present 
                                    if target.priority == 2: #check if target is going second
                                        target.condition += 'fln'   
                                        
                            elif 'psn' in effect: #check if move will induce poison
                                if 'psn' not in target.condition: #check if poison is not already present 
                                    target.condition += 'psn'
                                    print(target.name+" was poisoned!\n")                                                  
                                else:
                                    print(target.name+" is already poisoned.\n")
                                time.sleep(3)                                            
                                
                            elif 'brn' in effect:
                                if 'brn' not in target.condition: #check if burn is not already present 
                                    target.condition += 'brn'
                                    print(target.name+" was burned!\n")                                                  
                                else:
                                    print(target.name+" is already burned.\n")
                                time.sleep(3)       
                                
                            elif 'par' in effect:
                                if 'par' not in target.condition: #check if paralysis is not already present 
                                    target.condition += 'par'
                                    target.speed *= 0.5 #speed is halved
                                    print(target.name+" became paralyzed!\n")                                              
                                else:
                                    print(target.name+" is already paralyzed.\n")
                                time.sleep(3)                                      
                                
                            elif 'frz' in effect:
                                print(target.name+" was frozen solid!\n")
                                time.sleep(3)   
                                
                            else:
                                if effect[10:13] not in target.condition: #check if condition is not already present 
                                    target.condition += effect[10:13]           
        
        
    def attack_damage(self, attacker_battle, attacker_team, target, target_battle, attack):
         ##What about environmental factors?
        
        attacker = self
        combo = 1
        damage = 0
        
        if 'fury' in moves_dict[attack][6]: #check if attack has fury
            chance = randint(0,8) #3/8 chance of 2 atks, 3/8 chance of 3 atks, 1/8 chance of 4 and 5 atks
            if chance <= 3:
                combo = 2
            elif 3 < chance <= 6:
                combo = 3
            elif chance == 7:
                combo = 4
            else:
                combo = 5 
                
        for num in range(0,combo): #loop process for all attacks (should only loop for fury)
            C = moves_dict[attack][3] #C = base power of move
            Z = randint(217,255) #Z = random integer between 217 and 255
            
            if 'crit' in moves_dict[attack][6]: #check if crit is listed as a special effect
                crit_percent_index = moves_dict[attack][6].rfind('_') + 1 #find index of new critical percent chance
                crit = evaluate_percent(float(moves_dict[attack][6][crit_percent_index:]))
            else: 
                crit = evaluate_percent(6.25) #A = level of attacker; can be doubled on critical hit (normally 6.25% chance)
                
            if moves_dict[attack][2] != 'sta' and crit == True: #no criticals for status only moves
                print("A critical hit!\n")
                time.sleep(3)
                A = 2*attacker.lv #A = level of attacker
            else:
                A = attacker.lv
            
            if moves_dict[attack][2] == 'phy': #B = atk or sp.atk of attacker, D = def or sp.def of target
                B = attacker.atk    
                D = target.defs
            elif moves_dict[attack][2] == 'spc':
                B = attacker.spatk
                D = target.spdefs
            
            if moves_dict[attack][1] in attacker.typ: X = 1.5 #X = same type attack bonus (type of attacker = type of move)
            else: X = 1 
             
            Y = 1 #Y = type multiplier based on attack's type and target type 
            if '+' in target.typ: #check if target has more than one type
                target_type_list = target.typ.split('+') #split target's types into a list if applicable
            else:
                target_type_list = [target.typ]
                
            for typ in target_type_list: 
                if moves_dict[attack][2] == 'sta': Y = 1 #no bonus for status only moves
                elif typ in super_effective[moves_dict[attack][1]]: Y *= 2 #check if move is super effective (x2)                  
                elif typ in not_effective[moves_dict[attack][1]]: Y *= 0.5 #check if move is not very effective (x0.5)                      
                elif typ in immune[moves_dict[attack][1]]: Y *= 0 #check if move does no damage (x0)                       
                else: Y *= 1   

            if Y == 0: 
                print("It doesn't affect "+target.name+".\n") 
                time.sleep(3) 
            elif Y > 1: 
                print("It's super effective!\n")     
                time.sleep(3) 
            elif Y < 1: 
                print("It's not very effective...\n")
                time.sleep(3)  
                
            if moves_dict[attack][2] != 'sta': #check if move is not status only
                damage += math.floor(((((2*A)/5+2) * B * C / D)/50 +2)* X * Y * (Z/255)) + 1
                if 'brn' in attacker.condition and moves_dict[attack][2] != 'phy': #check if attacker is burned and move is physical 
                    damage = math.floor(damage * 0.5) + 1
                
            return damage
    
    def is_fainted(self, pokemon_battle):
        new = '' 
        if self.hp <= 0: #check if pokemon has less than or equal to 0 hp   
            self.hp = 0 #set pokemon hp to 0 if fainted
            self.condition = '' #remove all conditions  
            print(self.name+" fainted!\n")
            time.sleep(3)
            
            available_pokemon = []
            available_names = []
            for pokemon in pokemon_battle: #loop process for each pokemon on team
                if self.name != pokemon.name and pokemon.hp > 0: 
                    available_pokemon.append(pokemon) #add names to list if not fainted or not current pokemon 
                    available_names.append(pokemon.name)
            
            if available_pokemon == []: #check if all other pokemon have fainted
                new = None #no more pokemon available
            else:
                if self.order[0:4] == 'user': #show stats and allow user to choose next pokemon
                    print("Available Pokemon:")
                    for pokemon in available_pokemon: #loop process for all not fainted pokemon
                        print(pokemon.create_print_stats())
                        
                    new = str.upper(input("\nInput your next Pokemon: ")) #prompt input of pokemon name
                    while new not in available_names: #check if input is valid
                        new = str.upper(input("Please try again. Input your next Pokemon: ")) 
                    print('')
                    
                else:
                    i = randint(0, len(available_names)-1) #random number generator
                    new = available_names[i] #randomly choose a pokemon
        return new
        

# SUPPORTING FUNCTIONS
#------------------------------------------------------------------------------------------------------------
def print_stats(user, opnt): 
    print(40*'*' + '\n\n' + opnt.create_print_stats() + '\n' + user.create_print_stats() + '\n\n' + 40*'*' + '\n')

def evaluate_percent(percent):
    if type(percent) == float: #check if input is a float
        percent = round(percent,2) * 100 #round percent to two decimal places and * 100
        random_num = randint(0, 10000) #find random number between 0 and 10000
        if random_num <= percent: #check if number is in range of percent
            return True
        else:
            return False
    else:
        random_num = randint(0, 100) #find random number between 0 and 100
        if random_num <= percent: #check if number is in range of percent
            return True
        else:
            return False

def user_turn(user_current, user_battle, opnt_current):
    print_stats(user_current, opnt_current)
    
    print("What will "+user_current.name+" do?")
    
    print("\n-------------------------------------")
    print("|                                   |")
    print("|                                   |")
    print("|               FIGHT               |")
    print("|                                   |")
    print("|                                   |")
    print("-------------------------------------")
    print("|    BAG    |    RUN    |  POKEMON  |")
    print("-------------------------------------")
    
    choice = str.upper(input("\nInput FIGHT, BAG, RUN, or POKEMON: ")) #prompt input of FIGHT or SWITCH OUT
    
    while choice != "FIGHT" and choice != "BAG" and choice != "RUN" and choice != "POKEMON": #check if input is valid
        choice = str.upper(input("Please try again. Input FIGHT, BAG, RUN, or POKEMON: "))
    os.system('cls')    
    print_stats(user_current, opnt_current)
    
    if choice == "FIGHT": #check if user wants to access moves
        result = user_current.fight(user_battle, opnt_current)
    elif choice == 'BAG': #check if user wants to access bag
        result = user_current.bag(user_battle, opnt_current)
    elif choice == 'RUN': #check if user wants to run away
        result = user_current.run(user_battle, opnt_current)        
    elif choice == 'POKEMON': #check if user wants to access pokemon/switch out
        result = user_current.switch_out(user_battle, opnt_current)   
        
    return result

def opnt_turn(opnt_current):
    ##What if opnt wants to access their bag or switch out?
    
    i = randint(0, 3) #random integer between and including 0 to 3
    opnt_choice = opnt_current.moves[i][0] #randomly select a move for opnt_move
    
    while (opnt_choice == opnt_current.move1[0] and opnt_current.move1[1] == 0) or \
          (opnt_choice == opnt_current.move2[0] and opnt_current.move2[1] == 0) or \
          (opnt_choice == opnt_current.move3[0] and opnt_current.move3[1] == 0) or \
          (opnt_choice == opnt_current.move4[0] and opnt_current.move4[1] == 0): #check PP of move
        i = randint(0, 3) #
        opnt_choice = opnt_current.moves[i][0]

    for move in opnt_current.moves:
        if opnt_choice == move[0]:
            move[1] -= 1 #subtract 1 from PP of move     
            
    return ['fight', opnt_choice]

def priority(user_current, opnt_current, user_choice, opnt_choice):
    if user_choice[0] == 'run' and user_choice[1] == 'sucessful': #automatic battle end
        pass
    elif user_choice[0] == 'run' and user_choice[1] == 'unsucessful': #automatic lost turn
        user_current.priority = 2
        opnt_current.priority = 1
    elif user_choice[0] == 'bag' or user_choice[0] == 'switch': #automatic priority for player
        user_current.priority = 1
        opnt_current.priority = 2        
    else:
        if 'first' in moves_dict[user_choice[1]][6] and 'first' in moves_dict[opnt_choice[1]][6]: #check if both player and opnt moves have priority
            if user_current.speed > opnt_current.speed: #compare speeds
                user_current.priority = 1
                opnt_current.priority = 2                    
        elif 'first' in moves_dict[user_choice[1]][6]: #automatic priority for player
            user_current.priority = 1
            opnt_current.priority = 2                
        elif 'first' in moves_dict[opnt_choice[1]][6]: #automatic priority for opnt
            user_current.priority = 2
            opnt_current.priority = 1           
        else:
            if user_current.speed > opnt_current.speed: #compare speeds
                user_current.priority = 1
                opnt_current.priority = 2
                
def process_move(user_info, opnt_info, user_choice, opnt_choice, msg, stage):
    [user_battle, user_team, user_current] = user_info 
    [opnt_battle, opnt_team, opnt_current] = opnt_info  
    
    print_stats(user_current, opnt_current)
    
    if (user_current.priority == 1 and stage == 1) or (user_current.priority == 2 and stage == 2):
        if user_choice[0] == 'bag' or user_choice[0] == 'run':
            user_new = '' #no damage attack during this turn, no fainting
            opnt_new = '' #no damage attack during this turn, no fainting
            
        elif user_choice[0] == 'switch':
            for new in user_battle: #find replacment pokemon in user_battle record
                if user_choice[1] == new.name: 
                    user_current.priority = '' #remove priority indicator
                    
                    print(user_current.name+", switch out!\nCome back!\n")
                    time.sleep(3)                      
                    user_current = new #switch out old user_current for new
                    user_current.priority = 1 #reattach priority indicator
                    print("Go! "+user_current.name+"!\n")
                    time.sleep(3)
                    
                    user_new = '' #no damage attack during this turn, no fainting
                    opnt_new = '' #no damage attack during this turn, no fainting
                    break   
        else: #user attacks
            user_new, opnt_new = user_current.move_attack(user_battle, user_team, opnt_current, opnt_battle, user_choice[1])
            
    elif (opnt_current.priority == 1 and stage == 1) or (opnt_current.priority == 2 and stage == 2):
        if opnt_choice[0] == 'bag':
            user_new = '' #no damage attack during this turn, no fainting
            opnt_new = '' #no damage attack during this turn, no fainting
            
        elif opnt_choice[0] == 'switch':
            for new in opnt_battle: #find replacment pokemon in user_battle record
                if opnt_choice[1] == new.name: 
                    opnt_current.priority = '' #remove priority indicator
                    
                    print(msg[1]+' withdrew '+opnt_current.name+'!\n')
                    time.sleep(3)                      
                    opnt_current = new #switch out old user_current for new
                    opnt_current.priority = 1 #reattach priority indicator
                    print(msg[1]+' sent out '+opnt_current.name+'!\n')
                    time.sleep(3)
                    
                    user_new = '' #no damage attack during this turn, no fainting
                    opnt_new = '' #no damage attack during this turn, no fainting
                    break           
        else: #opnt attacks
            opnt_new, user_new = opnt_current.move_attack(opnt_battle, opnt_team, user_current, user_battle, opnt_choice[1])   
    
    fainted = []
    if user_new != '':
        fainted.append('user')
    if opnt_new != '':
        fainted.append('opnt')
    
    user_info = [user_battle, user_team, user_current]
    opnt_info = [opnt_battle, opnt_team, opnt_current]  
        
    battle_incomplete, winner, user_current, opnt_current = stage_result(user_info, user_new, opnt_info, opnt_new, msg) #result of this stage
       
    user_info = [user_battle, user_team, user_current]
    opnt_info = [opnt_battle, opnt_team, opnt_current]  
       
    return user_info, opnt_info, battle_incomplete, winner, fainted

def stage_result(user_info, user_new, opnt_info, opnt_new, msg):
    [user_battle, user_team, user_current] = user_info
    [opnt_battle, opnt_team, opnt_current] = opnt_info     
    
    if user_new == None: #check if user is out of pokemon
        os.system('cls')
        print_stats(user_current, opnt_current)
        
        print(p_name+" is out of\nusable Pokemon!\n")
        time.sleep(3)
        print(p_name+" dropped $40\nin panic!\n")
        time.sleep(3)
        print("... ... ... ...\n")
        time.sleep(3)
        print(p_name+" blacked out!\n")
        time.sleep(4)
        os.system('cls')
        
        print('\n'+p_name+" scurried back\nhome, protecting the exhausted and fainted Pokemon from futher\nharm...")
        time.sleep(6)
        battle_incomplete = False #battle is finished
        winner = 'opnt' #player loses
    
    elif opnt_new == None: #check if opnt is out of pokemon
        os.system('cls')
        print_stats(user_current, opnt_current)
        
        print("Player defeated\n"+msg[1]+"!\n")
        time.sleep(3)
        print(msg[4]+"\n")
        time.sleep(msg[5])
        print(p_name+" got $100\nfor winning!")
        time.sleep(4)
        battle_incomplete = False #battle is finished
        winner = 'user' #player loses
    
    else:
        battle_incomplete = True #battle is not finished
        winner = None #no one wins    
        
        if user_new != '': #check if there is a new user pokemon bc old one fainted
            for pokemon in user_battle: 
                if user_new == pokemon.name:
                    priority = user_current.priority #remember priority of old pokemon
                    user_current.priority = '' #remove priority indicator
                                       
                    user_current = pokemon #switch out old user_current for new
                    user_current.priority = priority #reattach priority indicator
                    print("Go! "+user_current.name+"!\n")
                    time.sleep(3)
                    break                       
                    
        if opnt_new != '': #check if there is a new opnt pokemon bc old one fainted
            for pokemon in opnt_battle: #loop process for each pokemon in opnt's battle team
                if opnt_new == pokemon.name: #check if current pokemon name matches name of pokemon in opnt's battle team
                    priority = opnt_current.priority
                    opnt_current.priority = '' #remove priority indicator
                    
                    opnt_current = pokemon
                    opnt_current.priority = priority
                    print(msg[1]+" sent out "+pokedex[opnt_current.no][0]+"!\n")
                    time.sleep(3)  
                    break  
    
    return battle_incomplete, winner, user_current, opnt_current             


# MAIN FUNCTION
#------------------------------------------------------------------------------------------------------------
def battle_main(p, previous_team, msg, new_team = new_team):
    global p_name
    
    opnt_battle = [] #create list of opnt pokemon team stats for this battle
    user_battle = [] #create list of player pokemon team stats for this battle
    
    with open("Pokemon_Global.txt","r") as file:
        name = file.readline().replace('\n','')    
    p_name = name

    ##What about wild pokemon?

    for pokemon in opponents[p]: #loop for all pokemon in opponent team
        opnt_battle.append(Battle(pokemon)) #create battle team stats from scratch   
    
    if previous_team == []: #check for previous battle history
        for pokemon in new_team:
            user_battle.append(Battle(pokemon)) #create battle team stats from scratch
    else:
        for pokemon in previous_team:        
            user_battle.append(Battle(pokemon)) #create battle team stats from battle history
    
    opnt_current = opnt_battle[0] #opnt's first pokemon will always be at full stats so first=current
        
    for pokemon in user_battle: #player's first pokemon will be the first not fainted pokemon in team
        user_current = pokemon
        if user_current.hp > 0:
            break    
    
    os.system('cls')
    print("You are challenged by "+msg[1]+"!")
    time.sleep(3)
    print(msg[1]+" sent out "+pokedex[opnt_current.no][0]+"!")
    time.sleep(3)
    print("Go! "+user_current.name+"!\n")
    time.sleep(3)
    os.system('cls')
    
    battle_incomplete = True
    user_info = [user_battle, new_team, user_current]
    opnt_info = [opnt_battle, opponents[p], opnt_current]
    
    while battle_incomplete:
        [user_battle, new_team, user_current] = user_info 
        [opnt_battle, opponents[p], opnt_current] = opnt_info         
        
        user_choice = user_turn(user_current, user_battle, opnt_current) #user turn
        opnt_choice = opnt_turn(opnt_current) #opponent turn
       
        time.sleep(1)
        os.system('cls')          
        
        priority(user_current, opnt_current, user_choice, opnt_choice) #establishes .priority 
        
        stage = 1 #first move is processed
        user_info, opnt_info, battle_incomplete, winner, fainted = process_move(user_info, opnt_info, user_choice, opnt_choice, msg, stage)  
        
        if battle_incomplete:
            os.system('cls')  
            stage += 1 #second move is processed
            if 'user' in fainted:
                user_choice[0] = 'bag' #with fainted pokemon, user loses turn (bag does nothing)
            if 'opnt' in fainted:
                opnt_choice[0] = 'bag' #with fainted pokemon, opnt loses turn (bag does nothing)       
            
            user_info, opnt_info, battle_incomplete, winner, fainted = process_move(user_info, opnt_info, user_choice, opnt_choice, msg, stage)  
            os.system('cls') 
    
    previous_team = []
    for self in user_battle:
        previous_team.append([self.no, self.hp-pokedex[self.no][2], self.atk-pokedex[self.no][3], self.defs-pokedex[self.no][4], 
                              self.spatk-pokedex[self.no][5], self.spdefs-pokedex[self.no][6], self.speed-pokedex[self.no][7], 
                              self.lv] + self.move1 + self.move2 + self.move3 + self.move4 + [self.condition, self.order, ''])
    
    return winner, previous_team


# TESTER FUNCTIONS
#------------------------------------------
def start():
    global p_name
    print("----------------------------------------\n")
    print(" W E L C O M E   T O   P O K E M O N ! \n")
    print("----------------------------------------") 
    time.sleep(1)
    print("\nWelcome to the world of Pokemon!\n")
    time.sleep(3)
    print("My name is Professor Oak.\n")
    time.sleep(2)    
    print("But everyone calls me the\nPokemon Professor.\n")
    time.sleep(3)
    print("Before we go any any further, I'd like to tell you a few things you should\nknow about this world!\n")
    time.sleep(4)
    print("This world is widely inhabited by creatures known as Pokemon.\n")
    time.sleep(4)
    print("We humans live alongside Pokemon\nas friends.\n")
    time.sleep(3)
    print("At times we play together, and at\nother times we work together.\n")
    time.sleep(4)    
    print("Some people use their Pokemon to\nbattle and develop closer bonds\nwith them.\n")
    time.sleep(5)    
    os.system('cls')
    print("Now, why don't you tell me a little\nabout yourself?\n")
    time.sleep(3) 
    gender = sex()
    p_name = name()
    time.sleep(1) 
    os.system('cls')
    print(p_name+"!\nAre you ready?\n")
    time.sleep(2)    
    print("Your very own tale of grand adventure\nis about to unfold.\n")
    time.sleep(3)
    print("Fun experiences, difficult experiences,\nthere's so much waiting for you!\n")
    time.sleep(4)    
    print("Dreams! Adventure! Let's go to the world of Pokemon!\n")
    time.sleep(4)
    print("I'll see you later!\n")
    time.sleep(2)    
    print("*cue whoosing sound*")
    time.sleep(3)
    
    os.system('cls')
    a = 3; b = 4; n_map = 0 #orient player position to row 3, column 4 in player house second floor
    m_1[3][4] = 100 #set player position as 100
    user_current = [] #set no data for user's current pokemon team
    print(m_1)   
    print("\n0 = open space")
    print("1 = uninteractable object")
    print("2 = map transitions")
    print("100 = player")
    time.sleep(1)
    print("\nUse arrow keys to move around.")
    
    step(a, b, n_map, user_current)

def test_all_but_intro():
    global p_name
    a = 3; b = 4; n_map = 0 #orient player position to row 3, column 4 in player house second floor
    m_1[3][4] = 100 #set player position as 100
    user_current = [] #set no data for user's current pokemon team
    print(m_1)   
    print('')
    p_name = name()
    print("0 = open space")
    print("1 = uninteractable object")
    print("2 = map transitions")
    print("100 = player")
    time.sleep(1)
    print("\nUse arrow keys to move around.")
    step(a, b, n_map, user_current)

def test_battle():
    global p_name
    msg = ["battle", "True Blue", "Boundless!", 2, "You are BOUNDLESS!!!", 3]
    p = 100
    p_name = 'Daniel'
    previous_team = []
    
    print(battle_main(p, previous_team, msg))
    A = input()