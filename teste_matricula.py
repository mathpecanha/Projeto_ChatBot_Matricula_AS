import requests
import json

def testar_matricula():
    """Testar o endpoint de matrícula"""
    url = "http://localhost:8080/api/matriculas"
    
    # Dados de teste
    dados = {
        "nome": "João Silva",
        "email": "joao@teste.com",
        "curso": "Engenharia"
    }
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    print("🔧 Testando endpoint de matrícula...")
    print(f"URL: {url}")
    print(f"Dados: {dados}")
    
    try:
        # Teste GET (listar matrículas)
        print("\n📋 Testando GET /api/matriculas")
        response_get = requests.get(url)
        print(f"Status: {response_get.status_code}")
        print(f"Resposta: {response_get.text}")
        
        # Teste POST (criar matrícula)
        print("\n➕ Testando POST /api/matriculas")
        response_post = requests.post(url, json=dados, headers=headers)
        print(f"Status: {response_post.status_code}")
        print(f"Resposta: {response_post.text}")
        
        if response_post.status_code == 201:
            print("✅ Matrícula criada com sucesso!")
        else:
            print("❌ Erro ao criar matrícula")
            
        # Teste GET novamente (verificar se foi criada)
        print("\n📋 Verificando matrículas após criação")
        response_get2 = requests.get(url)
        print(f"Status: {response_get2.status_code}")
        print(f"Resposta: {response_get2.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("Verifique se o backend está rodando em http://localhost:8080")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def testar_bot():
    """Testar se o bot está respondendo"""
    url = "http://localhost:3978/api/messages"
    
    print("\n🤖 Testando se o bot está rodando...")
    print(f"URL: {url}")
    
    try:
        # Tentar fazer uma requisição simples
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 405:  # Method Not Allowed é esperado para GET
            print("✅ Bot está rodando (405 Method Not Allowed é normal)")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Bot não está rodando ou não acessível")
        print("Execute: python bot/app.py")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🧪 TESTE DO PROJETO CHATBOT")
    print("=" * 40)
    
    testar_matricula()
    testar_bot()
    
    print("\n" + "=" * 40)
    print("✅ Testes concluídos!")
    print("\n📝 Para testar o bot completamente:")
    print("1. Baixe o Bot Framework Emulator")
    print("2. Conecte em: http://localhost:3978/api/messages")
    print("3. Digite: 'quero me matricular'") 