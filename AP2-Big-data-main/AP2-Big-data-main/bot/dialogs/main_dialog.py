# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt
from botbuilder.core import MessageFactory, UserState
from dialogs.matricula_dialog import MatriculaDialog
import json
import os
import logging

logger = logging.getLogger(__name__)

class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.user_state = user_state
        
        # Carregar FAQ do arquivo JSON
        self.faq_data = self._carregar_faq()
        
        # Adicionar diálogo de matrícula
        self.add_dialog(MatriculaDialog(user_state))
        
        # Adicionar prompt de texto
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        # Adicionar diálogo principal
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.processar_mensagem_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    def _carregar_faq(self) -> dict:
        """Carregar perguntas frequentes do arquivo JSON"""
        try:
            # Caminho relativo ao arquivo atual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            faq_path = os.path.join(current_dir, '..', 'data', 'faq.json')
            
            with open(faq_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Erro ao carregar FAQ: {str(e)}")
            # FAQ padrão caso o arquivo não seja encontrado
            return {
                "qual o calendário acadêmico?": "O calendário está disponível em: www.exemplo.edu/calendario",
                "como emitir boleto?": "Acesse o portal do aluno e clique em 'Financeiro'.",
                "quais os horários de aula?": "De segunda a sexta, das 19h às 22h.",
                "secretaria": "secretaria@exemplo.edu",
                "calendario": "O calendário está disponível em: www.exemplo.edu/calendario",
                "boleto": "Acesse o portal do aluno e clique em 'Financeiro'.",
                "horarios": "De segunda a sexta, das 19h às 22h."
            }

    async def processar_mensagem_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Processar a mensagem do usuário"""
        try:
            # Obter mensagem do usuário
            user_message = step_context.context.activity.text
            if not user_message:
                user_message = ""
            
            user_message = user_message.lower().strip()
            logger.info(f"Mensagem recebida: {user_message}")
            
            # Verificar se é uma solicitação de matrícula
            if self._is_matricula_request(user_message):
                return await step_context.begin_dialog(MatriculaDialog.__name__)
            
            # Verificar se é uma pergunta do FAQ
            resposta_faq = self._buscar_resposta_faq(user_message)
            if resposta_faq:
                await step_context.context.send_activity(MessageFactory.text(resposta_faq))
            else:
                # Mensagem padrão se não encontrar resposta
                mensagem_padrao = self._obter_mensagem_padrao()
                await step_context.context.send_activity(MessageFactory.text(mensagem_padrao))
            
            return await step_context.end_dialog()
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            erro_msg = "Desculpe, ocorreu um erro. Tente novamente ou digite 'ajuda' para ver as opções."
            await step_context.context.send_activity(MessageFactory.text(erro_msg))
            return await step_context.end_dialog()

    def _is_matricula_request(self, message: str) -> bool:
        """Verificar se a mensagem é uma solicitação de matrícula"""
        palavras_matricula = [
            'quero me matricular',
            'matricula',
            'matrícula',
            'inscrever',
            'inscrição',
            'fazer matricula',
            'realizar matricula',
            'me matricular',
            'nova matricula',
            'iniciar matricula'
        ]
        
        return any(palavra in message for palavra in palavras_matricula)

    def _buscar_resposta_faq(self, message: str) -> str:
        """Buscar resposta no FAQ baseada na mensagem do usuário"""
        if not self.faq_data:
            return None
        
        # Busca exata primeiro
        if message in self.faq_data:
            return self.faq_data[message]
        
        # Busca por palavras-chave
        for pergunta, resposta in self.faq_data.items():
            if self._mensagem_contem_palavras_chave(message, pergunta):
                return resposta
        
        return None

    def _mensagem_contem_palavras_chave(self, message: str, pergunta: str) -> bool:
        """Verificar se a mensagem contém palavras-chave da pergunta"""
        # Extrair palavras-chave importantes da pergunta
        palavras_pergunta = pergunta.lower().split()
        palavras_importantes = [palavra for palavra in palavras_pergunta 
                              if len(palavra) > 3 and palavra not in ['qual', 'como', 'quais', 'onde', 'quando']]
        
        # Verificar se pelo menos uma palavra importante está na mensagem
        return any(palavra in message for palavra in palavras_importantes)

    def _obter_mensagem_padrao(self) -> str:
        """Obter mensagem padrão quando não há resposta específica"""
        return """🤖 Olá! Sou o assistente virtual da nossa instituição.

Posso te ajudar com:

📚 Perguntas Frequentes:
• Calendário acadêmico
• Como emitir boleto
• Horários de aula
• Contato da secretaria
• Informações sobre cursos

🎓 Matrícula:
• Digite "quero me matricular" para iniciar o processo

💡 Exemplos de perguntas:
• "Qual o calendário acadêmico?"
• "Como emitir boleto?"
• "Quais os horários de aula?"
• "Secretaria"

Como posso te ajudar hoje?"""