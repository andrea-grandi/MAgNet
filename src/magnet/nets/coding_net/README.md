# Coding Net - Ensemble Agent System

Sistema di agenti ensemble per assistenza alla programmazione con aggregazione majority voting.

## 🎯 Caratteristiche

- **100 agenti in parallelo** (configurabile)
- **Majority voting** per aggregazione risposte
- **Configurazione YAML** completamente flessibile
- **Zero modifiche al codice** per cambiare numero agenti
- **Profili predefiniti** per diversi scenari

## 🚀 Quick Start

### Installazione dipendenze

```bash
pip install pyyaml numpy langchain-openai langchain-core
```

### Uso Base

```bash
# Modalità interattiva (default: 100 agenti)
python -m magnet.nets.coding_net.app

# Single question
python -m magnet.nets.coding_net.app --question "Come ordino una lista in Python?"

# Profilo quick test (10 agenti)
python -m magnet.nets.coding_net.app --profile quick_test

# Override numero agenti
python -m magnet.nets.coding_net.app --num-agents 50

# Alta accuratezza (200 agenti)
python -m magnet.nets.coding_net.app --profile high_accuracy
```

## ⚙️ Configurazione

### File di Configurazione: `config/ensemble_config.yaml`

Il file YAML controlla TUTTO senza modificare codice:

```yaml
ensemble:
  num_agents: 100          # ← Cambia qui il numero di agenti!
  max_concurrent: 20       # Chiamate API parallele
  timeout_seconds: 30
  
aggregation:
  method: "majority_vote"
  majority_vote:
    min_consensus: 60      # % minima di consenso
    similarity_threshold: 0.85
```

### Profili Predefiniti

| Profilo | Agenti | Uso |
|---------|--------|-----|
| `quick_test` | 10 | Test rapidi |
| `development` | 50 | Sviluppo |
| `production` | 100 | Production |
| `high_accuracy` | 200 | Massima precisione |
| `high_diversity` | 100 | Massima varietà |

**Uso:**
```bash
python -m magnet.nets.coding_net.app --profile high_accuracy
```

### Override Runtime

```bash
# Cambia numero agenti senza modificare YAML
python -m magnet.nets.coding_net.app --num-agents 150

# Cambia concurrent execution
python -m magnet.nets.coding_net.app --max-concurrent 30

# Cambia consenso minimo
python -m magnet.nets.coding_net.app --min-consensus 70

# Combina tutto
python -m magnet.nets.coding_net.app \
  --num-agents 200 \
  --max-concurrent 40 \
  --min-consensus 80
```

## 📊 Come Funziona

### 1. Esecuzione Parallela
```
User Question
      ↓
┌─────────────────────────────────┐
│  Ensemble Executor              │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│  100 Agenti in Parallelo        │
│  (max 20 concurrent)            │
│  Temperatures: 0.3 → 1.0        │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│  Raccolta Risposte              │
│  (min 60 risposte valide)       │
└─────────────────────────────────┘
      ↓
   Aggregazione
```

### 2. Majority Voting

```python
# Esempio con 100 agenti:
Risposta A: 65 agenti (65%) ← WINNER
Risposta B: 25 agenti (25%)
Risposta C: 10 agenti (10%)

Consenso: 65% > 60% (threshold) ✅
```

### 3. Semantic Clustering

Le risposte simili vengono raggruppate usando similarity semantica:

```yaml
similarity_threshold: 0.85  # 85% similarità → stesso cluster
```

## 🔧 Scalabilità

### Cambiare da 100 a 500 Agenti

**Opzione 1: Modifica YAML**
```yaml
ensemble:
  num_agents: 500
  max_concurrent: 50
```

**Opzione 2: Override Runtime**
```bash
python -m magnet.nets.coding_net.app --num-agents 500 --max-concurrent 50
```

**Opzione 3: Profilo Custom**
```yaml
# config/my_profile.yaml
ensemble:
  num_agents: 500
  max_concurrent: 50
  min_successful_responses: 400
```

```bash
python -m magnet.nets.coding_net.app --config config/my_profile.yaml
```

### Performance Tips

| Agenti | Max Concurrent | Tempo Atteso | Costo API |
|--------|----------------|--------------|-----------|
| 10 | 10 | ~5s | Basso |
| 50 | 15 | ~10s | Medio |
| 100 | 20 | ~15s | Medio-Alto |
| 200 | 30 | ~20s | Alto |
| 500 | 50 | ~30s | Molto Alto |

## 📈 Output

### Formato Standard

```
================================================================================
✅ CONSENSUS REACHED: 72.5%
================================================================================

📝 FINAL ANSWER:

[Risposta aggregata dai 100 agenti]

================================================================================

📊 METADATA:
  • Agents executed: 100
  • Successful responses: 95
  • Execution time: 18.45s
  • Avg response time: 2.31s
  • Temperature range: [0.3, 1.0]
  • Aggregation method: majority_vote

📈 RESPONSE DISTRIBUTION:
  1. 69 agents (72.6%)
     Preview: To sort a list in Python, use the sorted() function...
  2. 18 agents (18.9%)
     Preview: You can sort a list using the .sort() method...
  3. 8 agents (8.4%)
     Preview: For sorting, Python provides multiple approaches...
```

## 🎛️ Configurazione Avanzata

### Early Stopping

Ferma l'esecuzione quando il consenso è raggiunto:

```yaml
performance:
  early_stopping: true
  early_stop_threshold: 0.9      # Ferma al 90% consenso
  early_stop_min_responses: 30   # Minimo 30 risposte
```

### Diversificazione

Controlla la variabilità tra agenti:

```yaml
diversification:
  vary_temperature: true
  temperature_range: [0.3, 1.0]
  temperature_distribution: "uniform"  # uniform, normal, random
  
  vary_top_p: true
  top_p_range: [0.8, 1.0]
```

### Aggregation Strategies

```yaml
aggregation:
  method: "majority_vote"  # o weighted_vote, meta_synthesis
  
  majority_vote:
    min_consensus: 60
    similarity_method: "semantic"  # exact, semantic, hybrid
    similarity_threshold: 0.85
    fallback_strategy: "meta_synthesis"
```

## 📚 Esempi

### Esempio 1: Test Rapido (10 agenti)

```bash
python -m magnet.nets.coding_net.app \
  --profile quick_test \
  --question "Qual è la differenza tra lista e tupla in Python?"
```

### Esempio 2: Production (100 agenti)

```bash
python -m magnet.nets.coding_net.app \
  --profile production
```

### Esempio 3: Esperimento Massivo (500 agenti)

```bash
python -m magnet.nets.coding_net.app \
  --num-agents 500 \
  --max-concurrent 50 \
  --min-consensus 70 \
  --question "Come implementare un binary search tree in Python?"
```

## 🔍 Debugging

### Verbose Mode

```bash
python -m magnet.nets.coding_net.app --verbose
```

### Log Individual Responses

```yaml
output:
  log_individual_responses: true
  log_file: "logs/ensemble_execution.log"
```

## 🚨 Troubleshooting

### Rate Limiting

Se ottieni errori di rate limiting:

```yaml
performance:
  respect_rate_limits: true
  requests_per_minute: 100
  
ensemble:
  max_concurrent: 10  # Riduci concurrent requests
```

### Timeout Errors

```yaml
ensemble:
  timeout_seconds: 60  # Aumenta timeout
  continue_on_error: true
```

### Low Consensus

```yaml
aggregation:
  majority_vote:
    min_consensus: 50  # Abbassa threshold
    fallback_strategy: "meta_synthesis"
```

## 📝 Note

- **API Costs**: 100 agenti = 100 chiamate API per domanda
- **Rate Limits**: Usa `max_concurrent` per controllare velocità
- **Quality vs Speed**: Più agenti = migliore qualità, ma più lento
- **Temperature**: Range più ampio = più diversità, ma meno consenso

## 🎓 Best Practices

1. **Start Small**: Usa `quick_test` profile per test
2. **Monitor Costs**: Controlla usage API
3. **Tune Consensus**: Trova il giusto balance per il tuo use case
4. **Early Stopping**: Abilita per risparmiare costi
5. **Cache Responses**: Evita domande duplicate

## 📞 Supporto

Per domande o problemi, consulta:
- `config/ensemble_config.yaml` per tutte le opzioni
- `--help` per comandi disponibili
