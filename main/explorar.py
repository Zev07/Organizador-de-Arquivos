import unicodedata
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


BAIRROS = {
    "agua santa": "Água Santa",
    "andarai": "Andaraí",
    "benfica": "Benfica",
    "botafogo": "Botafogo",
    "cachambi": "Cachambi",
    "copacabana": "Copacabana",
    "engenho de dentro": "Engenho de Dentro",
    "engenho novo": "Engenho Novo",
    "gavea": "Gávea",
    "grajau": "Grajaú",
    "humaita": "Humaitá",
    "ipanema": "Ipanema",
    "laranjeiras": "Laranjeiras",
    "madureira": "Madureira",
    "mangueira": "Mangueira",
    "maracana": "Maracanã",
    "meier": "Méier",
    "piedade": "Piedade",
    "praca da bandeira": "Praça da Bandeira",
    "ramos": "Ramos",
    "rio comprido": "Rio Comprido",
    "rio cumprido": "Rio Comprido",
    "sampaio": "Sampaio",
    "sao cristovao": "São Cristóvão",
    "tijuca": "Tijuca",
    "vasco da gama": "Vasco da Gama",
    "vila isabel": "Vila Isabel",
    "vila izabel": "Vila Isabel",
}

RUAS = {
    "alves montes": "São Cristóvão",
    "coronel cabrita": "São Cristóvão",
    "vaz de toledo": "Engenho Novo",
    "nossa senhora de lourdes": "Vila Isabel",
    "nossa senhora de lurdes": "Vila Isabel",
    "jornalista orlando dantas": "Laranjeiras",
    "lins de vasconcelos": "Méier",
    "linsde vasconcelos": "Méier",
    "lins vasconcelos": "Méier",
    "pereira soares": "Vila Isabel",
}


def normalizar(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    resultado = ""
    for letra in decomposto:
        if not unicodedata.combining(letra):
            resultado = resultado + letra
    return resultado.lower()


def texto_do_paragrafo(paragrafo_xml):
    texto = ""
    for pedaco in paragrafo_xml.iter(qn("w:t")):
        if pedaco.text:
            texto = texto + pedaco.text
    return texto.strip()


def ler_cabecalho(arquivo):
    doc = Document(arquivo)
    cabecalho = ""
    for paragrafo_xml in doc.element.body.iter(qn("w:p")):
        texto = texto_do_paragrafo(paragrafo_xml)
        if texto.startswith("Serviços"):
            break
        cabecalho = cabecalho + " " + texto
    return cabecalho


def procurar(texto, dicionario):
    encontrados = []
    for chave in dicionario:
        if chave in texto:
            valor = dicionario[chave]
            if valor not in encontrados:
                encontrados.append(valor)
    return encontrados


def encontrar_bairro(texto):
    texto = normalizar(texto)

    pelas_ruas = procurar(texto, RUAS)
    if len(pelas_ruas) == 1:
        return pelas_ruas[0]

    pelos_bairros = procurar(texto, BAIRROS)
    if len(pelos_bairros) == 1:
        return pelos_bairros[0]

    return None


pasta = Path("teste_entrada")
contagem = {}
revisar = 0

for arquivo in pasta.rglob("*.docx"):
    if arquivo.name.startswith("~$"):
        continue
    cabecalho = ler_cabecalho(arquivo)
    bairro = encontrar_bairro(cabecalho)
    if bairro is None:
        print("REVISAR ->", arquivo.name, "|", cabecalho[:120])
        revisar += 1
    else:
        contagem[bairro] = contagem.get(bairro, 0) + 1

print("========== BAIRROS ==========")
for bairro in sorted(contagem):
    print(bairro, "->", contagem[bairro])
print("Para revisar:", revisar)