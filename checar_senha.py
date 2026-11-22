import requests
from bs4 import BeautifulSoup

def obter_clima():
    # Coordenadas de Caçapava - SP (Open-Meteo API)
    url = "https://api.open-meteo.com/v1/forecast?latitude=-23.1008&longitude=-45.7069¤t=temperature_2m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FSao_Paulo"
    dados = requests.get(url, timeout=10).json()
    atual = dados["current"]["temperature_2m"]
    maxima = dados["daily"]["temperature_2m_max"][0]
    minima = dados["daily"]["temperature_2m_min"][0]
    return f"🌡️ **Clima (Caçapava):** {atual}°C agora (Mín: {minima}°C / Máx: {maxima}°C)"

def obter_cotacoes():
    # AwesomeAPI (Dólar e Bitcoin em BRL)
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,BTC-BRL"
    dados = requests.get(url, timeout=10).json()
    dolar = float(dados["USDBRL"]["bid"])
    btc = float(dados["BTCBRL"]["bid"])
    return f"💵 **Cotações:** Dólar R$ {dolar:.2f} | Bitcoin R$ {btc:,.2f}"

def obter_manchetes():
    # Feed RSS do Google Notícias Brasil
    url = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"
    xml = requests.get(url, timeout=10).text
    soup = BeautifulSoup(xml, "xml")
    itens = soup.find_all("item", limit=3)
    
    manchetes = ["📰 **Top 3 Manchetes:**"]
    for i, item in enumerate(itens, 1):
        titulo = item.title.text.split(" - ")[0] # Remove o nome do portal no final
        manchetes.append(f"{i}. {titulo}")
    return "\n".join(manchetes)

def enviar_discord(webhook_url: str, mensagem: str):
    requests.post(webhook_url, json={"content": mensagem}, timeout=10)

if __name__ == "__main__":
    resumo = f"**☀️ Resumo Diário**\n\n{obter_clima()}\n{obter_cotacoes()}\n\n{obter_manchetes()}"
    print(resumo)
    # Para enviar ao Discord, descomente abaixo e insira sua URL de Webhook:
    # enviar_discord("SUA_WEBHOOK_URL_AQUI", resumo)