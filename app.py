from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem):
    prompt = f"""
    Você é um atendente da pizzaria AMOPIZZA 🍕

    PERSONALIDADE:
    - Simpático, rápido e carismático
    - Fala como humano
    - Sempre tenta vender mais (bebida, borda)

    CARDÁPIO:
    Calabresa, Frango com catupiry, Marguerita, 4 queijos

    TAMANHOS:
    P, M, G

    EXTRAS:
    Borda recheada +8
    Extra queijo +5

    BEBIDAS:
    Coca 2L, Guaraná 2L, Água

    Cliente disse:
    {mensagem}
    """

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Atendente AMOPIZZA"},
            {"role": "user", "content": prompt}
        ]
    )

    return resposta.choices[0].message.content


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    mensagem = data.get("message")

    resposta = gerar_resposta(mensagem)

    return jsonify({"reply": resposta})


@app.route("/")
def home():
    return "AMOPIZZA BOT ONLINE 🍕"


if __name__ == "__main__":
    app.run(port=5000)