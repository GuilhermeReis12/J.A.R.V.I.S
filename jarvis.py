import openai
import speech_recognition as sr
import pyttsx3
import logging

# Configurar a chave de API da OpenAI
openai.api_key = 'chave'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def reconhecer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Ajustando o nível de ruído...")
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Diga algo...")
        audio = recognizer.listen(source)
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        logging.info(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        logging.error("Não entendi o que você disse.")
        return None
    except sr.RequestError as e:
        logging.error(f"Erro ao se comunicar com o serviço de reconhecimento de voz: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado no reconhecimento de voz: {e}")
        return None

def obter_resposta(texto):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de IA."},
                {"role": "user", "content": texto}
            ]
        )
        resposta = response['choices'][0]['message']['content'].strip()
        logging.info(f"Resposta da IA: {resposta}")
        return resposta
    except openai.error.OpenAIError as e:
        logging.error(f"Erro ao obter resposta da OpenAI: {e}")
        return "Desculpe, ocorreu um erro ao tentar obter a resposta."
    except Exception as e:
        logging.error(f"Erro inesperado ao obter resposta: {e}")
        return "Desculpe, ocorreu um erro inesperado."

def falar(texto):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  
        engine.setProperty('volume', 1) 
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) 
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Erro ao tentar falar: {e}")

def main():
    while True:
        texto = reconhecer_voz()
        if texto:
            if 'sair' in texto.lower():
                logging.info("Saindo do aplicativo...")
                falar("Encerrando o aplicativo. Até logo!")
                break
            resposta = obter_resposta(texto)
            if resposta:
                print(f"JARVIS: {resposta}")
                falar(resposta)
            else:
                logging.error("Nenhuma resposta obtida da IA.")
                falar("Desculpe, não consegui obter uma resposta.")

if __name__ == "__main__":
    main()
