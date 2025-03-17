import numpy as np
from random import randint
import os
import time
import msvcrt
import math

# MAPS AND OBJECTS
#------------------------------------------

#create map of second floor of player house (7x10)
m_1 = np.array([[1,2,0,0,0,5,1,4,3,3], 
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,6,0,0,0,0,0,0,0,0],
                [0,6,0,0,0,0,0,0,0,1]])

#create map of first floor of player house (9x11)
m_2 = np.array([[1,2,0,0,3,3,1,7,7,8,9], 
                [0,0,0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,1,1,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,101,1,1,0,0,0],
                [0,0,0,0,0,0,1,1,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [1,0,0,103,0,0,0,0,0,0,1],
                [1,1,2,1,1,1,1,1,1,1,1]])

#dict of all maps
map_lays = [m_1, m_2] 

#dict of enviornments for all map indexes
environment_decider = {0:"building", 1:"building"} 

#dict for objects in player house
d_1 = {3 : "This is a TV.", 4 : "This is a Wii.", 
       5 : "This is a gaming laptop.", 6 : "A  warm bed.",
       7 : "Ouch! That's hot!", 8 : "A layer of dust covers the bookshelf.",
       9 : "Empty, except a half-finished bottle of vodka.", 101 : "Mom: Hello.", 
       103 : ["battle", "True Blue", "True Blue: Boundless!", 2, "True Blue: You are BOUNDLESS!!!", 3]} 

#dict of all objects in each map
dict_lays = [d_1, d_1] 

#dict for dialogue after defeating trainers
post_battle_msg = {103 : ["\nTrue Blue: Well done! You truly enbody\nthe UofT spirit!\n", "True Blue: Good luck with your studies!"]}

#dict for replacing battle messages
replace_battle_msg = {103 : "True Blue: You've already beaten me!"}

# DATABASE INFORMATION
#------------------------------------------

#dict of pokemon in form [name, type, hp, atk, def, sp.atk, sp.def, speed] <- base stats
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

#dict of bag items [description, effect]
bag_dict = {"Burn Heal": ['Blah', 'rem_brn'],
             "Chesto Berry": ['Blah', 'rem_slp']}


# VARIABLE INFORMATION
#------------------------------------------

# dict of all opponents' teams in form [pokedex #, hp, atk, def, sp.atk, sp.def, speed, lv, 4*[moves, PP], condition]
# Note: no duplicate pokemon or duplicate moves for each pokemon allowed
opponents = {103 : [[248, 50, 20, 20, 20, 20, 10, 40, 'Ice Fang', moves_dict['Ice Fang'][5], 'Flame Wheel', moves_dict['Flame Wheel'][5],
                     'Sleep Powder', moves_dict['Sleep Powder'][5],'Twister', moves_dict['Twister'][5], ''], #248
             
                    [22, 20, 10, 10, 10, 10, 10, 15, 'Growl', moves_dict['Growl'][5], 'Quick Attack', moves_dict['Quick Attack'][5],
                     'Stun Spore', moves_dict['Stun Spore'][5],'Synthesis', moves_dict['Synthesis'][5], '']]}

# player team in form [pokedex #, hp, atk, def, sp.atk, sp.def, speed, lv, 4*[moves, PP], condition] <- bonus stats
# Note: no duplicate pokemon or duplicate moves for each pokemon allowed
user_team = [[3, 20, 20, 20, 20, 20, 20, 35, 'Crunch', moves_dict['Crunch'][5], 'Poison Powder', moves_dict['Poison Powder'][5], 
              'Magical Leaf', moves_dict['Magical Leaf'][5], 'Fury Attack', moves_dict['Fury Attack'][5], ''],
             
             [130, 0, 0, 0, 0, 0, 0, 25, 'Flame Wheel', moves_dict['Flame Wheel'][5], 'Scratch', moves_dict['Scratch'][5], 
              'Bite', moves_dict['Bite'][5], 'Will-O-Wisp', moves_dict['Will-O-Wisp'][5], '']]

user_bag = [["Burn Heal", 1], ["Chesto Berry", 2]]

##What about exp and money?

# checkpoint for player defeat
checkpoint_row = 3; checkpoint_col = 4; checkpoint_map = 0


# INTRODUCTION FUNCTIONS
#------------------------------------------
def sex():
    gender = str.upper(input("Are you a boy?\nOr are you a girl? "))
    print('')
    if gender == "BOY" or gender == "GIRL": 
        ans = str.upper(input("So you are a "+gender+" then? "))
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
    print('')
    ans = str.upper(input("Your name is "+p_name+"? "))
    print('')
    if ans == "YES": 
        time.sleep(1)
        return p_name
    else: 
        return name()


# MOVEMENT FUNCTIONS
#------------------------------------------
def step(a, b, n_map, user_current): 
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
            return step(a, b, n_map, user_current) #retry
    
    elif direction == "b'K'": #check if direction is left
        if b-1 >= 0: #check if movement passes over left boundary of map
            c = a
            d = b-1 #left is valid
        else:
            os.system('cls')
            print(map_lays[n_map])       
            return step(a, b, n_map, user_current) #retry
        
    elif direction == "b'H'": #check if direction is up
        if a-1 >= 0: #check if movement passes over upper boundary of map
            c = a-1 #up is valid
            d = b
        else:      
            os.system('cls')
            print(map_lays[n_map])
            return step(a, b, n_map, user_current) #retry
        
    elif direction == "b'P'": #check if direction is down
        if a+1 < len(a_max): #check if movement passes over lower boundary of map
            c = a+1 #down is valid
            d = b
        else:
            os.system('cls')
            print(map_lays[n_map])         
            return step(a, b, n_map, user_current) #retry
    else:
        os.system('cls')
        print(map_lays[n_map])    
        return step(a, b, n_map, user_current) #retry
    
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
                    player_win, user_current = battle_intro(p, user_team, user_current, msg) #initiate battle sequence   
                    
                    if player_win == True: #check if player won battle
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
                        
                        os.system('cls')
                        print(map_lays[checkpoint_map])
                        return step(checkpoint_row, checkpoint_col, checkpoint_map, user_current) #relocate to checkpoint
                else:
                    print('\n'+msg)
                
        return step(a, b, n_map, user_current) #loop to beginning again
    else:
        map_lays[n_map][a][b] = 0 #set old position to 0
        map_lays[n_map][c][d] = 100 #set new position to 100
        
        os.system('cls')
        print(map_lays[n_map])
        return step(c, d, n_map, user_current) #retry   
    
    
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


# BATTLE - TURNS AND PRINTING STATS
#------------------------------------------
def print_stats(u_pokemon, o_pokemon):
    # 1 OPNT STATS
    #------------------------------------------------------------------------------------    
    if 'slp' in o_pokemon[17]: #check if sleep is in opnt conditions
        slp_move_index = o_pokemon[17].index('slp') + 3 #find index of moves until awake
        slp_move = o_pokemon[17][slp_move_index] #remember number of moves until awake
        o_pokemon[17] = o_pokemon[17][:slp_move_index] + o_pokemon[17][slp_move_index+1:] #remove number of moves
        
    if 'con' in o_pokemon[17]: #check if confusion is in opnt conditions
        con_move_index = o_pokemon[17].index('con') + 3 #find index of moves until not confused
        con_move = o_pokemon[17][con_move_index] #remember number of moves until not confused
        o_pokemon[17] = o_pokemon[17][:con_move_index] + o_pokemon[17][con_move_index+1:] #remove number of moves 
      
    if o_pokemon[17] == '': #check if no conditions (SLP, BRN, FRZ, etc)
        opnt_stats = "(LV "+str(o_pokemon[8])+") "+o_pokemon[0]+'\'s hp: '+str(o_pokemon[2]) #set hp of opponent pokemon and condition
    else:
        if len(o_pokemon[17]) > 3: #check if there are more than two conditions
            opnt_stats = "(LV "+str(o_pokemon[8])+") "+o_pokemon[0]+'\'s hp: '+str(o_pokemon[2])+' ['+ \
                  str.upper(o_pokemon[17][0:3])+']['+str.upper(o_pokemon[17][3:6])+']'  
        else:
            opnt_stats = "(LV "+str(o_pokemon[8])+") "+o_pokemon[0]+'\'s hp: '+str(o_pokemon[2])+' ['+ \
                  str.upper(o_pokemon[17][0:3])+']'
    
    if 'con' in o_pokemon[17]:
        o_pokemon[17] = o_pokemon[17][:con_move_index] + con_move + o_pokemon[17][con_move_index:] #reattach moves             
    if 'slp' in o_pokemon[17]:
        o_pokemon[17] = o_pokemon[17][:slp_move_index] + slp_move + o_pokemon[17][slp_move_index:] #reattach moves 
      
    # 2 USER STATS
    #------------------------------------------------------------------------------------       
    if 'slp' in u_pokemon[17]: #check if sleep is in opnt conditions
        slp_move_index = u_pokemon[17].index('slp') + 3 #find index of moves until awake
        slp_move = u_pokemon[17][slp_move_index] #remember number of moves until awake
        u_pokemon[17] = u_pokemon[17][:slp_move_index] + u_pokemon[17][slp_move_index+1:] #remove number of moves 
        
    if 'con' in u_pokemon[17]: #check if confusion is in opnt conditions
        con_move_index = u_pokemon[17].index('con') + 3 #find index of moves until not confused
        con_move = u_pokemon[17][con_move_index] #remember number of moves until not confused
        u_pokemon[17] = u_pokemon[17][:con_move_index] + u_pokemon[17][con_move_index+1:] #remove number of moves 
        
    if u_pokemon[17] == '': #check if no conditions (SLP, BRN, FRZ, etc)
        user_stats = "\n(LV "+str(u_pokemon[8])+") "+u_pokemon[0]+'\'s hp: '+str(u_pokemon[2]) #set hp of user pokemon and condition 
    else:
        if len(u_pokemon[17]) > 3: #check if there are more than two conditions
            user_stats = "\n(LV "+str(u_pokemon[8])+") "+u_pokemon[0]+'\'s hp: '+str(u_pokemon[2])+ \
                  ' ['+str.upper(u_pokemon[17][0:3])+']['+str.upper(u_pokemon[17][3:6])+']'  
        else:
            user_stats = "\n(LV "+str(u_pokemon[8])+") "+u_pokemon[0]+'\'s hp: '+str(u_pokemon[2])+ \
                  ' ['+str.upper(u_pokemon[17][0:3])+']'     
    
    if 'con' in u_pokemon[17]:
        u_pokemon[17] = u_pokemon[17][:con_move_index] + con_move + u_pokemon[17][con_move_index:] #reattach moves    
    if 'slp' in u_pokemon[17]:
        u_pokemon[17] = u_pokemon[17][:slp_move_index] + slp_move + u_pokemon[17][slp_move_index:] #reattach moves 
        
    return print('****************************************\n\n'+opnt_stats+'\n'+user_stats+'\n\n****************************************\n')


def user_turn(u_pokemon, user_battle, o_pokemon):
    print_stats(u_pokemon, o_pokemon)
    
    print("What will "+u_pokemon[0]+" do?")
    
    print("\n-------------------------------------")
    print("|                                   |")
    print("|               FIGHT               |")
    print("|                                   |")
    print("-------------------------------------")
    print("|    BAG    |    RUN    |  POKEMON  |")
    print("-------------------------------------")
    
    user_move = input("\nInput FIGHT, BAG, RUN, or POKEMON (case sensitive): ") #prompt input of FIGHT or SWITCH OUT
    
    while user_move != "FIGHT" and user_move != "BAG" and user_move != "RUN" and user_move != "POKEMON": #check if input is valid
        user_move = input("Please try again. Input FIGHT, BAG, RUN, or POKEMON (case sensitive): ")
    os.system('cls')
    
    # 1 INITIATE FIGHT
    #------------------------------------------------------------------------------------   
    print_type = {'nor':'NORMAL', 'fir':'FIRE', 'fgt':'FIGHT', 'wat':'WATER', 'fly':'FLY', 'gra':'GRASS', 'poi':'POISON', 'ele':'ELECTRIC', \
                  'gro':'GROUND', 'psy':'PSYCHIC', 'rck':'ROCK', 'ice':'ICE', 'bug':'BUG', 'drg':'DRAGON', 'gho':'GHOST', 'dar':'DARK', \
                  'ste':'STEEL'}
    
    if user_move == "FIGHT": #check if user wants to access moves
        first_move_line_1 = u_pokemon[9]+"\t\t\t" #format moves for printing
        first_move_line_2 = print_type[moves_dict[u_pokemon[9]][1]]+" PP "+str(u_pokemon[10])+"/"+str(moves_dict[u_pokemon[9]][5])+"\t\t"
        second_move_line_1 = u_pokemon[11]
        second_move_line_2 = print_type[moves_dict[u_pokemon[11]][1]]+" PP "+str(u_pokemon[12])+"/"+str(moves_dict[u_pokemon[11]][5])
        third_move_line_1 = u_pokemon[13]+"\t\t\t"
        third_move_line_2 = print_type[moves_dict[u_pokemon[13]][1]]+" PP "+str(u_pokemon[14])+"/"+str(moves_dict[u_pokemon[13]][5])+"\t\t"
        fourth_move_line_1 = u_pokemon[15]
        fourth_move_line_2 = print_type[moves_dict[u_pokemon[15]][1]]+" PP "+str(u_pokemon[16])+"/"+str(moves_dict[u_pokemon[15]][5])
        
        if len(first_move_line_1) > 16: #if first line of the first move is more than 16 characters, remove 2 tabs
            first_move_line_1 = first_move_line_1.replace("\t",'',2)
        elif len(first_move_line_1) > 12: #if first line of the first move is more than 12 characters, remove 1 tab
            first_move_line_1 = first_move_line_1.replace("\t",'',1)
            
        if len(third_move_line_1) > 16: #if first line of the third move is more than 16 characters, remove 2 tabs
            third_move_line_1 = third_move_line_1.replace("\t",'',2)
        elif len(third_move_line_1) > 12: #if first line of the third move is more than 12 characters, remove 1 tab
            third_move_line_1 = third_move_line_1.replace("\t",'',1)
        
        print_stats(u_pokemon, o_pokemon)
        
        print(' ' + first_move_line_1 + second_move_line_1) #print pokemon move options
        print(' ' + first_move_line_2 + second_move_line_2)
        print("\n " + third_move_line_1 + fourth_move_line_1)
        print(' ' + third_move_line_2 + fourth_move_line_2 + "\n")
        
        user_move = input("Input move or CANCEL (case sensitive): ") #prompt input of pokemon move or CANCEL
    
        while user_move not in u_pokemon and user_move != "CANCEL": #check if input is valid
            user_move = input("Please try again. Input move or CANCEL (case sensitive): ")
            
        while (user_move == u_pokemon[9] and u_pokemon[10] == 0) or (user_move == u_pokemon[11] and u_pokemon[12] == 0) or \
              (user_move == u_pokemon[13] and u_pokemon[14] == 0) or (user_move == u_pokemon[15] and u_pokemon[16] == 0): #check PP of move
            user_move = input("Move is out of PP. Input another move or CANCEL (case sensitive): ")    
            
        if user_move == "CANCEL": #check if user wants to be redirected back to first start menu
            os.system('cls')
            return user_turn(u_pokemon, user_battle, o_pokemon) 
        else:    
            pp_index = u_pokemon.index(user_move) + 1 
            u_pokemon[pp_index] -= 1 #subtract 1 from PP of move
            new = u_pokemon[0] #keep current pokemon  
            
    # 2 INITIATE BAG
    #------------------------------------------------------------------------------------    
    elif user_move == 'BAG': #check if user wants to access bag
        print_stats(u_pokemon, o_pokemon)
        global user_bag
        
        if user_bag == []:
            print(p_name+"'s BAG is empty.\n")
            choice = input("Please input BACK (case sensitive): ") #prompt input of BACK
            while choice != "BACK": #check if input is valid
                choice = input(p_name+"'s BAG is empty. Please input BACK (case sensitive): ") 
        else:
            for item in user_bag:
                print(item[0] + ' (x' + str(item[1]) + '): ' + bag_dict[item[0]][0]) 
            print()
            
            items_list = []
            for item in user_bag:
                items_list.append(item[0])             
                
            choice = input('Please select an item to use or input BACK (case sensitive): ')
            while choice != 'BACK' and choice not in items_list: #check if input is valid
                choice = input('Please select an item to use or input BACK (case sensitive): ') 
                
        if choice == 'BACK':    
            os.system('cls')
            return user_turn(u_pokemon, user_battle, o_pokemon) 
        else:
            os.system('cls')
            
            names = [] #create list of switchable pokemon names
            available = [] #create list of switchable pokemon names and stats
             
            for x in user_battle: #loop process for each pokemon on team
                if x[2] > 0: 
                    names.append(x[0])
                    condition = x[17]
                    
                    if 'slp' in x[17]: #check if sleep is in opnt conditions
                        slp_move_index = x[17].index('slp') + 3 #find index of moves until awake
                        slp_move = x[17][slp_move_index] #remember number of moves until awake
                        condition = x[17][:slp_move_index] + x[17][slp_move_index+1:] #remove number of moves
                        
                    if 'con' in x[17]: #check if confusion is in opnt conditions
                        con_move_index = x[17].index('con') + 3 #find index of moves until not confused
                        con_move = x[17][con_move_index] #remember number of moves until not confused
                        condition = x[17][:con_move_index] + x[17][con_move_index+1:] #remove number of moves
                    
                    available.append([x[8], x[0], x[2], condition]) #add names to list if not fainted or not current pokemon
                    
                ##code possibility to revive and do stuff to fainted pokemon
            
            print('')        
            for pokemon in available: #loop process for all not fainted pokemon
                if pokemon[3] == '':
                    print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])) 
                elif len(pokemon[3]) > 3: #check if there are more than two conditions
                    print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])+ \
                          ' ['+str.upper(pokemon[3][0:3])+']['+str.upper(pokemon[3][3:6])+']')  
                else:
                    print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])+ \
                          ' ['+str.upper(pokemon[3][0:3])+']')                   
                
            target = input('\nPlease select Pokemon would you like to use ' + choice + ' on, or input BACK (case sensitive): ')
            while target != 'BACK' and target not in names: #check if input is valid
                target = input('Please select Pokemon would you like to use ' + choice + ' on, or input BACK (case sensitive): ')             
            
            if target == 'BACK':
                os.system('cls')
                return user_turn(u_pokemon, user_battle, o_pokemon) 
            else:
                count = 0
                for item in user_bag:
                    count += 1
                    if choice == item[0]:
                        user_bag[count-1][1] -= 1 #decrease item number
                        
                        if user_bag[count-1][1] == 0:
                            user_bag.remove(user_bag[count-1])
                            
                new = u_pokemon[0] #keep current pokemon 
                
                ##code effects of using item
            
    
    # 3 INITIATE RUN
    #------------------------------------------------------------------------------------     
    elif user_move == 'RUN': #check if user wants to run away
        print_stats(u_pokemon, o_pokemon)
        
        print(p_name + ' is unable to run away!\n')
        user_move = input('Please input BACK (case sensitive): ') #prompt input of BACK
        while user_move != "BACK": #check if input is valid
            user_move = input('Player is unable to run away! Please input BACK (case sensitive): ')    
        
        if user_move == 'BACK':    
            os.system('cls')
            return user_turn(u_pokemon, user_battle, o_pokemon)        
    
    # 4 INITIATE SWITCH OUT
    #------------------------------------------------------------------------------------      
    elif user_move == 'POKEMON': #check if user wants to switch out current pokemon
        names = [] #create list of switchable pokemon names
        available = [] #create list of switchable pokemon names and stats
        
        print_stats(u_pokemon, o_pokemon)
        
        ##What if players want to only see their pokemon's stats/summaries?
        
        for x in user_battle: #loop process for each pokemon on team
            if u_pokemon[0] != x[0] and x[2] > 0: 
                names.append(x[0])
                condition = x[17]
                
                if 'slp' in x[17]: #check if sleep is in opnt conditions
                    slp_move_index = x[17].index('slp') + 3 #find index of moves until awake
                    slp_move = x[17][slp_move_index] #remember number of moves until awake
                    condition = x[17][:slp_move_index] + x[17][slp_move_index+1:] #remove number of moves
                        
                if 'con' in x[17]: #check if confusion is in opnt conditions
                    con_move_index = x[17].index('con') + 3 #find index of moves until not confused
                    con_move = x[17][con_move_index] #remember number of moves until not confused
                    condition = x[17][:con_move_index] + x[17][con_move_index+1:] #remove number of moves
                        
                available.append([x[8], x[0], x[2], condition]) #add names to list if not fainted or not current pokemon                
                
        if names == []: #check if all other pokemon have fainted
            new = input('No available pokemon. Please input BACK (case sensitive): ') #prompt input of BACK
            while new != 'BACK': #check if input is valid
                new = input('No available pokemon. Please input BACK (case sensitive): ') 
        else:
            print('Available Pokemon:')     
            for pokemon in available: #loop process for all not fainted pokemon
                if pokemon[3] == '':
                    print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])) 
                elif len(pokemon[3]) > 3: #check if there are more than two conditions
                    print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])+ \
                          ' ['+str.upper(pokemon[3][0:3])+']['+str.upper(pokemon[3][3:6])+']')  
                else:
                    print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])+ \
                          ' ['+str.upper(pokemon[3][0:3])+']')    
                
            new = input('\nInput Pokemon to switch in or BACK (case sensitive): ') #prompt input of pokemon name or BACK
            while new not in names and new != "BACK": #check if input is valid
                new = input('Please try again. Input Pokemon to switch in or BACK (case sensitive): ') 
        
        if new == 'BACK': #check if user wants to be redirected back to first start menu
            os.system('cls')
            return user_turn(u_pokemon, user_battle, o_pokemon) 
        
        user_move = 'SWITCH OUT' #relabel POKEMON as SWITCH OUT
    
    return u_pokemon, user_move, new
        
        
def opnt_turn(o_pokemon):
    i = randint(0, 3) 
    j = [9, 11, 13, 15] #indexes of pokemon move names
    opnt_move = o_pokemon[j[i]] #randomly select a move for opnt_move
    
    while (opnt_move == o_pokemon[9] and o_pokemon[10] == 0) or (opnt_move == o_pokemon[11] and o_pokemon[12] == 0) or \
          (opnt_move == o_pokemon[13] and o_pokemon[14] == 0) or (opnt_move == o_pokemon[15] and o_pokemon[16] == 0): #check PP of move
            i = randint(0, 3) 
            opnt_move = o_pokemon[j[i]]
    
    pp_index = o_pokemon.index(opnt_move) + 1
    o_pokemon[pp_index] -= 1 #subtract 1 from PP of move
    
    return o_pokemon, opnt_move


# BATTLE - BATTLE SEQUENCE 
#------------------------------------------
def battle_intro(p, user_team, user_current, msg):
    opnt_battle = [] #create list of opnt pokemon team stats for this battle
    user_battle = [] #create list of user pokemon team stats for this battle
    
    #[name, type, hp, atk, def, sp.atk, sp.def, speed, lv, 4*[moves, PP], condition]
    for x in opponents[p]: #loop for all pokemon in opponent team
        opnt_battle.append(["Foe's "+pokedex[x[0]][0]] + [pokedex[x[0]][1]] + list(np.add(x[1:7],pokedex[x[0]][2:8])) + x[7:18])    
    
    if user_current == []: #check if there is no data for user's current team
        for x in user_team: #loop for all pokemon in user's template team
            user_battle.append(pokedex[x[0]][0:2] + list(np.add(x[1:7],pokedex[x[0]][2:8])) + x[7:18]) 
    else:
        user_battle = user_current     
    
    o_pokemon = opnt_battle[0] #opnt's first pokemon will always be at full stats
        
    for x in user_battle: #user's first pokemon will be the first not fainted pokemon in team
        if x[2] > 0:
            u_pokemon = x 
            break    
    
    os.system('cls')
    print("You are challenged by "+msg[1]+"!")
    time.sleep(3)
    print(msg[1]+" sent out "+o_pokemon[0][6:]+"!")
    time.sleep(3)
    print("Go! "+u_pokemon[0]+"!\n")
    time.sleep(3)
    os.system('cls')
    
    return battle_main(user_battle, user_team, u_pokemon, opnt_battle, opponents[p], o_pokemon, msg)
    
    
def battle_main(user_battle, user_team, u_pokemon, opnt_battle, opnt_team, o_pokemon, msg):
    u_pokemon, user_move, u_new = user_turn(u_pokemon, user_battle, o_pokemon) #user turn
    o_pokemon, opnt_move = opnt_turn(o_pokemon) #opponent turn
    time.sleep(1)
    os.system('cls')         
    
    print_stats(u_pokemon, o_pokemon)
    
    if 'first' in moves_dict[opnt_move][6]: #Check if opnt has special effect for going first
        u_pokemon += [2]
    
    elif user_move == "BAG": #Check if user used bag instead of attacking
        if u_pokemon[7] < o_pokemon[7]: #Compare speed to decide which pokemon goes first
            u_pokemon += [2] #attach indicator to end of current user pokemon that user goes second
        else:
            u_pokemon += [1] #attach indicator to end of current user pokemon that user goes first           
    
    elif user_move != 'SWITCH OUT' and 'first' in moves_dict[user_move][6]: #Check if user has special effect for going first
            u_pokemon += [1]
    else:
        if u_pokemon[7] < o_pokemon[7]: #Compare speed to decide which pokemon goes first
            u_pokemon += [2] #attach indicator to end of current user pokemon that user goes second
        else:
            u_pokemon += [1] #attach indicator to end of current user pokemon that user goes first   
    
    # 1 FIRST MOVE 
    #------------------------------------------------------------------------------------ 
    if u_pokemon[18] == 1 and user_move == "SWITCH OUT": #check if user goes first and if move is switch
        for x in user_battle: #loop process for each pokemon in user's battle team
            if u_new == x[0]: #check if new pokemon name matches name of pokemon in user's battle team
                
                for y in user_battle: #loop process for each pokemon in user's battle team
                    if u_pokemon[0] == y[0]: #check if old pokemon name matches name of pokemon in user's battle team
                        u_pokemon.pop(18) #remove first/second indicator
                        y_index = user_battle.index(y) #find index of y in user battle team
                        user_battle.remove(y)
                        user_battle.insert(y_index, u_pokemon) #replace y in user battle team with current pokemon
                        break        
                     
                print(u_pokemon[0]+", switch out!\nCome back!\n")
                time.sleep(3)
                u_pokemon = x + [1] #attach first/second indicator onto new pokemon
                print("Go! "+u_pokemon[0]+"!\n")
                time.sleep(3)
                o_new = o_pokemon[0] #current opnt pokemon remains the same
                break
            
    elif u_pokemon[18] == 1 and user_move == "BAG":
        u_new = u_pokemon[0]
        o_new = o_pokemon[0]        
          
    else: #perform pokemon move instead of switch
        o_new = o_pokemon[0] #current opnt pokemon remains the same
        if u_pokemon[18] == 1: #check if user goes first
            u_pokemon, u_new, o_pokemon, o_new = move_process(u_pokemon, user_battle, user_team, u_new, o_pokemon, opnt_battle, o_new, user_move)
        else:
            o_pokemon, o_new, u_pokemon, u_new = move_process(o_pokemon, opnt_battle, opnt_team, o_new, u_pokemon, user_battle, u_new, opnt_move) 
        
        if user_move == 'SWITCH OUT' and u_pokemon[18] == 2 and 'fln' in u_pokemon[17]: #check if pokemon before switching out has flinch
            u_pokemon[17] = u_pokemon[17].replace('fln','') #remove condition
        
    battle_finished, player_win, user_switched, u_pokemon, o_pokemon = \
            move_result(u_new, u_pokemon, user_battle, o_new, o_pokemon, opnt_battle, msg) #evaluate result of first move
 
    # 2 SECOND MOVE 
    #------------------------------------------------------------------------------------                     
    if battle_finished == False: #check if battle is not finished
        os.system('cls')   
        
        print_stats(u_pokemon, o_pokemon)
        
        if u_pokemon[18] == 2 and user_move == "SWITCH OUT" and user_switched == False: #check if user goes second, move is switch, and no switch yet
            for x in user_battle: #loop process for each pokemon in user's battle team
                if u_new == x[0]: #check if new pokemon name matches name of pokemon in user's battle team
                    
                    for y in user_battle: #loop process for each pokemon in user's battle team
                        if u_pokemon[0] == y[0]: #check if old pokemon name matches name of pokemon in user's battle team
                            u_pokemon.pop(18) #remove first/second indicator
                            y_index = user_battle.index(y) #find index of y in user battle team
                            user_battle.remove(y)
                            user_battle.insert(y_index, u_pokemon) #replace y in user battle team with current pokemon
                            break        
                        
                    print(u_pokemon[0]+", switch out!\nCome back!\n")
                    time.sleep(3)
                    u_pokemon = x + [2] #attach first/second indicator onto new pokemon
                    print("Go! "+u_pokemon[0]+"!\n")
                    time.sleep(3)
                    o_new = o_pokemon[0] #current opnt pokemon remains the same
                    break
                
        elif u_pokemon[18] == 2 and (user_switched == True or user_move == "BAG"):
            u_new = u_pokemon[0]
            o_new = o_pokemon[0]
            
        else: #perform pokemon move instead of switch
            o_new = o_pokemon[0] #current opnt pokemon remains the same
            if u_pokemon[18] == 2: #check if user goes first
                u_pokemon, u_new, o_pokemon, o_new = \
                    move_process(u_pokemon, user_battle, user_team, u_new, o_pokemon, opnt_battle, o_new, user_move)
            else:
                o_pokemon, o_new, u_pokemon, u_new = \
                    move_process(o_pokemon, opnt_battle, opnt_team, o_new, u_pokemon, user_battle, u_new, opnt_move) 
            
        battle_finished, player_win, user_switched, u_pokemon, o_pokemon = \
            move_result(u_new, u_pokemon, user_battle, o_new, o_pokemon, opnt_battle, msg) #evaluate result of second move
    
    # 3 OVERALL RESULTS
    #------------------------------------------------------------------------------------     
    if battle_finished == False: #check if battle is not finished
        u_pokemon.pop(18) #remove first/second indicator
        os.system('cls')        
        return battle_main(user_battle, user_team, u_pokemon, opnt_battle, opnt_team, o_pokemon, msg)
    else:
        user_current = [] #clear current user team
        
        if player_win == True: #check if player has won     
            
            for x in user_battle: #loop process for each pokemon in user's battle team
                if u_pokemon[0] == x[0]: #check if current pokemon name matches name of pokemon in user's battle team
                    u_pokemon.pop(18) #remove first/second indicator
                    x_index = user_battle.index(x) #find index of x in user battle team
                    user_battle.remove(x)
                    user_battle.insert(x_index, u_pokemon) #replace x in user battle team with current pokemon
                    break 
            
            ##What about reversing stat changes other than hp?
            
            user_current = user_battle[:] #set battle team to current user team           
                         
        return player_win, user_current

        
def move_process(attacking_pokemon, attacking_battle, attacking_team, attacking_new, target_pokemon, target_battle, target_new, move):
    stats_indexes = {'hp ':2, 'atk':3, 'def':4, 'spa':5, 'spd':6, 'spe':7} #dict of indexes in pokemon list for given stat
    stats_names = {'atk': 'Attack', 'def': 'Defense', 'spa': 'Special Attack', 'spd': 'Special Defense', 'spe': 'Speed'} #dict of stat names
    combo = 1 #assume move only consists of one attack
    paralyzed = False; frozen = False; confused = False; sleep = False #assume conditions do not occur
    self_damage = 0; damage = 0 #assume damage and self damage are 0
    moves_indexes = [9,11,13,15]
    
    attacking_condition = attacking_pokemon[17] #set attacker's condition variable for better formatting
    target_condition = target_pokemon[17] #set target condition variable for better formatting
    
    ##What about inf (infatuation)?
    
    # 1 BEFORE MOVE CONDITIONS
    #------------------------------------------------------------------------------------ 
    if 'slp' in attacking_condition: #check if attacker's condition includes sleep
        slp_move_index = attacking_condition.index('slp') + 3 #find index of moves until awake
        slp_move = int(attacking_condition[slp_move_index])
        if slp_move == 1: #check if moves until awake is 1
            attacking_pokemon[17] = attacking_condition.replace('slp1','') #remove sleep condition 
            print(attacking_pokemon[0]+" woke up!\n")
            sleep = False
            time.sleep(3) 
        else: #moves until awake is more than 1
            attacking_pokemon[17] = attacking_condition[:slp_move_index] + str(slp_move-1) + attacking_condition[slp_move_index+1:] #-1 moves
            sleep = True #attacker is asleep and will be unable to attack  
        
    if 'par' in attacking_condition: #check if attacker's condition includes paralysis
        if evaluate_percent(25): #check if attacker will be paralyzed (25% chance)
            paralyzed = True #attacker is paralyzed and will be unable to attack
            
    if 'frz' in attacking_condition: #check if attacker's condition includes frozen
        if evaluate_percent(80): #check if attacker will be frozen (80% chance)
            frozen = True #attacker is frozen and will be unable to attack
        else:
            print(attacking_pokemon[0]+" thawed out!\n") #attacker is unfrozen
            time.sleep(3)      
            attacking_pokemon[17] = attacking_condition.replace('frz','') #remove frozen condition
    
    if 'con' in attacking_condition: #check if attacker's condition includes confusion       
        con_move_index = attacking_condition.index('con') + 3 #find index of moves until no longer confused 
        con_move = int(attacking_condition[con_move_index])
        if con_move == 1: #check if moves until not confused is 1
            attacking_pokemon[17] = attacking_condition.replace('con1','') #remove confusion 
            print(attacking_pokemon[0]+" snapped out of confusion!\n")
            time.sleep(3)    
        else: #moves until not confused is more than 1
            attacking_pokemon[17] = attacking_condition[:con_move_index] + str(con_move- 1) + attacking_condition[con_move_index+1:]
            print(attacking_pokemon[0]+" is confused!\n")
            time.sleep(3)                
            if evaluate_percent(50): #check if attacker will be paralyzed (50% chance)
                confused = True #attacker is confused and will hurt itself               
    
    for x in moves_indexes: #for all indexes with move names
        if move == attacking_pokemon[x]: #if the move name matches the move used
            move_PP_index = x + 1 #find the index of the move's PP
    
    if 'fln' not in attacking_condition and sleep == False and paralyzed == False and frozen == False and confused == False: #check if moves works
        print(attacking_pokemon[0]+" used\n"+move+"!\n")                                                            
        time.sleep(3)      

        if (evaluate_percent(moves_dict[move][4])) or ('no_miss' in moves_dict[move][6]): #check if move itself hits based on accuracy and special fx
            
    # 2 CONDITION/STAT CHANGES
    #------------------------------------------------------------------------------------    
            if '+' in moves_dict[move][6]: #check if move has more than 1 special effects
                special_fx = moves_dict[move][6].split('+') #split special effects into a list if applicable
            else:
                special_fx = [moves_dict[move][6]]    
            
            for x in special_fx: #loop process for each special effect
                if x != '': #check if move has no special effects
                    if 'stat' in x: #check if move affects condition/stat 
                        special_percent_index = x.rfind('_') + 1 #find index of special effect accuracy 
                        if evaluate_percent(int(x[special_percent_index:])): #check if special effect hits based on accuracy 
                            
                            if 'atk' in x or 'def' in x or 'spa' in x or 'spd' in x or 'spe' in x: #check if effect changes stats of attacker/target
                                stat_index = stats_indexes[x[10:13]] #find index for changing stat
                                if 'user' in x: #check if stat change affects attacker
                                    if 'dn' in x: #check if there is a decrease in attacker stats
                                        amount_index = x.index('dn') + 2 #find index of amount decreased ((amount*10)%)
                                        attacking_pokemon[stat_index] *= (1-int(x[amount_index:special_percent_index-1])/10) 
                                        attacking_pokemon[stat_index] = int(attacking_pokemon[stat_index])
                                        
                                        if int(x[amount_index:special_percent_index-1]) == 1:
                                            print(attacking_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nfell!\n")
                                            time.sleep(3)
                                        else:
                                            print(attacking_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nharshly fell!\n")
                                            time.sleep(3)
                                            
                                    elif 'up' in x: #check if there is a increase in attacker stats
                                        amount_index = x.index('up') + 2 #find index of amount increased ((amount*10)%)
                                        attacking_pokemon[stat_index] *= (1+int(x[amount_index:special_percent_index-1])/10) 
                                        attacking_pokemon[stat_index] = int(attacking_pokemon[stat_index])
                                        
                                        if int(x[amount_index:special_percent_index-1]) == 1:
                                            print(attacking_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nrose!\n")
                                            time.sleep(3)
                                        else:
                                            print(attacking_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nsharply rose!\n") 
                                            time.sleep(3)
                                            
                                elif 'opnt' in x: #check if stat change affects target
                                    if 'dn' in x: #check if there is a decrease in target stats
                                        amount_index = x.index('dn') + 2 #find index of amount decreased ((amount*10)%)
                                        target_pokemon[stat_index] *= (1-int(x[amount_index:special_percent_index-1])/10) 
                                        target_pokemon[stat_index] = int(target_pokemon[stat_index])
                                        
                                        if int(x[amount_index:special_percent_index-1]) == 1:
                                            print(target_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nfell!\n")
                                            time.sleep(3)
                                        else:
                                            print(target_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nharshly fell!\n") 
                                            time.sleep(3)
                                            
                                    elif 'up' in x: #check if there is a increase in target stats
                                        amount_index = x.index('up') + 2 #find index of amount increased ((amount*10)%)
                                        target_pokemon[stat_index] *= (1+int(x[amount_index:special_percent_index-1])/10)   
                                        target_pokemon[stat_index] = int(target_pokemon[stat_index])
                                        
                                        if int(x[amount_index:special_percent_index-1]) == 1:
                                            print(target_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nrose!\n")
                                            time.sleep(3)
                                        else:
                                            print(target_pokemon[0]+"'s "+stats_names[x[10:13]]+"\nsharply rose!\n")
                                            time.sleep(3)
                                        
                            elif 'hp' in x: #check if effect changes hp of attacker
                                stat_index = stats_indexes[x[10:13]] #find index for changing hp
                                for y in attacking_team: 
                                    if attacking_pokemon[9] == y[8] and attacking_pokemon[11] == y[10] and attacking_pokemon[13] == y[12]:
                                        base_hp = pokedex[y[0]][2] #find base hp of attacker
                                        max_hp = base_hp + y[2] #find max hp of attacker
                                        break
                                if attacking_pokemon[stat_index] < max_hp: #check if attacker is below max hp
                                    amount_index = x.index('up') + 2 #find index of amount healed ((base hp*amount*10)%)
                                    attacking_pokemon[stat_index] += int(base_hp * int(x[amount_index:special_percent_index-1])/10) 
                                    
                                    if attacking_pokemon[stat_index] > max_hp: #check if attacker is above max hp affter healing
                                        attacking_pokemon[stat_index] = max_hp #set attacker hp to max hp
                                    
                            else: #attack changes target condition
                                if 'slp' in x or 'con' in x: #check if move will induce sleep or confusion
                                    if move == "Grass Whistle" or move == "Hypnosis" or move == "Lovely Kiss" or move == "Sing" or \
                                       move == "Sleep Powder" or move == "Spore" or move == "Yawn":
                                        if 'slp' not in target_condition: #check if sleep is not already present 
                                            target_pokemon[17] += ('slp'+str(randint(1,4))) #include conditon and set move timer (2-4 turns)
                                            print(target_pokemon[0]+" fell\nasleep!\n")
                                            time.sleep(3)                                                   
                                        else:
                                            print(target_pokemon[0]+" is already asleep.\n")
                                            time.sleep(3)                                    
                                    
                                    else:
                                        if x[10:13] not in target_condition: #check if condition is not already present
                                            target_pokemon[17] += (x[10:13]+str(randint(1,4))) #include conditon and set move timer (2-4 turns)
                                            if 'slp' in x:
                                                print(target_pokemon[0]+" fell\nasleep!\n")
                                                time.sleep(3)     
                                            elif 'con' in x:
                                                print(target_pokemon[0]+" is\nconfused!\n")
                                                time.sleep(3)     
                            
                                else: #move induces other conditions outside of sleep or confusion
                                    if 'fln' in x: #check if move will induce flinching
                                        if 'slp' not in target_condition: #check if sleep is not present 
                                            if len(target_pokemon) == 19: #check if user == target
                                                if target_pokemon[18] == 2: #check if user is going second
                                                    target_pokemon[17] += 'fln'   
                                            else: #user == attacker
                                                if attacking_pokemon[18] == 1: #check if user is going first
                                                    target_pokemon[17] += 'fln' 
                                            
                                    elif move == "Poison Powder" or move == "Poison Gas": 
                                        if 'psn' not in target_condition: #check if poison is not already present 
                                            target_pokemon[17] += 'psn'
                                            print(target_pokemon[0]+" was poisoned!\n")
                                            time.sleep(3)                                                   
                                        else:
                                            print(target_pokemon[0]+" is already poisoned.\n")
                                            time.sleep(3)                                            
                                    
                                    elif move == "Will-O-Wisp":
                                        if 'brn' not in target_condition: #check if burn is not already present 
                                            target_pokemon[17] += 'brn'
                                            print(target_pokemon[0]+" was burned!\n")
                                            time.sleep(3)                                                   
                                        else:
                                            print(target_pokemon[0]+" is already burned.\n")
                                            time.sleep(3)       
                                    
                                    elif move == "Thunder Wave" or move == "Stun Spore" or move == "Glare":
                                        if 'par' not in target_condition: #check if paralysis is not already present 
                                            target_pokemon[17] += 'par'
                                            target_pokemon[7] *= 0.5 #speed is halved
                                            print(target_pokemon[0]+" became paralyzed!\n")
                                            time.sleep(3)                                                   
                                        else:
                                            print(target_pokemon[0]+" is already paralyzed.\n")
                                            time.sleep(3)                                      
                                    
                                    else:
                                        if x[10:13] not in target_condition: #check if condition is not already present 
                                            target_pokemon[17] += x[10:13]   
                                            if 'psn' in x:
                                                print(target_pokemon[0]+" was poisoned!\n")
                                                time.sleep(3)       
                                            elif 'brn' in x:
                                                print(target_pokemon[0]+" was burned!\n")
                                                time.sleep(3)        
                                            elif 'frz' in x:
                                                print(target_pokemon[0]+" was frozen solid!\n")
                                                time.sleep(3)   
                                            elif 'par' in x:
                                                target_pokemon[7] *= 0.5 #speed is halved
                                                print(target_pokemon[0]+" became paralyzed!\n")
                                                time.sleep(3)                                                   
                        
                    elif 'fury' in x: #check if attack has fury
                        chance = randint(0,8) #3/8 chance of 2 atks, 3/8 chance of 3 atks, 1/8 chance of 4 and 5 atks
                        if chance <= 3:
                            combo = 2
                        elif 3 < chance <= 6:
                            combo = 3
                        elif chance == 7:
                            combo = 4
                        else:
                            combo = 5                
            
    # 3 CALCULATING DAMAGE
    #------------------------------------------------------------------------------------  

    ##What about environmental factors?
    
            for num in range(0,combo): #loop process for all attacks (should only loop for fury)
                C = moves_dict[move][3] #C = base power of move
                Z = randint(217,255) #Z = random integer between 217 and 255
                
                if 'crit' in moves_dict[move][6]: #check if crit is listed as a special effect
                    crit_percent_index = moves_dict[move][6].rfind('_') + 1 #find index of new critical percent chance
                    crit = evaluate_percent(float(moves_dict[move][6][crit_percent_index:]))
                else: 
                    crit = evaluate_percent(6.25) #A = level of attacker; can be doubled on critical hit (normally 6.25% chance)
                    
                if moves_dict[move][2] == 'sta': #no criticals for status only moves
                    crit = False
                    
                if crit == True: #check if move is a critical
                    print("A critical hit!\n")
                    time.sleep(3)
                    A = 2*attacking_pokemon[8] 
                else:
                    A = attacking_pokemon[8]
                
                if moves_dict[move][2] == 'phy': #B = atk or sp.atk of attacker
                    B = attacking_pokemon[3]    #D = def or sp.def of target
                    D = target_pokemon[4]
                elif moves_dict[move][2] == 'spc':
                    B = attacking_pokemon[5]
                    D = target_pokemon[6] 
                
                if moves_dict[move][1] in attacking_pokemon[1]: #X = same type attack bonus (type of attacker = type of move)
                    X = 1.5
                else:
                    X = 1
                 
                Y = 1 #Y = type multiplier based on attack's type and target type; assume Y = 1
                if '+' in target_pokemon[1]: #check if target has more than one type
                    target_type = target_pokemon[1].split('+') #split target's types into a list if applicable
                else:
                    target_type = [target_pokemon[1]]
                    
                for x in target_type: 
                    if x in super_effective[moves_dict[move][1]]: #check if move is super effective (x2)                
                        Y  *= 2
                    elif x in not_effective[moves_dict[move][1]]: #check if move is not very effective (x0.5)                      
                        Y  *= 0.5
                    elif x in immune[moves_dict[move][1]]: #check if move does no damage (x0)                      
                        Y  *= 0
                    else:    
                        Y  *= 1
                
                if moves_dict[move][2] == 'sta': #no bonus for status only moves
                    Y = 1
                        
                if Y == 0:
                    print("It doesn't affect "+target_pokemon[0]+".\n")
                    time.sleep(3)                      
                elif Y > 1:
                    print("It's super effective!\n")
                    time.sleep(3)                      
                elif Y < 1: 
                    print("It's not very effective...\n")
                    time.sleep(3)  
                    
                if moves_dict[move][2] != 'sta': #check if move is status only
                    damage += math.floor(((((2*A)/5+2) * B * C / D)/50 +2)* X * Y * (Z/255)) + 1
                    if 'brn' in attacking_condition and moves_dict[move][2] != 'phy': #check if attacker is burned and move is physical 
                        damage = math.floor(damage * 0.5) + 1
                
    # 4 PRINT CONDITIONS OF MOVE MISS
    #------------------------------------------------------------------------------------     
        else:
            print(attacking_pokemon[0]+"'s attack missed!\n") #attacker missed
            time.sleep(3)
            damage = 0
            
    elif 'fln' in attacking_condition: #check if attacker flinched
        print(attacking_pokemon[0]+" flinched!\n")
        time.sleep(3)
        attacking_pokemon[move_PP_index] += 1 #add 1 to PP of move if attacker was unable to use it
        attacking_pokemon[17] = attacking_condition.replace('fln','') #remove condition
        damage = 0
    
    elif 'con' in attacking_condition: #check if attacker is confused and hurt itself
        print(attacking_pokemon[0]+" hurt itself in its confusion!\n")
        time.sleep(3)         
        attacking_pokemon[move_PP_index] += 1 #add 1 to PP of move if attacker was unable to use it
        
        A = attacking_pokemon[8]
        B = attacking_pokemon[3]
        C = 40
        D = attacking_pokemon[4]
        X = 1; Y = 1; Z = randint(217,255)
        
        self_damage += math.floor(((((2*A)/5+2) * B * C / D)/50 +2)* X * Y * (Z/255)) + 1      
    
    elif 'slp' in attacking_condition: #check if attacker is asleep
        print(attacking_pokemon[0]+" is fast\nasleep.\n")
        time.sleep(3)
        attacking_pokemon[move_PP_index] += 1 #add 1 to PP of move if attacker was unable to use it
        
    elif paralyzed == True: #check if attacker is paralyzed
        print(attacking_pokemon[0]+" is paralyzed!\nIt can't move!\n")
        time.sleep(3)
        attacking_pokemon[move_PP_index] += 1 #add 1 to PP of move if attacker was unable to use it
        
    elif frozen == True: #check if attacker is frozen
        print(attacking_pokemon[0]+" is\nfrozen solid!\n")
        time.sleep(3)   
        attacking_pokemon[move_PP_index] += 1 #add 1 to PP of move if attacker was unable to use it
    
    # 5 DAMAGE INFLICTED TO TARGET AND ATTACKER
    #------------------------------------------------------------------------------------      
    if len(target_pokemon) == 19:
        owner = "user"
    else:
        owner = "opnt"
    
    target_pokemon[2] -= damage #target receives attack damage  
    target_new = is_fainted(target_pokemon, target_battle, target_new, owner) #evaluate if target fainted and if there is a new target 
           
    if moves_dict[move][1] == 'fir' and 'frz' in target_condition: #fire moves remove frz from target
        target_pokemon[17] = target_condition.replace('frz','')
        print(target_pokemon[0]+" thawed out!\n")        
        time.sleep(3)
        
    if 'brn' in attacking_condition: #check if attacker is burned
        print(attacking_pokemon[0]+" is hurt\nby its burn!\n")      
        time.sleep(3)   
        for x in attacking_team: 
            if attacking_pokemon[9] == x[8] and attacking_pokemon[11] == x[10] and attacking_pokemon[13] == x[12]:
                base_hp = pokedex[x[0]][2] #base hp of attacker
                max_hp = base_hp + x[2] #max hp of attacker
                break        
        self_damage += int(0.125 * max_hp) #add damage to self-inflicted       
    
    if 'psn' in attacking_condition: #check if attacker is poisoned
        print(attacking_pokemon[0]+" is hurt\nby poison!\n")       
        time.sleep(3)    
        for x in attacking_team: 
            if attacking_pokemon[9] == x[8] and attacking_pokemon[11] == x[10] and attacking_pokemon[13] == x[12]:
                base_hp = pokedex[x[0]][2] #base hp of attacker
                max_hp = base_hp + x[2] #max hp of attacker
                break        
        self_damage += int(0.125 * max_hp) #add damage to self-inflicted     
        
    ##What about recoil?
    
    if len(attacking_pokemon) == 19:
        owner = "user"
    else:
        owner = "opnt"    
    
    attacking_pokemon[2] -= self_damage #attacker receives self inflicted damage 
    attacking_new = is_fainted(attacking_pokemon, attacking_battle, attacking_new, owner) #evaluate if attacker fainted and if there is new attacker
    
    return attacking_pokemon, attacking_new, target_pokemon, target_new


def is_fainted(current_pokemon, pokemon_battle, expected_new_pokemon, owner):
    if current_pokemon[2] <= 0: #check if pokemon has less than or equal to 0 hp   
        current_pokemon[2] = 0 #set pokemon hp to 0 if fainted
        current_pokemon[17] = '' #remove all conditions
        
        names = [] #create list of switchable pokemon names
        available = [] #create list of switchable pokemon names and stats
        
        for x in pokemon_battle: #loop process for each pokemon on team
            if current_pokemon[0] != x[0] and x[2] > 0: 
                names.append(x[0]) #add names to list if not fainted or not current pokemon
                condition = x[17]
                
                if 'slp' in x[17]: #check if sleep is in opnt conditions
                    slp_move_index = x[17].index('slp') + 3 #find index of moves until awake
                    slp_move = x[17][slp_move_index] #remember number of moves until awake
                    condition = x[17][:slp_move_index] + x[17][slp_move_index+1:] #remove number of moves
                        
                if 'con' in x[17]: #check if confusion is in opnt conditions
                    con_move_index = x[17].index('con') + 3 #find index of moves until not confused
                    con_move = x[17][con_move_index] #remember number of moves until not confused
                    condition = x[17][:con_move_index] + x[17][con_move_index+1:] #remove number of moves
                        
                available.append([x[8], x[0], x[2], condition]) #add names to list if not fainted or not current pokemon

        print(current_pokemon[0]+" fainted!\n")
        time.sleep(3)
        
        if names == []: #check if all other pokemon have fainted
            new = None #no more pokemon available
        else:
            if owner == 'user':
                print("Available Pokemon:")
                for pokemon in available: #loop process for all not fainted pokemon
                    if pokemon[3] == '':
                        print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])) 
                    elif len(pokemon[3]) > 3: #check if there are more than two conditions
                        print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])+ \
                              ' ['+str.upper(pokemon[3][0:3])+']['+str.upper(pokemon[3][3:6])+']')  
                    else:
                        print("(LV "+str(pokemon[0])+") "+pokemon[1]+' hp: '+str(pokemon[2])+ \
                              ' ['+str.upper(pokemon[3][0:3])+']')
                    
                new = input("\nInput your next Pokemon (case sensitive): ") #prompt input of pokemon name
                while new not in names: #check if input is valid
                    new = input("Please try again. Input your next Pokemon (case sensitive): ") 
                print('')
                
            else:
                random = randint(0, len(names)-1) #random number generator
                new = names[random] #randomly choose a pokemon
    else:
        new = expected_new_pokemon #no new pokemon
    
    return new
  
 
def move_result(u_new, u_pokemon, user_battle, o_new, o_pokemon, opnt_battle, msg):
    user_switched = False #assume user did not switch pokemon       
    
    if u_new == None: #check if user is out of pokemon
        os.system('cls')
        print_stats(u_pokemon, o_pokemon)
        
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
        battle_finished = True #battle is finished
        player_win = False #player loses
        user_switched = None #does not matter    
    
    elif o_new == None: #check if opnt is out of pokemon
        os.system('cls')
        print_stats(u_pokemon, o_pokemon)
        
        print("Player defeated\n"+msg[1]+"!\n")
        time.sleep(3)
        print(msg[4]+"\n")
        time.sleep(msg[5])
        print(p_name+" got $100\nfor winning!")
        time.sleep(4)
        battle_finished = True #battle is finished
        player_win = True #player wins
        user_switched = None #does not matter    
    
    else:
        battle_finished = False #battle is not finished
        player_win = None #no one wins    
        
        if u_new != u_pokemon[0] and u_pokemon[2] == 0: #check if there is a new user pokemon bc old one fainted
            for x in user_battle: 
                if u_new == x[0]:
                    turn_indicator = u_pokemon[18] #remember turn indicator of old pokemon
                    
                    for y in user_battle: #loop process for each pokemon in user's battle team
                        if u_pokemon[0] == y[0]: #check if current pokemon name matches name of pokemon in user's battle team
                            u_pokemon.pop(18) #remove first/second indicator
                            y_index = user_battle.index(y) #find index of y in user battle team
                            user_battle.remove(y)
                            user_battle.insert(y_index, u_pokemon) #replace y in user battle team with current pokemon
                            break                        
                    
                    u_pokemon = x + [turn_indicator] #attach first/second indicator onto new pokemon
                    print("Go! "+u_pokemon[0]+"!\n")
                    time.sleep(3)
                    user_switched = True #remember that user has already switched pokemon
                    break
                    
        if o_new != o_pokemon[0]: #check if there is a new opnt pokemon bc old one fainted
            for x in opnt_battle: #loop process for each pokemon in opnt's battle team
                if o_new == x[0]: #check if current pokemon name matches name of pokemon in opnt's battle team
                    o_pokemon = x 
                    print(msg[1]+" sent out "+o_pokemon[0][6:]+"!\n")
                    time.sleep(3)    
    
    return battle_finished, player_win, user_switched, u_pokemon, o_pokemon              
                
                
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
        

# STARTER FUNCTION
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

#start()

# TESTING
#------------------------------------------
def test_battle():
    global p_name
    msg = ["battle", "True Blue", "Boundless!", 2, "You are BOUNDLESS!!!", 3]
    p = 103
    p_name = 'Daniel'
    user_current = []
    
    print(battle_intro(p, user_team, user_current, msg))
    A = input()

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

def check_base_stats():
    #stat_sum includes #1-
    stat_sum = []   
    
    print(len(stat_sum))
    
    problems = []
    completed = 0
    
    for x in range(1,41):
        result = sum(pokedex[x+completed][2:8])
        if result != stat_sum[x-1]:
            problems.append(x+completed)
    
    print(problems)
    
test_all_but_intro()
#test_battle()