# 🚀 CODING_NET ENSEMBLE SYSTEM

## ✅ Sistema Completo Creato!

Hai ora un sistema completo di ensemble agents con le seguenti caratteristiche:

### 📁 Struttura Creata

```
coding_net/
├── config/
│   ├── __init__.py
│   ├── loader.py                      # Config loader
│   ├── ensemble_config.yaml           # ★ CONFIGURAZIONE PRINCIPALE
│   └── example_custom_config.yaml     # Template per custom configs
├── agent/
│   ├── __init__.py
│   ├── configs.py                     # Agent names
│   ├── llms.py                        # LLM models
│   ├── prompts.py                     # System prompts
│   └── ensemble.py                    # ★ ENGINE PRINCIPALE
├── app/
│   ├── __init__.py
│   └── __main__.py                    # ★ APPLICAZIONE
├── README.md                          # Documentazione completa
├── requirements.txt                   # Dipendenze
├── Dockerfile                         # Per deployment
├── test.py                           # Test suite
├── show_config.py                    # Mostra configurazioni
├── quickstart.sh                     # Script setup rapido
└── .gitignore
```

### 🎯 Come Cambiare il Numero di Agenti (ZERO Modifiche Codice)

#### Metodo 1: Modifica YAML
```yaml
# Apri: config/ensemble_config.yaml
ensemble:
  num_agents: 500  # ← Cambia qui!
```

#### Metodo 2: Override Runtime
```bash
python -m magnet.nets.coding_net.app --num-agents 500
```

#### Metodo 3: Usa Profili
```bash
python -m magnet.nets.coding_net.app --profile high_accuracy  # 200 agenti
```

#### Metodo 4: Config Custom
```bash
python -m magnet.nets.coding_net.app --config my_config.yaml
```

### 🏃 Quick Start

```bash
# 1. Vai nella directory
cd src/magnet/nets/coding_net

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Test veloce (5 agenti)
python test.py

# 4. Mostra configurazioni disponibili
python show_config.py

# 5. Avvia modalità interattiva (100 agenti)
python -m magnet.nets.coding_net.app

# 6. Test rapido (10 agenti)
python -m magnet.nets.coding_net.app --profile quick_test
```

### 📊 Esempi Pratici

#### Esempio 1: Da 100 a 10 agenti (testing rapido)
```bash
python -m magnet.nets.coding_net.app --num-agents 10 --max-concurrent 10
```

#### Esempio 2: Da 100 a 500 agenti (massima accuratezza)
```bash
python -m magnet.nets.coding_net.app --num-agents 500 --max-concurrent 50
```

#### Esempio 3: Single question con 200 agenti
```bash
python -m magnet.nets.coding_net.app \
  --num-agents 200 \
  --question "Explain Python decorators with examples"
```

#### Esempio 4: Cambia strategia (mantenendo 100 agenti)
```yaml
# In ensemble_config.yaml
aggregation:
  method: "majority_vote"
  majority_vote:
    min_consensus: 80  # Più rigido
    similarity_threshold: 0.9  # Più preciso
```

### ⚙️ Profili Predefiniti

| Profilo | Agenti | Descrizione |
|---------|--------|-------------|
| `quick_test` | 10 | Testing rapido |
| `development` | 50 | Sviluppo |
| `production` | 100 | Production standard |
| `high_accuracy` | 200 | Massima accuratezza |
| `high_diversity` | 100 | Massima varietà risposte |

**Uso:**
```bash
python -m magnet.nets.coding_net.app --profile [nome_profilo]
```

### 🎛️ Parametri Configurabili (Senza Modificare Codice)

Tutti configurabili in `config/ensemble_config.yaml`:

- ✅ **num_agents**: 1 a 1000+ agenti
- ✅ **max_concurrent**: Controllo parallelismo
- ✅ **temperature_range**: Diversificazione risposte
- ✅ **min_consensus**: Soglia consenso (%)
- ✅ **similarity_threshold**: Clustering risposte
- ✅ **timeout_seconds**: Timeout per agente
- ✅ **early_stopping**: Stop anticipato
- ✅ **aggregation method**: majority_vote, weighted_vote, etc.

### 📈 Scalabilità

```bash
# 10 agenti (testing)
python -m magnet.nets.coding_net.app --num-agents 10

# 50 agenti (dev)
python -m magnet.nets.coding_net.app --num-agents 50

# 100 agenti (production)
python -m magnet.nets.coding_net.app --num-agents 100

# 200 agenti (high accuracy)
python -m magnet.nets.coding_net.app --num-agents 200

# 500 agenti (massivo)
python -m magnet.nets.coding_net.app --num-agents 500

# 1000 agenti (estremo)
python -m magnet.nets.coding_net.app --num-agents 1000 --max-concurrent 100
```

### 🔍 Come Funziona l'Aggregazione

1. **Esecuzione Parallela**: N agenti lavorano simultaneamente
2. **Clustering Semantico**: Risposte simili vengono raggruppate
3. **Majority Voting**: Il cluster più grande vince
4. **Consenso Check**: Verifica soglia minima consenso
5. **Output**: Risposta finale + metadata

### 💡 Best Practices

1. **Start Small**: Inizia con `--profile quick_test` (10 agenti)
2. **Monitor Costs**: Ogni agente = 1 chiamata API
3. **Tune Consensus**: Trova il giusto balance per il tuo caso
4. **Use Early Stopping**: Risparmia costi quando consenso raggiunto
5. **Scale Gradually**: 10 → 50 → 100 → 200 → 500

### 📝 Note Importanti

- **API Costs**: 100 agenti = 100 chiamate OpenAI per domanda
- **Rate Limits**: Usa `max_concurrent` per evitare rate limiting
- **Quality vs Speed**: Più agenti = migliore qualità, ma più lento
- **Consenso**: 60% è un buon default, aumenta per più certezza

### 🐛 Debugging

```bash
# Verbose output
python -m magnet.nets.coding_net.app --verbose

# Vedi tutte le configurazioni
python show_config.py

# Test il sistema
python test.py
```

### 🎉 Pronto all'Uso!

Il sistema è completamente funzionante. Cambia il numero di agenti semplicemente:

1. Modificando `config/ensemble_config.yaml`, OPPURE
2. Usando `--num-agents N`, OPPURE
3. Usando un profilo con `--profile [nome]`

**ZERO modifiche al codice necessarie!**

---

Per maggiori dettagli, vedi `README.md`
