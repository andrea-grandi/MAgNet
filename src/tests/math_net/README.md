# Cooperative Swarm of 10 Agents

Questo progetto implementa uno swarm cooperativo di 10 agenti identici che collaborano scambiandosi risposte e insights.

## Struttura

- `config.yaml` - Configurazione dello swarm (modello, agenti, tools, handoffs)
- `main.py` - Script principale per testare lo swarm
- `requirements.txt` - Dipendenze Python
- `.env` - Variabili d'ambiente (da creare)

## Setup

1. **Installa le dipendenze:**

```bash
pip install -r requirements.txt
```

2. **Configura le variabili d'ambiente:**
   Crea un file `.env` nella directory corrente:

```bash
cp .env.example .env
```

Modifica `.env` e inserisci la tua API key di OpenAI:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Esecuzione

Esegui lo script principale:

```bash
python main.py
```

## Funzionalità

Lo script esegue le seguenti operazioni:

1. **Carica la configurazione** da `config.yaml`
2. **Crea 10 agenti cooperativi** identici
3. **Genera il grafo dello swarm** salvandolo in `swarm.png`
4. **Testa lo swarm** con una domanda di esempio
5. **Avvia la modalità interattiva** per conversare con lo swarm

### Visualizzazione del Grafo

Il grafo dello swarm viene automaticamente salvato come `swarm.png` e mostra:

- Tutti i 10 agenti
- Le connessioni di handoff tra gli agenti
- Il flusso di comunicazione

### Modalità Interattiva

Dopo il test iniziale, lo script entra in modalità interattiva dove puoi:

- Fare domande agli agenti
- Vedere come cooperano scambiandosi informazioni
- Osservare i passaggi di handoff tra agenti

Digita `exit`, `quit` o `q` per uscire.

## Configurazione dello Swarm

### Agenti

- **10 agenti identici** (`agent_1` - `agent_10`)
- Ogni agente può fare handoff a qualsiasi altro agente
- Tutti condividono lo stesso modello e temperature

### Tools

- `share_response` - Permette agli agenti di processare e migliorare le risposte degli altri

### Handoffs

Ogni agente può trasferire il controllo a qualsiasi altro agente per ottenere diverse prospettive e costruire risposte collaborative.

## Personalizzazione

Puoi modificare `config.yaml` per:

- Cambiare il modello LLM
- Modificare la temperatura
- Personalizzare i prompt degli agenti
- Aggiungere nuovi tools
- Modificare le regole di handoff
