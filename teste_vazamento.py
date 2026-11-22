import json
import time
from pathlib import Path
import requests

CODIGO = "AA123456789BR"
ARQUIVO_ESTADO = Path("status_rastreio.json")
WEBHOOK_DISCORD = "SUA_WEBHOOK_URL_AQUI"

def carregar_ultimo_status() -> str:
    if ARQUIVO_ESTADO.exists():
        dados = json.loads(ARQUIVO_ESTADO.read_text(encoding="utf-8"))
        return dados.get(CODIGO, "")
    return ""

def salvar_status(status: str):
    dados = {}
    if ARQUIVO_ESTADO.exists():
        dados = json.loads(ARQUIVO_ESTADO.read_text(encoding="utf-8"))
    dados[CODIGO] = status
    ARQUIVO_ESTADO.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")

def checar_encomenda():
    # API pública de consulta (exemplo Linketrack)
    url = f"https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={CODIGO}"
    resposta = requests.get(url, timeout=15)
    
    if resposta.status_code != 200:
        print("Aguardando disponibilidade da API...")
        return

    eventos = resposta.json().get("eventos", [])
    if not eventos:
        print("Nenhum evento registrado ainda.")
        return

    ultimo_evento = eventos[0]
    status_atual = f"{ultimo_evento['data']} {ultimo_evento['hora']} - {ultimo_evento['status']} ({ultimo_evento['local']})"
    status_anterior = carregar_ultimo_status()

    if status_atual != status_anterior:
        print(f"Atualização detectada: {status_atual}")
        salvar_status(status_atual)
        if WEBHOOK_DISCORD != "SUA_WEBHOOK_URL_AQUI":
            requests.post(WEBHOOK_DISCORD, json={
                "content": f"📦 **Atualização no rastreio `{CODIGO}`:**\n{status_atual}"
            })
    else:
        print("Nenhuma novidade.")

if __name__ == "__main__":
    while True:
        try:
            checar_encomenda()
        except Exception as e:
            print(f"Erro na consulta: {e}")
        time.sleep(1800) # Verifica a cada 30 minutos