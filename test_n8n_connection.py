"""
Script de prueba para verificar la conexión con n8n
"""
import requests
import json
from datetime import datetime

# Configuración
N8N_WEBHOOK_URL = "https://n8n.yamboly.lat/webhook/tourist-guide"

def test_connection():
    """Prueba la conexión básica con n8n"""
    print("🔍 Probando conexión con n8n...")
    print(f"URL: {N8N_WEBHOOK_URL}\n")
    
    # Datos de prueba
    payload = {
        "action_type": "get_poi_recommendations",
        "lat": 41.4036,
        "lng": 2.1744,
        "city_id": "test-city-id",
        "user_id": "test-user",
        "timestamp": datetime.now().isoformat(),
        "max_distance": 10,
        "min_rating": 3.5,
        "max_results": 10
    }
    
    print("📤 Enviando petición...")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Respuesta recibida!")
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"Content-Length: {len(response.content)} bytes\n")
        
        # Intentar parsear como JSON
        try:
            result = response.json()
            print("✅ Respuesta JSON válida:")
            print(json.dumps(result, indent=2))
            
            # Verificar estructura
            if 'recommendations' in result:
                print(f"\n✅ Encontradas {len(result['recommendations'])} recomendaciones")
            elif 'pois' in result:
                print(f"\n✅ Encontrados {len(result['pois'])} POIs")
            else:
                print("\n⚠️ Estructura de respuesta inesperada")
                print(f"Claves disponibles: {list(result.keys())}")
                
        except ValueError as e:
            print(f"❌ Error al parsear JSON: {str(e)}")
            print(f"Contenido de la respuesta (primeros 500 caracteres):")
            print(response.text[:500])
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión: {str(e)}")
        print("\n💡 Posibles causas:")
        print("1. El servidor n8n no está activo")
        print("2. Problema de DNS con el dominio")
        print("3. Firewall bloqueando la conexión")
        print("4. Problema de red local")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout: El servidor tardó demasiado en responder")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP {e.response.status_code}")
        print(f"Respuesta: {e.response.text[:500]}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")


def test_dns():
    """Prueba la resolución DNS del dominio"""
    print("\n" + "="*50)
    print("🔍 Probando resolución DNS...")
    print("="*50 + "\n")
    
    import socket
    
    domain = "n8n.yamboly.lat"
    
    try:
        ip = socket.gethostbyname(domain)
        print(f"✅ DNS resuelto correctamente")
        print(f"Dominio: {domain}")
        print(f"IP: {ip}")
    except socket.gaierror as e:
        print(f"❌ Error al resolver DNS: {str(e)}")
        print(f"\n💡 El dominio '{domain}' no puede ser resuelto")
        print("Verifica:")
        print("1. Que el dominio esté correctamente configurado")
        print("2. Tu conexión a internet")
        print("3. La configuración DNS de tu sistema")


def test_ping():
    """Prueba la conectividad básica"""
    print("\n" + "="*50)
    print("🔍 Probando conectividad (ping)...")
    print("="*50 + "\n")
    
    import platform
    import subprocess
    
    domain = "n8n.yamboly.lat"
    
    # Comando ping según el sistema operativo
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', domain]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ Ping exitoso a {domain}")
            print(result.stdout)
        else:
            print(f"❌ Ping falló")
            print(result.stdout)
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout al hacer ping a {domain}")
    except Exception as e:
        print(f"❌ Error al hacer ping: {str(e)}")


if __name__ == "__main__":
    print("="*50)
    print("🧪 Test de Conexión con n8n")
    print("="*50 + "\n")
    
    # Ejecutar pruebas
    test_dns()
    test_ping()
    test_connection()
    
    print("\n" + "="*50)
    print("✅ Pruebas completadas")
    print("="*50)
