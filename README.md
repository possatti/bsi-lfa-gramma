# gramma

Programa simples feito em Python 3 para a produção de palavras que sejam reconhecidas por uma gramática. O nome do projeto vem das primeiras letras da palavra em inglês "grammar", para intencionalmente soar engraçado, visto que "gramma" soa como "vózinha" em inglês. O código está hospedado nesse link: https://github.com/possatti/gramma

## Autor
 - Lucas Possatti (@possatti)

## Descrição do projeto

O projeto foi realizado como uma atividade da disciplina de Linguagens Formais e Automatos (LFA) do meu curso. O objetivo é criar um programa que leia uma definição de uma gramática e gere palavras de um determinado tamanho que sejam aceitas pela gramática lida.

A sintaxe com que as gramáticas são definidas é exemplificada abaixo. O exemplo é de uma gramática que reconhece palavras palíndromas compostas pelas letras `a` e `b`. Note que o símbolo `$` significa vazio.

```
V = P
T = a b
S = P
P -> $
P -> a
P -> b
P -> aPa
P -> bPb
P -> aPa
P -> bPb
P -> aPPa
P -> bPPb
```

Veja que, na verdade, é possível definir mais de uma variável (`V = A B C`). O exemplo não define mais de uma, porque não era necessário, neste caso.

E fique atento que os espaços em branco são importantes para separar os elementos da definição. Caso a definição dos símbolos terminais fosse escrita sem espaços ao redor do `=` (`T=a b`), a linha dessa definição não seria reconhecida. Portanto, deixe tudo bem separado por espaços.

## Estrutura e modo de uso

O projeto é basicamente composto por um único arquivo (`gramma.py`) que foi codificado na linguagem Python 3 e é o programa principal. Para executa-lo, basta rodar o seguinte comando:

```bash
$ python3 gramma.py <arquivo da gramatica> <tamanho das palavras>
```

Também é possível ler um pequeno texto de ajuda através da opção `-h`.

Adicionalmente, há uma pasta chamada `samples`, onde estão alguns exemplos de gramáticas, que podem ser usadas para testar o programa.
