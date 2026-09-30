from pathlib import Path

def listar_arquivos(pasta, extensao):
    encontrados = []
    for item in pasta.iterdir():
        if item.suffix.lower() == extensao:
            encontrados.append(item)
    return encontrados

EXTENSOES = {".pdf", ".docx"}

def listar_documentos(pasta):
    encontrados = []
    for item in pasta.rglob("*"):
        if (
            item.is_file()
            and item.suffix.lower() in EXTENSOES
            and not item.name.startswith("~$")
        ):
            encontrados.append(item)
    return encontrados

def classificar(arquivo):
    nome = arquivo.name.lower()
    if "recibo" in nome:
        return "recibo"
    elif "contrato" in nome:
        return "contrato"
    elif "orçam" in nome or "orcam" in nome:
        return "orçamento"
    else:
        return "outro"
    
pasta_teste= Path("teste_entrada")
orcamentos = listar_documentos(pasta_teste)

print("Encontrei", len(orcamentos), "orçamentos:")
for arquivo in orcamentos:
    print(classificar(arquivo), "->", arquivo.name)
