from django.db import models

class PromptHistory(models.Model):
    TYPE_CHOICES = (
        ('image', 'Imagem'),
        ('video', 'Vídeo'),
    )
    
    prompt_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')
    final_prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt {self.id} - {self.prompt_type} - {self.created_at.strftime('%d/%m/%Y')}"