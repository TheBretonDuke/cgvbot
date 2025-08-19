  **Proof of Concept (POC)**
- **Interface** : affichage **console** (Python)
- **Base de données** : **SQL**, explorée via **Adminer** en Docker
- **Livraison** : 8 juillet 2025
- **Plateforme** : code + doc sur **GitHub**
- Par Alan et Simon
- LICENSE MIT

---

## Fonctionnalités POC
- Chargement d’un **pré-prompt métier** dans le code.
- Appel d’un **modèle fine-tuné** sur un échantillon de **CGV** au format **JSONL**.
- **Affichage** des réponses en console.
- **Log** des prompts/réponses dans la table logs.

---

### Utilisation

# 1. Cloner le repo
git clone <https://github.com/TheBretonDuke/cgvbot>
cd cgvbot

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
