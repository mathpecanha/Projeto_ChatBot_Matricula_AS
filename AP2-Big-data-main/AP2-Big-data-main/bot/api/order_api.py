import requests
import json
from datetime import datetime
from config import DefaultConfig

CONFIG = DefaultConfig()

class OrderAPI:
    def consultar_pedidos(self, nome_cliente):
        try:
            url = f"{CONFIG.API_BASE_URL}/pedido/nome/{nome_cliente}"
            print(f"Consultando API: {url}")
            
            headers = {
                'User-Agent': 'IBMEC-Bot/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Pedidos encontrados: {len(result)}")
                return result
            else:
                print(f"Erro na API: {response.text}")
                return []
        except Exception as e:
            print(f"Exceção ao consultar pedidos: {e}")
            return []

    def consultar_pedidos_por_cartao(self, cartao_id):
        try:
            url = f"{CONFIG.API_BASE_URL}/pedido/cartao/{cartao_id}"
            print(f"Consultando pedidos do cartão {cartao_id} na URL: {url}")
            
            headers = {
                'User-Agent': 'IBMEC-Bot/1.0',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Status code da consulta: {response.status_code}")
            print(f"Resposta da API: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Pedidos encontrados: {len(result)}")
                return result
            else:
                print(f"Erro ao consultar pedidos do cartão: {response.text}")
                return []
        except Exception as e:
            print(f"Exceção ao consultar pedidos do cartão: {e}")
            return []

    def consultar_pedidos_por_id(self, id_pedido):
        try:
            url = f"{CONFIG.API_BASE_URL}/pedido/{id_pedido}"
            print(f"Consultando API: {url}")
            
            headers = {
                'User-Agent': 'IBMEC-Bot/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Status code consulta ID: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Pedido encontrado por ID...")
                return result
            else:
                print(f"Erro ao consultar por ID: {response.text}")
                return None
        except Exception as e:
            print(f"Exceção ao consultar pedido por ID: {e}")
            return None

    def criar_pedido(self, id_produto, id_usuario, valor_total, id_cartao):
        try:
            url = f"{CONFIG.API_BASE_URL}/pedido"
            data = {
                "id_produto": id_produto,
                "id_usuario": id_usuario,
                "valor_total": valor_total,
                "id_cartao": id_cartao,
                "data_pedido": datetime.now().strftime("%Y-%m-%d"),
                "status": "Confirmado"
            }
            
            headers = {
                'User-Agent': 'IBMEC-Bot/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            print(f"Criando pedido: {json.dumps(data, indent=2)}")
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            print(f"Status code: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 201:
                result = response.json()
                print(f"Pedido criado: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return result
            else:
                print(f"Erro ao criar pedido: {response.text}")
                # Tentar pegar detalhes do erro
                try:
                    error_detail = response.json()
                    print(f"Detalhes do erro: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
                except:
                    pass
                return None
        except Exception as e:
            print(f"Exceção ao criar pedido: {e}")
            return None

    def autorizar_transacao(self, id_usuario, numero_cartao, data_expiracao, cvv, valor):
        try:
            url = f"{CONFIG.API_BASE_URL}/cartao/authorize/usuario/{id_usuario}"
            data = {
                "numero": numero_cartao,
                "cvv": cvv,
                "dt_expiracao": data_expiracao,
                "valor": valor
            }
            
            headers = {
                'User-Agent': 'IBMEC-Bot/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            print(f"Autorizando transação: {json.dumps(data, indent=2)}")
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Transação autorizada: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return result
            else:
                error_msg = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                print(f"Erro ao autorizar transação: {error_msg}")
                return {"status": "NOT_AUTHORIZED", "message": error_msg}
        except Exception as e:
            print(f"Exceção ao autorizar transação: {e}")
            return {"status": "ERROR", "message": str(e)}