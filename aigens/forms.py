from django import forms

class PromptGeneratorForm(forms.Form):
    CUSTOM_VALUE = 'custom'
    
    # --- OPÇÕES PADRÃO ---
    PRODUTO_CHOICES = [
        ('Caderno espiral com capa de vira-lata caramelo', 'Caderno Caramelo'),
        ('Bloco de notas pequeno com estampa de patinhas', 'Bloco de Notas Patinhas'),
        ('Planner semanal com ilustrações de pets', 'Planner Semanal Pets'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]


    # Adicione esta lista junto com as outras opções (PRODUTO_CHOICES, etc.)
    DIMENSAO_CHOICES = [
        ('1:1 (Square, 1080x1080) - Instagram Post', 'Post Quadrado (1:1)'),
        ('9:16 (Vertical, 1080x1920) - Instagram Reels, Stories, TikTok', 'Reels / Stories (9:16)'),
        ('4:5 (Portrait, 1080x1350) - Instagram Portrait Post', 'Post Retrato (4:5)'),
        ('2:3 (Vertical, 1000x1500) - Pinterest Pin', 'Pinterest Pin (2:3)'),
        ('16:9 (Landscape, 1920x1080) - YouTube Video', 'Paisagem (16:9)'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]


    CENARIO_CHOICES = [
        ('Mesa de madeira clara de uma cafeteria', 'Mesa de Cafeteria'),
        ('Bancada de ateliê artesanal de madeira rústica', 'Bancada de Ateliê'),
        ('Cama aconchegante com lençóis brancos', 'Cama Aconchegante'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]
    ELEMENTOS_CHOICES = [
        ('Xícara de café fumegante, canetas coloridas', 'Café e Canetas'),
        ('Fitas washi, agulha de encadernação, linha', 'Ferramentas de Artesanato'),
        ('Embalagem de presente de papel craft, laço', 'Embalagem de Presente'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]
    LUZ_CHOICES = [
        ('Luz natural suave da manhã entrando pela janela', 'Luz da Manhã'),
        ('Iluminação de estúdio clara e minimalista', 'Estúdio Claro'),
        ('Luz quente e dourada de fim de tarde (Golden Hour)', 'Golden Hour'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]
    CLIMA_CHOICES = [
        ('Aconchegante, nostálgico e acolhedor', 'Aconchegante'),
        ('Fofo, divertido e vibrante', 'Fofo e Divertido'),
        ('Profissional, limpo e organizado', 'Profissional'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]
    ESTILO_CHOICES = [
        ('Fotografia realista macro com foco no detalhe', 'Macro Realista'),
        ('Fotografia flat-lay vista de cima', 'Flat-lay (Vista de cima)'),
        ('Fotografia de produto para e-commerce', 'Estúdio de Produto'),
        (CUSTOM_VALUE, 'Customizar...'),
    ]

    # --- OPÇÕES DE VÍDEO (Sem customizar) ---
    ACAO_CHOICES = [
        ('', '--- Selecione (Apenas Vídeo) ---'),
        ('Fumaça do café subindo suavemente', 'Fumaça Subindo'),
        ('Poeira brilhante flutuando na luz', 'Poeira Brilhante'),
        ('Páginas do caderno virando com o vento', 'Páginas Virando'),
    ]
    CAMERA_CHOICES = [
        ('', '--- Selecione (Apenas Vídeo) ---'),
        ('Zoom in lento', 'Aproximação Lenta'),
        ('Câmera estática', 'Estática'),
        ('Panorâmica suave da esquerda para a direita', 'Panorâmica (Pan)'),
    ]
    VELOCIDADE_CHOICES = [
        ('', '--- Selecione (Apenas Vídeo) ---'),
        ('Velocidade normal e suave', 'Normal'),
        ('Câmera lenta (slow-motion)', 'Câmera Lenta'),
    ]

    # Campos Dropdown
    is_video = forms.BooleanField(required=False, label="Gerar prompt para Vídeo?")
    
    produto = forms.ChoiceField(choices=PRODUTO_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    produto_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))
    
    cenario = forms.ChoiceField(choices=CENARIO_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    cenario_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))
    
    elementos = forms.ChoiceField(choices=ELEMENTOS_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    elementos_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))
    
    luz = forms.ChoiceField(choices=LUZ_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    luz_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))
    
    clima = forms.ChoiceField(choices=CLIMA_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    clima_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))
    
    estilo = forms.ChoiceField(choices=ESTILO_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    estilo_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))

    # Campos de Vídeo
    video_acao = forms.ChoiceField(choices=ACAO_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select video-only'}))
    video_camera = forms.ChoiceField(choices=CAMERA_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select video-only'}))
    video_velocidade = forms.ChoiceField(choices=VELOCIDADE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select video-only'}))

    # E adicione estes dois campos junto com os outros campos do form:
    dimensao = forms.ChoiceField(choices=DIMENSAO_CHOICES, widget=forms.Select(attrs={'class': 'form-select trigger-custom'}))
    dimensao_custom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mt-2 custom-input', 'style': 'display:none;'}))





from django import forms

class CampaignGeneratorForm(forms.Form):
    FASE_CHOICES = [
        ('Pré-Lançamento', 'Pré-Lançamento (Foco em Antecipação/Mistério)'),
        ('Lançamento', 'Lançamento (Foco em Venda/Urgência)'),
        ('Tração', 'Tração (Foco em Autoridade/Prova Social)'),
        ('Operação', 'Operação Contínua (Rotina de Manutenção)'),
    ]
    
    PILAR_CHOICES = [
        ('Produto (40%)', 'Produto (Foco nos detalhes, uso e desejo)'),
        ('Bastidores (20%)', 'Bastidores (Foco no processo artesanal e perrengues)'),
        ('Inspiração/Conexão (20%)', 'Inspiração (Foco no amor por pets e dicas)'),
    ]

    QUANTIDADE_CHOICES = [(i, str(i)) for i in range(1, 6)] # 1 a 5 posts por vez para não estourar o timeout

    fase = forms.ChoiceField(choices=FASE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    pilar = forms.ChoiceField(choices=PILAR_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    quantidade = forms.ChoiceField(choices=QUANTIDADE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))