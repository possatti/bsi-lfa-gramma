#!/usr/bin/python3

import argparse
import sys

# Descrição da interface da linha de comando.
parser = argparse.ArgumentParser(description="Gera palavras que são reconhecidas pela gramática indicada e que tenham o comprimento determinado.")
parser.add_argument('input_file', metavar='ARQUIVO', type=argparse.FileType('r'),
                   help='Indica o arquivo que contém a gramática que será usada.')
parser.add_argument('num', metavar='COMPRIMENTO', type=int,
                   help='Comprimento das palavras que serão geradas.')

# Processa os argumentos recebidos da linha de comando.
args = parser.parse_args()

def printerr(*msg):
	'''Imprime uma mensagem de erro para o standard error.'''
	print(parser.prog + ':', *msg, file=sys.stderr)

def err(*msg):
	'''Imprime uma mensagem de erro e sai do programa.'''
	printerr(*msg)
	printerr("Saindo com erro.")
	exit(1)

# Interpreta a gramática descrita no arquivo indicado.
variaveis = []
terminais = []
inicial = None
regras_producao = []
with open(args.input_file.name) as f:
	for linha in f.readlines():
		# Divide a linha em tokens.
		tokens = linha.split()

		# Se for a definição de variáveis.
		if len(tokens) > 2 and tokens[0].upper() == 'V' and tokens[1] == '=':
			for variavel in tokens[2:]:
				# Verifica se o comprimento da variável é 1.
				if len(variavel) > 1:
					err("Variáveis devem ser compostas por apenas um caractere. E a variável '" + variavel + "'' quebra essa regra na definição da gramática.")

				# Adiciona as variáveis, somente se já não estiver lá.
				if variavel not in variaveis:
					variaveis.append(variavel)
				else:
					printerr("Ignorando uma declaração de variável duplicada.")

		# Se for a definição de símbolos terminais.
		elif len(tokens) > 2 and tokens[0].upper() == 'T' and tokens[1] == '=':
			for terminal in tokens[2:]:
				# Verifica se o comprimento do terminal é 1.
				if len(terminal) > 1:
					err("Símbolos terminais devem ser compostos por apenas um caractere. E o terminal '" + terminal + "'' quebra essa regra na definição da gramática.")

				# Adiciona aos terminais, somente se já não estiver lá.
				if terminal not in terminais:
					terminais.append(terminal)
				else:
					printerr("Ignorando uma declaração de terminal duplicada.")

		# Se for a definição do símbolo inicial.
		elif len(tokens) == 3 and tokens[0].upper() == 'S' and tokens[1] == '=':
			inicial = tokens[2]

		# Se for a definição de uma regra de produção.
		elif len(tokens) == 3 and tokens[1] == '->':
			regras_producao.append((tokens[0], tokens[2]))

		# Se uma linha não puder ser interpretada.
		else:
			printerr("Ignorando linha que não pôde ser interpretada:", linha)

# Verifica se a gramática lida é valida.
if inicial == None or inicial not in variaveis:
	err("A gramática não declarou a variável inicial ou ela não está indefinida na seção de variáveis.")

# Verifica se todos os símbolos usados nas regras estão declarados como
# variáveis ou terminais.
for regra in regras_producao:
	for palavra in regra:
		for simbolo in palavra:
			if simbolo not in variaveis \
					and simbolo not in terminais \
					and simbolo != '$':
				err("O símbolo '" + simbolo + "' está sendo usado nas regras, porém ele não foi declarado como um símbolo terminal e nem variável.")

# Verifica se os conjuntos de variáveis e terminais são disjuntos.
for variavel in variaveis:
	for terminal in terminais:
		if terminal == variavel:
			err("O símbolo '" + terminal + "' esta declarado tanto como terminal, como variável. Porém o conjunto dos símbolos terminais e os das variáveis devem ser disjuntos.")

def derivar(cadeia, regras):
	'''Retorna uma lista de cadeias derivadas da cadeia original,
	através da aplicação de todas as regras possíveis.'''
	cadeias_derivadas = []
	for regra in regras:
		if regra[0] in cadeia:
			# Aplica a regra.
			nova_cadeia = ''
			if regra[1] == '$':
				nova_cadeia = cadeia.replace(regra[0], "")
			else:
				nova_cadeia = cadeia.replace(regra[0], regra[1])

			# Adiciona a nova cadeia a lista de cadeias derivadas.
			if nova_cadeia not in cadeias_derivadas:
				cadeias_derivadas.append(nova_cadeia)
	return cadeias_derivadas

# Deriva as cadeias, várias e várias vezes, limitando o seu tamanho para
# no máximo, o limite especifícado pelo usuário.
cadeias = [inicial]
for cadeia in cadeias:
	derivadas = derivar(cadeia, regras_producao)
	for derivada in derivadas:
		if len(derivada) <= args.num and derivada not in cadeias:
			cadeias.append(derivada)

# Separa as cadeias que são constituídas apenas por símbolos terminais e
# do tamanho específicado pelo usuário.
cadeias_finais = []
for cadeia in cadeias:
	# Verifica se a cadeia tem variáveis.
	tem_variavel = False
	for simbolo in cadeia:
		if simbolo in variaveis:
			tem_variavel = True

	# Adiciona apenas as que não tem variáveis e tem o tamanho certo.
	if not tem_variavel and len(cadeia) == args.num:
		cadeias_finais.append(cadeia)

# Imprime as palavras solicitadas pelos usuário. Isto é, aquelas que tem
# o tamanho específicado e são aceitas pela gramática indicada.
for palavra in cadeias_finais:
	print(palavra)
