from pathlib import Path

def listar_arquivos(pasta, extensao):
    encontrados = []
    for item in pasta.iterdir():
        if item.suffix.lower() == extensao:
            encontrados.append(item)
    return encontrados

pasta_teste= Path("teste_entrada")

pdfs = listar_arquivos(pasta_teste, ".pdf")

print("Encontrei", len(pdfs), "PDFs:")
for arquivo in pdfs:
    print(arquivo.name)

