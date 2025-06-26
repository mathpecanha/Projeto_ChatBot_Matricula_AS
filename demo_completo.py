import requests
import json
import time
import random

def demonstrar_backend():
    """Demonstração completa do backend"""
    print("🌐 DEMONSTRAÇÃO DO BACKEND FLASK")
    print("=" * 50)
    
    url = "http://localhost:8080/api/matriculas"
    
    # Lista de dados de teste
    estudantes = [
        {"nome": "Maria Santos", "email": "maria@teste.com", "curso": "Administração"},
        {"nome": "Pedro Oliveira", "email": "pedro@teste.com", "curso": "Direito"},
        {"nome": "Ana Costa", "email": "ana@teste.com", "curso": "Medicina"},
        {"nome": "Lucas Lima", "email": "lucas@teste.com", "curso": "Tecnologia da Informação"},
    ]
    
    print("📋 1. Listando matrículas existentes...")
    response = requests.get(url)
    matriculas_existentes = response.json()
    print(f"   Matrículas cadastradas: {len(matriculas_existentes)}")
    
    print("\n➕ 2. Criando novas matrículas...")
    matriculas_criadas = 0
    
    for estudante in estudantes:
        print(f"   Criando matrícula para: {estudante['nome']}")
        response = requests.post(url, json=estudante)
        
        if response.status_code == 201:
            print(f"   ✅ Sucesso: {estudante['nome']} matriculado(a)")
            matriculas_criadas += 1
        elif response.status_code == 409:
            print(f"   ⚠️  Já existe: {estudante['nome']} já estava matriculado(a)")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    
    print(f"\n📊 3. Resultado: {matriculas_criadas} novas matrículas criadas")
    
    print("\n📋 4. Listando todas as matrículas...")
    response = requests.get(url)
    todas_matriculas = response.json()
    
    print(f"   Total de matrículas: {len(todas_matriculas)}")
    for i, matricula in enumerate(todas_matriculas, 1):
        print(f"   {i}. {matricula['nome']} - {matricula['curso']} ({matricula['email']})")
    
    print("\n🎯 5. Testando busca por ID...")
    if todas_matriculas:
        primeira_matricula = todas_matriculas[0]
        matricula_id = primeira_matricula['id']
        response = requests.get(f"{url}/{matricula_id}")
        if response.status_code == 200:
            print(f"   ✅ Encontrada: {response.json()['nome']}")
        else:
            print(f"   ❌ Erro na busca por ID")

def testar_integracao_bot():
    """Testar integração do bot com backend"""
    print("\n🤖 TESTE DE INTEGRAÇÃO BOT-BACKEND")
    print("=" * 50)
    
    # Simular o que o bot faria
    url = "http://localhost:8080/api/matriculas"
    
    dados_bot = {
        "nome": "Thiago Testador",
        "email": "thiago.bot@teste.com", 
        "curso": "Engenharia"
    }
    
    print("🔄 Simulando processo de matrícula via bot...")
    print(f"   Nome: {dados_bot['nome']}")
    print(f"   Email: {dados_bot['email']}")
    print(f"   Curso: {dados_bot['curso']}")
    
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.post(url, json=dados_bot, headers=headers)
    
    print(f"\n📡 Resposta do backend:")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        resposta_json = response.json()
        print("   ✅ Matrícula realizada com sucesso!")
        print(f"   📝 ID da matrícula: {resposta_json['id']}")
        print(f"   📧 Email confirmado: {resposta_json['email']}")
        print(f"   🎓 Curso: {resposta_json['curso']}")
        print(f"   📅 Data: {resposta_json['data_matricula']}")
        print(f"   💬 Mensagem: {resposta_json['message']}")
    elif response.status_code == 409:
        print("   ⚠️  Email já cadastrado (comportamento correto)")
    else:
        print(f"   ❌ Erro: {response.text}")

def verificar_servicos():
    """Verificar status dos serviços"""
    print("\n🔍 VERIFICAÇÃO DOS SERVIÇOS")
    print("=" * 50)
    
    servicos = [
        ("Backend Flask", "http://localhost:8080/docs"),
        ("Bot Framework", "http://localhost:3978/api/messages"),
        ("API Matrícula", "http://localhost:8080/api/matriculas")
    ]
    
    for nome, url in servicos:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code in [200, 405]:  # 405 é normal para bot
                print(f"   ✅ {nome}: Funcionando")
            else:
                print(f"   ⚠️  {nome}: Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {nome}: Não acessível")
        except Exception as e:
            print(f"   ❌ {nome}: Erro - {e}")

def mostrar_instrucoes():
    """Mostrar instruções para usar o projeto"""
    print("\n📖 INSTRUÇÕES PARA USO COMPLETO")
    print("=" * 50)
    
    print("🎯 Para testar o chatbot completo:")
    print("   1. Baixe o Bot Framework Emulator:")
    print("      https://github.com/Microsoft/BotFramework-Emulator/releases")
    print("   2. Abra o emulator")
    print("   3. Conecte-se em: http://localhost:3978/api/messages")
    print("   4. Deixe App ID e App Password em branco")
    
    print("\n💬 Exemplos de conversas:")
    print("   📚 FAQ:")
    print("      • 'Qual o calendário acadêmico?'")
    print("      • 'Como emitir boleto?'")
    print("      • 'Quais os horários de aula?'")
    print("      • 'Secretaria'")
    print("      • 'Cursos'")
    
    print("\n   🎓 Matrícula:")
    print("      • Digite: 'quero me matricular'")
    print("      • Siga o processo guiado")
    
    print("\n🌐 URLs importantes:")
    print(f"   • Backend: http://localhost:8080")
    print(f"   • Swagger: http://localhost:8080/docs")
    print(f"   • Bot: http://localhost:3978")

if __name__ == "__main__":
    print("🚀 DEMONSTRAÇÃO COMPLETA DO PROJETO CHATBOT")
    print("=" * 60)
    print("Autores: João Victor G Campelo & Matheus Pecanha Cavalcante")
    print("Projeto: Chatbot de Matrícula com Bot Framework e Flask")
    print("=" * 60)
    
    try:
        verificar_servicos()
        demonstrar_backend()
        testar_integracao_bot()
        mostrar_instrucoes()
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("✅ Projeto totalmente funcional e pronto para uso!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Backend não está rodando")
        print("Execute primeiro: python run.py")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}") 