#Algoritmos First,Follow e Predictive Table

# Variaveis globais

G = {}
naoTerminais = []
terminais = []
firstVisitado = {}
followVisitado = {}
derivaLambda = {}
simboloVazio = "e"
simbolosTerminais = [";", ":", ",", "(", ")", "=",
                     "<", ">", "+", "-", "&", "*",
                     "/", "identifier",
                     "ALIASED", "BOX", "CONSTANT",
                     "IS_ASSIGNED", "IS", "SUBTYPE",
                     "DIGITS", "NEW", "RANGE", "DOT_DOT",
                     "TIC", "MOD", "DIGITS", "DELTA",
                     "ARRAY", "OF", "RECORD", "NULL",
                     "TAGGED", "ACCESS", "CASE", "WHEN",
                     "RIGHT_SHAFT", "PIPE", "ALL", "PROCEDURE",
                     "RETURN", "FUNCTION", "PROTECTED",
                     "PRAGMA", "PRIVATE", "PACKAGE",
                     "USE", "BODY", "IS", "END",
                     "ABSTRACT", "SEPARATE", "WITH",
                     "TYPE"]

# Funções comun

def Uniao(listaA, listaB):
    for i in listaB:
        if i in listaA:
            continue
        else:
            listaA.append(i)
    return listaA

def EhTerminal(simbolo):
    if simbolo == simboloVazio:
        return False
    if simbolo == "|":
        return False
    if simbolo in simbolosTerminais:
        return True
    return simbolo.isupper()

#Abrindo o arquivo

arquivo = open("gramaticaAda.txt")

for linha in arquivo.readlines():
    naoTerminal = linha.split(":")[0].strip()
    naoTerminais += [naoTerminal] 
    firstVisitado[naoTerminal] = False
    followVisitado[naoTerminal] = False
    derivaLambda[naoTerminal] = False
    linha = linha.strip('\n')
    terminal = filter(EhTerminal, linha.split(":")[1].split(" "))
    Uniao(terminais, terminal)
    producoes = []
    for producao in linha.split(":")[1].split('|'):
        simbolos = [];
        for simbolo in producao.split(" "):
            if simbolo != "":
                simbolos += [simbolo]
        producoes += [simbolos]
    G[naoTerminal] = producoes

arquivo.close()

terminais.sort()
terminais.append("$")

# Funções do First

def SimboloDerivaLambda(producao):
    for simbolo in producao:
        if simbolo != simboloVazio and not EhTerminal(simbolo) and derivaLambda[simbolo]:
            continue
        else:
            return False
    return True

def AlgumaProducaoDerivaLambda(naoTerminal):
    for producao in G[naoTerminal]:
        if SimboloDerivaLambda(producao):
            return True
        else:
            continue
    return False

def FirstInterno(Xb):
    if Xb[0] == "" or Xb[0] == simboloVazio:
        return []
    if EhTerminal(Xb[0]):
        return [Xb[0]]
    conjunto = []
    if not firstVisitado[Xb[0]]:
        firstVisitado[Xb[0]] = True
        for producao in G[Xb[0]]:
            conjunto = Uniao(conjunto, FirstInterno(producao))
    if simboloVazio in G[Xb[0]]:
        conjunto = Uniao(conjunto, FirstInterno(Xb[1:]))
    return conjunto

# Função First
def First(a):
    for A in naoTerminais:
        for producao in G[A]:    
            derivaLambda[A] = simboloVazio in producao
            firstVisitado[A] = False
    conjunto = FirstInterno([a])
    if (a != "" and not EhTerminal(a)) and (derivaLambda[a] or AlgumaProducaoDerivaLambda(a)):
        conjunto = Uniao(conjunto, [simboloVazio])
    return conjunto

# Funções do Follow
def Ocorrencias(A):
    ocorrencia = []
    for naoTerminal in naoTerminais:
        for corpoDaProducao in G[naoTerminal]:
            if A in corpoDaProducao:
                ocorrencia.append({"NT":naoTerminal,"CP":corpoDaProducao})
    return ocorrencia

def Cauda(corpoDaProducao, naoTerminal):
    indiceDoNaoTerminal = corpoDaProducao.index(naoTerminal)
    return corpoDaProducao[(indiceDoNaoTerminal + 1):]

def TodosDerivamVazio(y):
    for X in y:
        if X.islower() or (X.isupper() and not derivaLambda[X]):
            return False
    return True

def FollowInterno(A):
    ans = []
    if A == "S":
        return ["$"]
    if not followVisitado[A]:
        followVisitado[A] = True
        for a in Ocorrencias(A):
            ans = Uniao(First(Cauda(a["CP"], A)), ans)
            if TodosDerivamVazio(Cauda(a["CP"], A)):
                ans = Uniao(ans, FollowInterno(a["NT"]))
    return ans

# Função Follow

def Follow(a):
    for A in naoTerminais:
        derivaLambda = simboloVazio in G[A]
        followVisitado[A] = False
    ans = FollowInterno(a)
    return ans

# Visualização

##def printTabela(tabela):
##    tamanhoColuna = [max(len(x) for x in col) for col in zip(*tabela)]
##    for linha in tabela:
##        print("| " + " | ".join("{:{}}".format(x, tamanhoColuna[i])
##                                for i, x in enumerate(linha)) + " |")
##
##tabelaFirstAndFollow = [["Nao Terminal", "First", "Follow"]]
##for naoTerminal in naoTerminais:
##    tabelaFirstAndFollow.append([naoTerminal, str(First(naoTerminal)), str(Follow(naoTerminal))])
##
##printTabela(tabelaFirstAndFollow)

###Tabela preditiva
##
##TabelaPreditiva = {}
##def inicializarTabelaPreditiva():
##    for naoTerminal in naoTerminais:
##        TabelaPreditiva[naoTerminal] = {}
##        for terminal in terminais:
##            TabelaPreditiva[naoTerminal][terminal] = "ERRO"
##
##def gerarTabelaPreditiva():
##    for nt in G:
##        for p in G[nt]:
##            conjuntoFirst = First(p)
##            conjuntoFollow = Follow(nt)
##            for a in conjuntoFirst:
##                TabelaPreditiva[str(nt)][str(a)] = {str(nt): [p]}
##            if simboloVazio in conjuntoFirst or len(conjuntoFirst) == 0:
##                for b in conjuntoFollow:
##                    TabelaPreditiva[str(nt)][str(b)] = {str(nt): [p]}
##            if (simboloVazio in conjuntoFirst or len(conjuntoFirst) == 0) and "$" in conjuntoFollow:
##                TabelaPreditiva[str(nt)]["$"] = {str(nt): [p]}
##
##def printTabelaPreditiva(tabelaPreditiva):
##    tabela = []
##    cabecalho = ["Nao Terminal"]
##    for terminal in terminais:
##        cabecalho.append(terminal)
##    tabela.append(cabecalho)
##    for naoTerminal in naoTerminais:
##        linha = [naoTerminal]
##        for terminal in terminais:
##            linha.append(str(tabelaPreditiva[naoTerminal][terminal]))
##        tabela.append(linha)
##    printTabela(tabela)
##
##print("\nTabela Preditiva")
##inicializarTabelaPreditiva()
##gerarTabelaPreditiva()
##printTabelaPreditiva(TabelaPreditiva)
