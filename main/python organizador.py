from pathlib import Path

def listar_arquivos(pasta, extensao):
    encontrados = []
    for item in pasta.iterdir():
        if item.suffix.lower() == extensao:
            encontrados.append(item)
    return encontrados

EXTENSOES = {".pdf", ".docx"}

def listar_orcamentos(pasta):
    encontrados = []
    for item in pasta.rglob("*"):
        if (
            item.is_file()
            and item.suffix.lower() in EXTENSOES
            and not item.name.startswith("~$")
        ):
            encontrados.append(item)
    return encontrados

pasta_teste= Path("teste_entrada")
orcamentos = listar_orcamentos(pasta_teste)

print("Encontrei", len(orcamentos), "orçamentos:")
for arquivo in orcamentos:
    print(arquivo.name, "-> pasta:", arquivo.parent.name)
