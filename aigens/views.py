from django.shortcuts import render
from .forms import PromptGeneratorForm, CampaignGeneratorForm
from .models import PromptHistory

def generate_prompt_view(request):
    generated_prompt = None
    
    if request.method == 'POST':
        form = PromptGeneratorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Função auxiliar para pegar o valor customizado se necessário
            def get_value(field_name):
                val = data.get(field_name)
                if val == 'custom':
                    return data.get(f"{field_name}_custom", "")
                return val

 
# Dentro do bloco if form.is_valid():
# ...
            produto = get_value('produto')
            cenario = get_value('cenario')
            elementos = get_value('elementos')
            luz = get_value('luz')
            clima = get_value('clima')
            estilo = get_value('estilo')
            dimensao = get_value('dimensao') # <-- Nova linha capturando a dimensão
            is_video = data.get('is_video')

# Define o tipo de mídia dinamicamente
            media_type = "video" if is_video else "image"
            if not is_video:
                greeting = f"Please, generate an image according to this prompt:"
            else:
                greeting = ""

            # Montando a Base do Prompt atualizada com a variável media_type
            prompt = (
                f"{greeting}"
                f"Act as an expert art director for a handmade pet stationery brand. "
                f"Create a highly detailed {media_type} prompt. \n"
                f"Subject: {produto}. \n"
                f"Environment: {cenario}. \n"
                f"Props/Elements: {elementos}. \n"
                f"Lighting: {luz}. \n"
                f"Mood/Atmosphere: {clima}. \n"
                f"Visual Style: {estilo}. \n"
                f"Aspect Ratio / Resolution: {dimensao}. "
            )

            # Adicionando regras de vídeo se a caixa estiver marcada
            if is_video:
                acao = data.get('video_acao')
                camera = data.get('video_camera')
                velocidade = data.get('video_velocidade')
                
                prompt += (
                    f"\nVideo Dynamics: "
                    f"Action: {acao}. "
                    f"Camera Movement: {camera}. "
                    f"Speed/Rhythm: {velocidade}."
                )
            
            generated_prompt = prompt
            
            # Salvando no banco
            PromptHistory.objects.create(
                prompt_type='video' if is_video else 'image',
                final_prompt=prompt
            )
    else:
        form = PromptGeneratorForm()

    return render(request, 'aigens/prompt_generator.html', {
        'form': form,
        'generated_prompt': generated_prompt
    })




import os
import time
import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

class MockResponse:
    def __init__(self, text):
        self.text = text

def generate_with_retry(contents, temp, safety, cand_count, tp, tk, max_retries=5):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "teste-449215")
    location = "us-central1"
    
    cred_env_value = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    
    if not cred_env_value:
        print("❌ ERRO: GOOGLE_CREDENTIALS_JSON não encontrado nas variáveis.")
        return None
        
    try:
        # A MÁGICA ACONTECE AQUI:
        # Se o texto começar com '{', ele sabe que é a string da Vercel
        if cred_env_value.strip().startswith('{'):
            cred_dict = json.loads(cred_env_value)
        # Se não, ele sabe que é o caminho do arquivo no seu PC (ex: C:/Users/...)
        else:
            with open(cred_env_value, 'r', encoding='utf-8') as f:
                cred_dict = json.load(f)
                
    except Exception as e:
        print(f"❌ ERRO ao tentar ler as credenciais: {e}")
        return None

    print("✅ Iniciando geração via REST API (Bypass Vercel)...")

    for attempt in range(max_retries):
        try:
            # Gera o token de acesso fresco "na raça"
            credentials = service_account.Credentials.from_service_account_info(
                cred_dict,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            token = credentials.token

            # Monta o pacote de dados para enviar direto ao Vertex AI
            url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/gemini-2.5-pro:generateContent" 
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [{"role": "user", "parts": [{"text": contents}]}],
                "generationConfig": {
                    "temperature": temp,
                    "topP": tp,
                    "topK": tk,
                    "candidateCount": cand_count,
                    "responseMimeType": "application/json"
                }
            }
            
            # Envia o foguete
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                resp_json = response.json()
                text_result = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                print("✅ Sucesso! Texto gerado.")
                return MockResponse(text_result)
            else:
                print(f"❌ Falha na API (Status {response.status_code}): {response.text}")
                if response.status_code == 429: # Cota excedida
                    time.sleep(11)
                else:
                    break
                    
        except Exception as e:
            print(f"❌ Tentativa {attempt+1} falhou com erro Python: {e}")
            time.sleep(2)
            
    return None



def campaign_generator_view(request):
    generated_posts = None
    error_message = None

    if request.method == 'POST':
        form = CampaignGeneratorForm(request.POST)
        if form.is_valid():
            fase = form.cleaned_data['fase']
            pilar = form.cleaned_data['pilar']
            quantidade = form.cleaned_data['quantidade']

            # Payload Base da Mutts
            base_payload = """
            Você é o Diretor de Marketing da "Mutts", uma marca de papelaria artesanal focada em mães de pets.
            PRODUTOS INICIAIS: Caderno Caramelo, Bloco Patinhas, Planner Semanal Pets (feitos à mão, papel de alta gramatura).
            PÚBLICO-ALVO (PERSONA): Mariana, mulher, 40 a 50 anos, dona de um Shih Tzu. Frequenta pet shop toda semana e adora comprar "mimos" fofos para ela ou para dar de presente.
            TOM DE VOZ: Empolgado, acolhedor, íntimo e apaixonado por cachorros e gatos. Use emojis moderadamente.
            """

            # Prompt Dinâmico formatado para JSON
            prompt = f"""
            {base_payload}

            TAREFA:
            Crie {quantidade} postagens para o Instagram para a fase de campanha: {fase}.
            O foco/pilar de conteúdo destas postagens deve ser: {pilar}.

            DIRETRIZES DE SAÍDA:
            Para cada post, forneça:
            1. Um prompt descritivo em inglês para geração de imagem focado no cenário e produto artesanal. Aspect Ratio 1:1.
            2. O texto da legenda em português (com Gancho nas 2 primeiras linhas, Corpo do texto valorizando o produto/artesanal, e um Call to Action claro focando em engajamento ou venda dependendo da fase).

            FORMATO OBRIGATÓRIO:
            Retorne APENAS um objeto JSON válido, sem markdown envolvente (como ```json). 
            Estrutura exigida:
            {{
              "posts": [
                {{
                  "id": 1,
                  "image_prompt_en": "...",
                  "caption_pt": "..."
                }}
              ]
            }}
            """

            # Executando a chamada (ajuste os safety settings conforme sua constante/necessidade)
            response = generate_with_retry(
                contents=prompt,
                temp=0.7, # Temperatura um pouco mais alta para criatividade nos textos
                safety=None, # Substitua pela sua configuração de segurança
                cand_count=1,
                tp=0.95,
                tk=40
            )

            if response and response.text:
                try:
                    # Parse do JSON retornado pelo Gemini
                    json_data = json.loads(response.text)
                    generated_posts = json_data.get('posts', [])
                except json.JSONDecodeError:
                    error_message = "Erro ao decodificar a resposta da IA. O formato JSON estava inválido."
            else:
                error_message = "A API não retornou uma resposta válida após as tentativas."

    else:
        form = CampaignGeneratorForm()

    return render(request, 'aigens/campaign_generator.html', {
        'form': form,
        'generated_posts': generated_posts,
        'error_message': error_message
    })


def marketing_menu(request):
   return render(request, 'aigens/marketing_menu.html' )