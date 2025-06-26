<<<<<<< HEAD
import requests
import json

def testar_api():
    """Testar se a API está funcionando"""
    try:
        # Testar se o backend está acessível
        print("🔍 Testando conectividade com o backend...")
        response = requests.get("http://localhost:8080/docs", timeout=5)
        print(f"✅ Backend acessível - Status: {response.status_code}")
        
        # Testar endpoint de matrículas
        print("\n📋 Testando endpoint de matrículas...")
        response = requests.get("http://localhost:8080/api/matriculas", timeout=5)
        print(f"✅ Endpoint funcionando - Status: {response.status_code}")
        
        # Testar criação de matrícula
        print("\n➕ Testando criação de matrícula...")
        dados_teste = {
            "nome": "Teste Bot",
            "email": "teste.bot@exemplo.com",
            "curso": "Engenharia"
        }
        
        response = requests.post(
            "http://localhost:8080/api/matriculas", 
            json=dados_teste, 
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📡 Resposta: Status {response.status_code}")
        print(f"📄 Conteúdo: {response.text}")
        
        if response.status_code == 201:
            print("✅ Matrícula criada com sucesso!")
        elif response.status_code == 409:
            print("⚠️  Email já cadastrado (comportamento esperado)")
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Backend não está rodando!")
        print("Execute: python run.py")
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")

if __name__ == "__main__":
=======
import requests
import json

def testar_api():
    """Testar se a API está funcionando"""
    try:
        # Testar se o backend está acessível
        print("🔍 Testando conectividade com o backend...")
        response = requests.get("http://localhost:8080/docs", timeout=5)
        print(f"✅ Backend acessível - Status: {response.status_code}")
        
        # Testar endpoint de matrículas
        print("\n📋 Testando endpoint de matrículas...")
        response = requests.get("http://localhost:8080/api/matriculas", timeout=5)
        print(f"✅ Endpoint funcionando - Status: {response.status_code}")
        
        # Testar criação de matrícula
        print("\n➕ Testando criação de matrícula...")
        dados_teste = {
            "nome": "Teste Bot",
            "email": "teste.bot@exemplo.com",
            "curso": "Engenharia"
        }
        
        response = requests.post(
            "http://localhost:8080/api/matriculas", 
            json=dados_teste, 
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📡 Resposta: Status {response.status_code}")
        print(f"📄 Conteúdo: {response.text}")
        
        if response.status_code == 201:
            print("✅ Matrícula criada com sucesso!")
        elif response.status_code == 409:
            print("⚠️  Email já cadastrado (comportamento esperado)")
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Backend não está rodando!")
        print("Execute: python run.py")
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")

if __name__ == "__main__":
>>>>>>> 81e477779abb3825222f0d5a29000548cc385579
    testar_api() 