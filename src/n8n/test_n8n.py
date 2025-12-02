"""
Script de prueba para verificar la conexión con n8n
"""
import requests
import json

# URL del webhook
N8N_WEBHOOK_URL = "https://n8n.yamboly.lat/webhook-test/tourist-guide"

def test_poi_recommendations():
    """Prueba el endpoint de recomendaciones de POIs"""
    print("🧪 Probando recomendaciones de POIs...")
    
    payload = {
        "action_type": "get_poi_recommendations",
        "lat": 41.4036,
        "lng": 2.1744,
        "city_id": "barcelona"
    }
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta recibida:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar estructura
            if isinstance(data, dict):
                print(f"\n📊 Campos en la respuesta: {list(data.keys())}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_audio_guide():
    """Prueba el endpoint de audio-guías"""
    print("\n🧪 Probando generación de audio-guía...")
    
    payload = {
        "action_type": "audio_guide",
        "poi_id": "test-123",
        "poi_name": "Sagrada Familia",
        "poi_description": "Basílica diseñada por Antoni Gaudí",
        "user_id": "test-user",
        "language": "es",
        "voice_type": "female"
    }
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta recibida:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_booking():
    """Prueba el endpoint de reservas"""
    print("\n🧪 Probando creación de reserva...")
    
    payload = {
        "action_type": "booking",
        "user_id": "test-user-123",
        "poi_id": "test-poi-456",
        "booking_date": "2025-10-31T10:00:00Z",
        "number_of_people": 2,
        "total_price": 39.99,
        "currency": "EUR",
        "status": "pending",
        "payment_method": "stripe"
    }
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta recibida:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar que tenga payment_id
            if isinstance(data, dict) and 'payment_id' in data:
                print(f"\n✅ payment_id encontrado: {data['payment_id']}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PRUEBAS DE INTEGRACIÓN CON N8N")
    print("=" * 60)
    print(f"URL: {N8N_WEBHOOK_URL}")
    print("=" * 60)
    
    # Ejecutar pruebas
    results = []
    
    results.append(("Recomendaciones POI", test_poi_recommendations()))
    results.append(("Audio-guía", test_audio_guide()))
    results.append(("Reserva", test_booking()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    total_passed = sum(1 for _, result in results if result)
    print(f"\n✅ Pruebas exitosas: {total_passed}/{len(results)}")
    print("=" * 60)
