"""
Script di test per il customer swarm.
Questo script testa l'interazione tra orchestrator, flight_assistant e hotel_assistant.
"""

from magnet.nets.customer_net.agent.swarm import app


def test_flight_search():
    """Test per la ricerca di voli."""
    print("\n" + "="*60)
    print("TEST 1: Ricerca voli")
    print("="*60)
    
    messages = [
        {
            "role": "user",
            "content": "Vorrei cercare voli da Milano a Roma per il 15 novembre 2025"
        }
    ]
    
    result = app.invoke(
        {"messages": messages}, 
        {"recursion_limit": 50}
    )
    
    print("\n--- Risposta ---")
    if "messages" in result:
        for msg in result["messages"]:
            if hasattr(msg, "content"):
                print(f"{msg.type}: {msg.content}")
    
    return result


def test_hotel_search():
    """Test per la ricerca di hotel."""
    print("\n" + "="*60)
    print("TEST 2: Ricerca hotel")
    print("="*60)
    
    messages = [
        {
            "role": "user",
            "content": "Sto cercando un hotel a Roma per 2 notti dal 15 novembre"
        }
    ]
    
    result = app.invoke({"messages": messages})
    
    print("\n--- Risposta ---")
    if "messages" in result:
        for msg in result["messages"]:
            if hasattr(msg, "content"):
                print(f"{msg.type}: {msg.content}")
    
    return result


def test_combined_request():
    """Test per una richiesta combinata (volo + hotel)."""
    print("\n" + "="*60)
    print("TEST 3: Richiesta combinata (volo + hotel)")
    print("="*60)
    
    messages = [
        {
            "role": "user",
            "content": "Devo andare a Roma dal 15 al 17 novembre. Mi serve un volo da Milano e un hotel per 2 notti."
        }
    ]
    
    result = app.invoke({"messages": messages})
    
    print("\n--- Risposta ---")
    if "messages" in result:
        for msg in result["messages"]:
            if hasattr(msg, "content"):
                print(f"{msg.type}: {msg.content}")
    
    return result


def test_conversation():
    """Test per una conversazione multi-turno."""
    print("\n" + "="*60)
    print("TEST 4: Conversazione multi-turno")
    print("="*60)
    
    # Primo messaggio
    messages = [
        {
            "role": "user",
            "content": "Ciao, vorrei organizzare un viaggio"
        }
    ]
    
    result = app.invoke({"messages": messages})
    
    print("\n--- Turno 1 ---")
    if "messages" in result:
        last_msg = result["messages"][-1]
        if hasattr(last_msg, "content"):
            print(f"Assistant: {last_msg.content}")
    
    # Secondo messaggio
    result["messages"].append({
        "role": "user",
        "content": "Voglio andare a Barcellona"
    })
    
    result = app.invoke({"messages": result["messages"]})
    
    print("\n--- Turno 2 ---")
    if "messages" in result:
        last_msg = result["messages"][-1]
        if hasattr(last_msg, "content"):
            print(f"Assistant: {last_msg.content}")
    
    return result


def interactive_test():
    """Test interattivo con l'utente."""
    print("\n" + "="*60)
    print("TEST INTERATTIVO")
    print("="*60)
    print("Digita 'exit' o 'quit' per uscire")
    print("-"*60)
    
    messages = []
    
    while True:
        user_input = input("\nTu: ").strip()
        
        if user_input.lower() in ["exit", "quit", "esci"]:
            print("Arrivederci!")
            break
        
        if not user_input:
            continue
        
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            result = app.invoke({"messages": messages})
            
            if "messages" in result:
                messages = result["messages"]
                last_msg = messages[-1]
                if hasattr(last_msg, "content"):
                    print(f"\nAssistant: {last_msg.content}")
        except Exception as e:
            print(f"\nErrore: {e}")


if __name__ == "__main__":
    import sys
    
    print("\n🚀 TEST CUSTOMER SWARM")
    print("="*60)
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        if test_name == "flight":
            test_flight_search()
        elif test_name == "hotel":
            test_hotel_search()
        elif test_name == "combined":
            test_combined_request()
        elif test_name == "conversation":
            test_conversation()
        elif test_name == "interactive":
            interactive_test()
        else:
            print(f"Test '{test_name}' non riconosciuto.")
            print("\nTest disponibili:")
            print("  - flight: test ricerca voli")
            print("  - hotel: test ricerca hotel")
            print("  - combined: test richiesta combinata")
            print("  - conversation: test conversazione multi-turno")
            print("  - interactive: modalità interattiva")
    else:
        # Esegui tutti i test automatici
        try:
            test_flight_search()
        except Exception as e:
            print(f"Errore nel test voli: {e}")
        
        try:
            test_hotel_search()
        except Exception as e:
            print(f"Errore nel test hotel: {e}")
        
        try:
            test_combined_request()
        except Exception as e:
            print(f"Errore nel test combinato: {e}")
        
        try:
            test_conversation()
        except Exception as e:
            print(f"Errore nel test conversazione: {e}")
        
        print("\n" + "="*60)
        print("✅ Test completati!")
        print("="*60)
        print("\nPer eseguire un test specifico:")
        print("  python test_swarm.py [flight|hotel|combined|conversation|interactive]")
