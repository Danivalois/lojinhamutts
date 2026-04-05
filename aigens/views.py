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




from google.oauth2 import service_account # ADICIONE ESTE IMPORT NO TOPO

import os
import time
import json
from google import genai

import os
import time
from google import genai

def generate_with_retry(contents, temp, safety, cand_count, tp, tk, max_retries=5):
    project_id = "teste-449215"
    
    # 1. TESTE HARDCODED: Cole TODO o conteúdo do seu arquivo .json aqui dentro das aspas triplas
    json_string = """{
  "type": "service_account",
  "project_id": "teste-449215",
  "private_key_id": "f194574e2dfbbf8cd3f4be266b7bb0f363c9461f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDA2ClYPNTFHf/U\nQHR4l7kcwArCmZpmAAtLm3qqRKlFWep4UfBncU2JmclSo8P/M/ofc3MJc8qURrfd\nZWTclAD75UDegNaaxYwLs13N+xcMRLw368ayDfgZtNt40UrcHlQD2OFVJZzIu+0B\nd8ezLA7Twg5M9Ig6O3lt6CL52wetuqJc9j8ZUYZjsY2ccFT3h9xrQqOrl78/hdn0\nWNXJUzuMC2Qajfy7SGyTWGkdrsB3ciKN3Xg364IRxdYDsLu/XIKX+CouqWnEvjy1\nBoucIT/1vA42e3mGNDuIbQpLVbWrg+hH6DIfdfgOfgVDwuyvfOF1XpBTyPqjRlqY\nj1+Aa/ofAgMBAAECggEAIIx7kfqWePzCwNruLaqCIoGhb04Iut2YCndgIVv8bAms\nowlFd9guW6K60bl1a94kgel1CavjDdrPzsz91KMgdWOw6r05O59LL3BjTVBrh/UU\nBaZEf6oO7ZvSjVZZ+cQerxWMltgF2fWqH5zNdobhq8ktq7x8P8PpD21mdeCLr70s\nwnaDcQAsEUOedAEjLCo6XpiY83g4jqNg+JByeR9qMSuO+5KMowLfqZUP4dIpQfS4\ndPeHRqe59m2epyBWsXPRhfoh1oCXYYsJs0SdOKc0ZPV4YHDZJ9o4W2SyOEi0RG/V\nU1s4XHfo5uSjOrd9c5+TQy0tKHgiAumF+38+nfhA3QKBgQDx86A1qpwvP8qbIzyZ\nDWjZMcZBQVQuGzv11sahj7f4CWqJSXAS4eYvV1bFw88Xg60/rQ1sLPs6GafFSFQK\nwUei0wBnKm26H6NFWU+WuOS8iYDQN3UXu08eq4lvOa5aZUnYEZ0E6+rOL78bEfQS\nyM3JqB/bkeCjriqHlgU/qYpZowKBgQDMCpqlwPf92s+o8bgKVx3yfAMcvZNyEEJy\nrgWqTPrlcTUJubHu82t1Mi1Gkng9/hpkLPdWu8zGyoXuRv9hsls1Dqz9bV0G24Rm\n0jCQQRWVzm6FIRkpHCGGCPzLbWs3p0mh+dqRUKbSpb4o6pdEwFLA81cdU8X18IaH\nb1TDyCRdVQKBgQC9itrOUAqs5S+Gm3Mkf6HMzLaAdnpI6GLvs0LGXH2FnXLNfC+F\nS1z1Z1l98mixBiHaCWrDfPWOzXxmC8Ry7Hl/MAdXyqBNN+3DLTUxYUUoAhxcgaWE\nYuOXplAzRx+0hzbzQtEcgujef/8ZaNYpRRAZ01CpxT0TXSTKNReFiP7uOwKBgQCn\n6romWs47/c0T7glViSg+HEy7ZFBpeHQWyJwk8MEx/Z52aHnEelMe2bJk97k421uA\nwXizyk3V82mRFKCrGArzeSZoUY5TTGiD7crFjKpk5MQTj4+TQ3FbSx4vk9a+sE9q\nm6KCIGuJw5jhN15R2CzCWgCBRCYQJmewIbEShi1XGQKBgGvuJyph0LAiXEcRuP4N\nckwDaUSY502h12fra/3rfGBITRiG+wTbgB3Nj2cj8Vvjamuf4VkUtKub9kPJxlIf\nu3tYVr52YEZIU5DFeJMuYNmHf10MOJVKmPqgGmgcrSpfBbt0RrnlKwQQUPEKTRne\nEOt9KUZ5vLpSpqWP99W+7oY/\n-----END PRIVATE KEY-----\n",
  "client_email": "ajax-backend@teste-449215.iam.gserviceaccount.com",
  "client_id": "104464953281056038734",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ajax-backend%40teste-449215.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""
    
    # 2. Escreve a string hardcodada em um arquivo real dentro do servidor da Vercel
    tmp_path = "/tmp/teste-449215-f194574e2dfb.json"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(json_string)
        print("✅ Arquivo JSON temporário criado com sucesso na Vercel.")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo temporário: {e}")
            
    # 3. Aponta o caminho para a biblioteca do Google
    os.environ["GOOGLE_CREDENTIALS_JSON"] = tmp_path

    # 4. Inicializa o cliente
    try:
        client = genai.Client(
            vertexai=True, 
            project=project_id, 
            location="global"
        )
        print("✅ Cliente Vertex AI inicializado.")
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return None
    
    print("XXXXX contents, temp, safety pre engine TEXT", contents, temp, cand_count, tp, tk, safety )
    from google.genai import types


    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash', #gemini-2.5-pro',
                contents=contents,
            config=types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                temperature=temp,
                safety_settings=safety,
                candidate_count=cand_count,
                top_p=tp,
                top_k=tk,
                response_mime_type="application/json"
                )
            )
            print("XXXX response after engine", response)
            return response
        
        except Exception as e:
            print(f"Tentativa {attempt+1} falhou: {e}")
            if "429" in str(e) or "500" in str(e):
                time.sleep(11)
            else:
                break
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