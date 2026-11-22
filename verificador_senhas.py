import hashlib
import requests

def verificar_senha(senha: str):
    # Gera o hash SHA-1 em maiúsculo
    sha1 = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
    prefixo, sufixo = sha1[:5], sha1[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefixo}"
    resposta = requests.get(url, timeout=10)
    
    if resposta.status_code != 200:
        raise RuntimeError(f"Erro na API: {resposta.status_code}")
    
    # Cada linha retornada tem o formato SUFIXO:CONTAGEM
    hashes = (linha.split(':') for linha in resposta.text.splitlines())
    for h, contagem in hashes:
        if h == sufixo:
            print(f"⚠️ Senha comprometida! Encontrada {int(contagem):,} vezes em vazamentos.")
            return
            
    print("✅ Senha segura! Não encontrada nos vazamentos conhecidos.")

if __name__ == "__main__":
    senha_teste = input("Digite a senha para testar: ")
    verificar_senha(senha_teste)