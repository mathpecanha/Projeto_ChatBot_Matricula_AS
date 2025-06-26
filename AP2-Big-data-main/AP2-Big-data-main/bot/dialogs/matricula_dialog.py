from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    PromptOptions,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptValidatorContext
from botbuilder.core import MessageFactory, UserState
import requests
import json
import re
import logging

logger = logging.getLogger(__name__)

class MatriculaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MatriculaDialog, self).__init__(MatriculaDialog.__name__)
        
        self.user_state = user_state
        
        # Lista de cursos disponíveis
        self.cursos_disponiveis = [
            "Engenharia",
            "Administração", 
            "Direito",
            "Medicina",
            "Tecnologia da Informação"
        ]
        
        # Adicionar diálogos
        self.add_dialog(TextPrompt("nome_prompt", self._validar_nome))
        self.add_dialog(TextPrompt("email_prompt", self._validar_email))
        self.add_dialog(TextPrompt("curso_prompt", self._validar_curso))
        
        self.add_dialog(
            WaterfallDialog(
                "matricula_waterfall",
                [
                    self._step_nome,
                    self._step_email,
                    self._step_curso,
                    self._step_confirmar,
                    self._step_final
                ]
            )
        )
        
        self.initial_dialog_id = "matricula_waterfall"
    
    async def _step_nome(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Primeiro passo: coletar nome"""
        prompt_message = MessageFactory.text("Ótimo! Vamos começar sua matrícula. Qual é o seu nome completo?")
        return await step_context.prompt(
            "nome_prompt",
            PromptOptions(prompt=prompt_message, retry_prompt=MessageFactory.text("Por favor, digite seu nome completo (mínimo 2 palavras):"))
        )
    
    async def _step_email(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Segundo passo: coletar email"""
        step_context.values["nome"] = step_context.result
        
        prompt_message = MessageFactory.text(f"Perfeito, {step_context.result}! Agora preciso do seu email:")
        return await step_context.prompt(
            "email_prompt",
            PromptOptions(prompt=prompt_message, retry_prompt=MessageFactory.text("Por favor, digite um email válido (exemplo: seuemail@exemplo.com):"))
        )
    
    async def _step_curso(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Terceiro passo: coletar curso"""
        step_context.values["email"] = step_context.result
        
        cursos_texto = "\n".join([f"• {curso}" for curso in self.cursos_disponiveis])
        prompt_message = MessageFactory.text(f"Excelente! Agora escolha um dos cursos disponíveis:\n\n{cursos_texto}\n\nDigite o nome do curso desejado:")
        
        return await step_context.prompt(
            "curso_prompt",
            PromptOptions(prompt=prompt_message, retry_prompt=MessageFactory.text(f"Por favor, escolha um dos cursos disponíveis:\n{cursos_texto}"))
        )
    
    async def _step_confirmar(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Quarto passo: confirmar dados"""
        step_context.values["curso"] = step_context.result
        
        nome = step_context.values["nome"]
        email = step_context.values["email"]
        curso = step_context.values["curso"]
        
        confirmacao_texto = f"""
📋 **Confirmação dos Dados da Matrícula**

**Nome:** {nome}
**Email:** {email}
**Curso:** {curso}

Os dados estão corretos? Digite 'sim' para confirmar ou 'não' para cancelar.
        """
        
        prompt_message = MessageFactory.text(confirmacao_texto)
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=prompt_message)
        )
    
    async def _step_final(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Passo final: processar matrícula"""
        confirmacao = step_context.result.lower()
        
        if confirmacao in ['sim', 's', 'yes', 'y', 'confirmar', 'ok']:
            # Enviar dados para o backend
            nome = step_context.values["nome"]
            email = step_context.values["email"]
            curso = step_context.values["curso"]
            
            sucesso = await self._enviar_matricula(nome, email, curso)
            
            if sucesso:
                mensagem_sucesso = f"""
🎉 **Matrícula Realizada com Sucesso!**

Parabéns, {nome}! Sua matrícula no curso de {curso} foi processada.

📧 Um email de confirmação será enviado para: {email}

Em breve você receberá mais informações sobre:
• Data de início das aulas
• Material necessário
• Acesso ao portal do aluno

Bem-vindo(a) à nossa instituição! 🎓
                """
                await step_context.context.send_activity(MessageFactory.text(mensagem_sucesso))
            else:
                mensagem_erro = """
❌ **Erro ao Processar Matrícula**

Desculpe, ocorreu um erro ao processar sua matrícula. 

Possíveis causas:
• Backend não está rodando (execute: python run.py)
• Problema de conexão com o servidor
• Email já cadastrado no sistema

Por favor, tente novamente mais tarde ou entre em contato com a secretaria: secretaria@exemplo.edu

Você pode tentar novamente digitando 'quero me matricular'.
                """
                await step_context.context.send_activity(MessageFactory.text(mensagem_erro))
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Matrícula cancelada. Se mudar de ideia, digite 'quero me matricular' a qualquer momento!")
            )
        
        return await step_context.end_dialog()
    
    async def _enviar_matricula(self, nome: str, email: str, curso: str) -> bool:
        """Enviar dados da matrícula para o backend"""
        try:
            url = "http://localhost:8080/api/matriculas"
            dados = {
                "nome": nome,
                "email": email,
                "curso": curso
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            logger.info(f"Tentando enviar matrícula para: {url}")
            logger.info(f"Dados: {dados}")
            
            # Primeiro, testar se o backend está acessível
            try:
                test_response = requests.get("http://localhost:8080/docs", timeout=5)
                logger.info(f"Backend acessível. Status: {test_response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Backend não está acessível: {str(e)}")
                return False
            
            # Enviar dados da matrícula
            response = requests.post(url, json=dados, headers=headers, timeout=10)
            
            logger.info(f"Resposta do backend - Status: {response.status_code}")
            logger.info(f"Resposta do backend - Text: {response.text}")
            
            if response.status_code == 201:
                logger.info(f"Matrícula enviada com sucesso: {nome} - {email} - {curso}")
                return True
            elif response.status_code == 409:
                logger.warning(f"Email já cadastrado: {email}")
                return False
            else:
                logger.error(f"Erro ao enviar matrícula. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Erro de conexão ao enviar matrícula: {str(e)}")
            return False
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout ao enviar matrícula: {str(e)}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao enviar matrícula: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar matrícula: {str(e)}")
            return False
    
    async def _validar_nome(self, prompt_context: PromptValidatorContext) -> bool:
        """Validar nome (deve ter pelo menos 2 palavras)"""
        if prompt_context.recognized.succeeded:
            nome = prompt_context.recognized.value.strip()
            # Verificar se tem pelo menos 2 palavras
            palavras = nome.split()
            return len(palavras) >= 2 and all(palavra.isalpha() for palavra in palavras)
        return False
    
    async def _validar_email(self, prompt_context: PromptValidatorContext) -> bool:
        """Validar formato do email"""
        if prompt_context.recognized.succeeded:
            email = prompt_context.recognized.value.strip()
            # Regex simples para validar email
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        return False
    
    async def _validar_curso(self, prompt_context: PromptValidatorContext) -> bool:
        """Validar se o curso está na lista de cursos disponíveis"""
        if prompt_context.recognized.succeeded:
            curso = prompt_context.recognized.value.strip()
            # Buscar curso de forma case-insensitive
            for curso_disponivel in self.cursos_disponiveis:
                if curso.lower() == curso_disponivel.lower():
                    # Atualizar o valor com a capitalização correta
                    prompt_context.recognized.value = curso_disponivel
                    return True
        return False 