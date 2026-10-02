import re

texto = "  20/06/2026  Orçamento     Destinatário: Rua Nossa Senhora de Lourdes"

resultado = re.search(r"\d{2}/\d{2}/\d{4}", texto)
print(resultado.group())    # 20/06/2026

resultado = re.search(r"\d{2}/\d{2}/\d{4}", "texto sem data nenhuma")
if resultado is None:
    print("não achei")

resultado = re.search(r"(\d{2})/(\d{2})/(\d{4})", texto)
print(resultado.group(1))   # 20     (o dia)
print(resultado.group(2))   # 06     (o mês)
print(resultado.group(3))   # 2026   (o ano)

estranho = "9017/07/2025  Orçamento"
resultado = re.search(r"(\d{2})/(\d{2})/(\d{4})", estranho)
print(resultado.group())