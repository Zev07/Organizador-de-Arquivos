import re
import unicodedata
from datetime import datetime
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
    "rua alves nº 41": "São Cristóvão",
    "nossa senhora de lourdes": "Vila Isabel",
    "nossa senhora de lurdes": "Vila Isabel",
    "jornalista orlando dantas": "Laranjeiras",
    "lins de vasconcelos": "Méier",
    "linsde vasconcelos": "Méier",
    "lins vasconcelos": "Méier",
    "pereira soares": "Vila Isabel",
}

MESES = {
    "janeiro": "01",
    "fevereiro": "02",
    "marco": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12",
}


# ---------- Utilidades de texto ----------

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


# ---------- Bairro ----------

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


# ---------- Data ----------

def encontrar_data(texto):
    # Plano A: formato 24/01/2026
    resultado = re.search(r"\d{2}/\d{2}/\d{4}", texto)
    if resultado is not None:
        return resultado.group()

    # Plano B: formato "24 de janeiro de 2026"
    resultado = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", normalizar(texto))
    if resultado is not None:
        dia = resultado.group(1).zfill(2)
        mes = MESES.get(resultado.group(2))
        ano = resultado.group(3)
        if mes is not None:
            return dia + "/" + mes + "/" + ano

    return None


def converter_data(texto_data):
    try:
        data = datetime.strptime(texto_data, "%d/%m/%Y")
    except ValueError:
        return None
    if data.year < 2019 or data > datetime.now():
        return None
    return data


def data_pelo_nome(arquivo):
    resultado = re.search(r"\d{6,}", arquivo.stem)
    if resultado is None:
        return None
    numeros = resultado.group()
    if len(numeros) >= 8:
        # formato DDMMAAAA (o que vier depois é sufixo)
        texto_data = numeros[0:2] + "/" + numeros[2:4] + "/" + numeros[4:8]
    else:
        # formato DDMMAA (6 ou 7 dígitos)
        texto_data = numeros[0:2] + "/" + numeros[2:4] + "/20" + numeros[4:6]
    return converter_data(texto_data)


def descobrir_data(arquivo, cabecalho):
    data_texto = encontrar_data(cabecalho)
    if data_texto is not None:
        data = converter_data(data_texto)
        if data is not None:
            return data
    # Plano C: o nome do arquivo
    return data_pelo_nome(arquivo)


# ---------- Teste em massa ----------

pasta = Path("teste_entrada")
contagem = {}
sem_bairro = 0
sem_data = 0

for arquivo in pasta.rglob("*.docx"):
    if arquivo.name.startswith("~$"):
        continue
    cabecalho = ler_cabecalho(arquivo)

    bairro = encontrar_bairro(cabecalho)
    if bairro is None:
        print("SEM BAIRRO ->", arquivo.name)
        sem_bairro += 1
    else:
        contagem[bairro] = contagem.get(bairro, 0) + 1

    data = descobrir_data(arquivo, cabecalho)
    if data is None:
        print("SEM DATA ->", arquivo.name, "|", cabecalho[:80])
        sem_data += 1

print("========== BAIRROS ==========")
for bairro in sorted(contagem):
    print(bairro, "->", contagem[bairro])
print("Sem bairro:", sem_bairro, "| Sem data:", sem_data)