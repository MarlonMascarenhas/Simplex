#################################################################################################
#                                                                                            	#
# Simplex.py                                                                                  	#
#                                                                                            	#
# Instituto Federal de Educação, Ciência e Tecnologia de Minas Gerais (IFMG) - Formiga/MG   	#
#                                                                                            	#
# Data       Autor        Comentarios                                                        	#
# ========   ===========  ======================================================================#
# 13/11/19   Marlon Mascarenhas  Versao Inicial. Trata apenas problemas sem degeneracao.		#
# 13/11/19	 Italo  Hylander																	#
# 13/11/19   Renan  Evilasio																	#
#                                                                                            	#
#################################################################################################
#																								#
#################################################################################################
#                                                                                            	#
# Metodo Simplex                                                                             	#
#                                                                                            	#
# Resolve problemas de programação linear utilizando o método Simplex proposto por Dantzig   	#
# em 1947. São informados a matriz de coeficientes 'matriz', o vetor de recursos 'b', o vetor de#
# custos 'vetCost', os indices de matriz que formam a base da solucao basica factivel inicial,  #
# os indices das variaveis nao-basicas, a dimensao de 'matriz'        							#
#                                                                                           	#
# para executar digite no terminal $python Simplex.py "nome de arquivo" (certifique de ter 		#
# aberto o terminal no mesmo diretorio do arquivo) é necessario utilizar python3.				#
# também deve-se instalar as bibliotecas numpy e math (se não as possuir) deve-se rodar os 		#
# comandos:																						#
# py -m pip install numpy																		#
# py -m pip install math																		#
#################################################################################################


import numpy as np
import math as m
from os import path
import sys
from datetime import date



def calcSolBasic(matrix, b):
	#calcula solução basica
	Binv = np.linalg.inv(matrix)

	Binv = np.transpose(Binv)#matriz inversa Trasposta

	return Binv, np.dot(Binv, b) #retorna matriz inversa transposta + a solução basica

 
def montaMatrix(matrix, vetorBase, linhas):
	#monta matriz com vetores base
	aux = []

	for j in vetorBase:
		aux2 = []
		for i in range(linhas):
			aux2.append(matrix[i][j])
		aux.append(aux2)
		
	return aux #retorna matriz basica escolhida pelo usuario

def montaVetNaoBase(qtdCol, vetBase):
	#monta matriz de vetor não base
	aux = []
	for i in range(qtdCol):
		if not i in vetBase:
			aux.append(i)
	return aux #retorna matriz não escolhido pelo usuario 

def montaCustBase(custo, vetBase):
	#monta custo base
	aux = []
	for i in vetBase:
		aux.append(custo[i])
	return aux #monta vetor de custo base escolhido pelo usuario

def montaCustNaoBase(custo, vetNaoBase):
	#monta vetor de custo não base
	aux = []
	for i in vetNaoBase:
		aux.append(custo[i])
	return aux #monta vetor de custo não escolhido pelo usaurio

def escolheCustReduzido(indicesNaobase, matrix, linhas, matrixInv, vetCust, vetCustBase, indicesBase, solBasic, colunas):
	#Escolhe o menor custo para entrar na base e o maior para sair da mesma

	CustoEscolhido = 1000000000000000000000000 #infinito
	Jescolhido = -1
	transpostaVetCustBase =  vetCustBase #faz o vetor de custo base transposto

	for j in indicesNaobase:
		aux = []
		for i in range(linhas):
			aux.append(matrix[i][j])

		
		direcao = np.dot((matrixInv * -1), aux)

		auxCalc = np.dot(transpostaVetCustBase, matrixInv)

		auxCalc = np.dot(auxCalc, aux)

		custo = vetCust[j] - auxCalc

		if (custo < 0 and custo < CustoEscolhido):
			Jescolhido = j
			CustoEscolhido = custo

		if (Jescolhido == -1):
			valObjetivo = 0
			for i in range(linhas):
				valObjetivo = valObjetivo + vetCustBase[i] + solBasic[i]
			print('valor objetivo')
			print(valObjetivo)

			solucao = []

			for i in range(colunas):
				solucao.append(0)

			for i in range(linhas):
				solucao[indicesBase[i]] = solBasic[i]


			for i in range(colunas):
				print('x[', i, '] = ', solucao[i])

			return 1, indicesNaobase, matrix, linhas, matrixInv, vetCust, vetCustBase, indicesBase, solBasic, colunas, Jescolhido, solucao

		
	return 0, indicesNaobase, matrix, linhas, matrixInv, vetCust, vetCustBase, indicesBase, solBasic, colunas, Jescolhido, 0

def computaVetor(JotaEscolhido, matrixInv, linha, coluna, matrix):
	

	A = []

	for i in range(linha):
		
		A.append(matrix[i][JotaEscolhido])

	
	u = np.dot(matrixInv, A)
	existePositivo = False

	for i in range(linha):
		if u[i] > 0:
			existePositivo  = True

	if(not existePositivo):
		print('custo Otimo = -infinito')
		return 1

	return u

def Theta(linha, solBasic, u, indicesBase):
	theta = 10000000000000
	indiceL = -1
	razao = 0
 
	for i in range(linha):
		if u[i] > 0:
			razao = solBasic[i] / u[i]

			if razao < theta:
				theta = razao
				indiceL = indicesBase[i]


	return theta, indiceL, razao, u


def atualiza(linha, coluna, indiceL, indicesBase, theta, JotaEscolhido, indicesNaobase, solBasic):
	


	for i in range(linha):
		if indicesBase[i] == indiceL:
			solBasic[i] = theta
			indicesBase[i] = JotaEscolhido

	for i in range(coluna - linha):
		if indicesNaobase[i] == JotaEscolhido:
			indicesNaobase[i] = indiceL

	return solBasic, indicesBase, indicesNaobase, indiceL, JotaEscolhido


def leArquivo(NomeArq):
		aux = []
		matriz = []		
		vetCost = []
		vetBase = []
		b = []
		arq = open(NomeArq,'r')

		caracter = arq.read()	
		u = 0
		aux.append("")
		for i in range(len(caracter)):
			if caracter[i] != ' ' and  caracter[i] != '\n':
				aux[u] += caracter[i]

			else:
				if aux[u] != "":
					aux.append("")
					u = u + 1

				

		contC = 2			
		qtdLin = int(aux[0])
		qtdCol = int(aux[1])

		print(qtdLin)
		print(qtdCol)
		for i in range(qtdLin):
				matriz.append([])
				for j in range(qtdCol):
						if(aux[contC] == '-'):
							contC += 1
							matriz[i].append(float(aux[contC]))
							matriz[i] = matriz[i] * -1
						else:
							matriz[i].append(float(aux[contC]))
						
						contC += 1
		
		for i in range(qtdCol):
			if(aux[contC] == '-'):
				contC += 1
				vetCost.append(float(aux[contC])  * -1)
			else:
				vetCost.append(float(aux[contC]))
			contC+=1
		print(vetCost)

		for i in range(qtdLin):
			if(aux[contC] == '-'):
				contC += 1
				vetBase.append(int(aux[contC]) * -1)
			else:
				vetBase.append(int(aux[contC]))	
			contC+=1

		print(vetBase)

		for i in range(qtdLin):
			if(aux[contC] == '-'):
				contC += 1
				b.append(float(aux[contC]) * -1)
			else:
				b.append(float(aux[contC]))	
			contC+=1


		return(matriz, vetCost, vetBase, qtdLin, qtdCol, b)


if __name__ == "__main__":
	
	aux = []
	
	for param in sys.argv:
		aux.append(param)
	NomeArq = aux[1]		

matriz,vetCost,vetBase,qtdLin,qtdCol,b = leArquivo(NomeArq)

print("Matriz:")
print(matriz)

print("Vetor de Custo:")
print(vetCost)	

vetCostIni = vetCost

print("vetor base:")				
print(vetBase)



control = 0
exe = 1

while(control != 1):
	print('\n')
	print('\n')

	print("Execução: Nº", exe)

	matrizB = montaMatrix(matriz, vetBase, qtdLin)
	print('matrixB')
	print(matrizB)

	vetCustBase = montaCustBase(vetCost, vetBase)
	print('vetor custo base')
	print(vetCustBase)

	matrixInv, solBasic = calcSolBasic(matrizB, b)
	print('matrix inversa')
	print(matrixInv)
	print('solucao basica')
	print(solBasic)

	indicesNaobase = montaVetNaoBase(qtdCol, vetBase)
	print('indeices Nao base')
	print(indicesNaobase)

	vetCustNaoBase = montaCustNaoBase(vetCost, indicesNaobase)
	print('vetor custo nao base')
	print(vetCustNaoBase)

	print('custo reduzido')
	control, indicesNaobase, matriz, qtdLin, matrixInv, vetCost, vetCustBase, vetBase, solBasic, qtdCol, Jescolhido, solucao  = escolheCustReduzido(indicesNaobase, matriz, qtdLin, matrixInv, vetCost, vetCustBase, vetBase, solBasic, qtdCol)

	if control != 1:
		u = computaVetor(Jescolhido, matrixInv, qtdLin, qtdCol, matriz)

		theta, indiceL, razao, u = Theta(qtdLin, solBasic, u, vetBase)

		solBasic, vetBase, indicesNaobase, indiceL, Jescolhido = atualiza(qtdLin, qtdCol, indiceL, vetBase, theta, Jescolhido, indicesNaobase, solBasic)
	exe += 1
