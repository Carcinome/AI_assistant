# AI Assistant project named "Alfred":
## A reference to the famous majordomo of Bruce Wayne.

---

- To devs, think of configuring your virtual environment on your machine before starting to code. Indeed, "the env.work"
folder is not included in the repo.
    - the requirements.txt file is included in the repo and contains all the dependencies.

---

- To devs on JetBrains IDEs, the .idea folder is not included in the repo.
- To devs on VS Code, the .vscode folder is not included in the repo.

---

### **French programmers :**

#### Comment ajouter une skill rapidement :

##### Etape 1 :

Créer le fichier de la skill, à placer dans `assistant/skills`.\
*Par exemple, `assistant/skills/skill_caps.py`.*

Ensuite, prendre le skill suivant comme exemple :

```# assistant/skills/skill_caps.py
from typing import Any, Dict
from .skill_base import Skill

class CapsSkill(Skill):
    name = "caps"
    description = "Transforme un texte en MAJUSCULES."
    priority = 30  # après greet/time/help/router

    def can_handle(self, user_text: str) -> bool:
        text = user_text.strip().lower()
        # Déclencheurs simples (tu en ajouteras autant que tu veux)
        return text.startswith("caps ") or text.startswith("crie ")

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        # Retirer le mot-clé, puis upper()
        text = user_text.strip()
        if text.lower().startswith("caps "):
            payload = text[5:]
        elif text.lower().startswith("crie "):
            payload = text[5:]
        else:
            payload = text
        return payload.upper() if payload else "Que veux-tu mettre en majuscules ?"
```

Explications :
- name/description : identifiants humains & docs.
- priority : ordre d’exécution (plus petit = plus prioritaire). Ici 30, après les trucs “socle”.
- can_handle : dit “oui, je peux” si le message commence par caps ou crie .
- handle : récupère la partie après le mot-clé et renvoie .upper().

##### Etape 2 :

Ajouter les motifs au router (optionnel, mais recommandé tout de même, plus "ingé").\
Les skills seront ainsi détectées par le **RegexIntentRouterSkill**.

Dans `assistant/skills/skill_router.py`, préciser dans `self._patterns` 
à la suite du pattern de base pour créer des modules et non juste un bloc :

```
self._patterns += [
    # Intention CAPS : "caps <texte>" ou "crie <texte>"
    (re.compile(r"^\s*caps\s+(?P<payload>.+)$", re.IGNORECASE), "caps"),
    (re.compile(r"^\s*crie\s+(?P<payload>.+)$", re.IGNORECASE), "caps"),
]
```

Explications :
- On crée un label d'intent `"caps`.
- On capture le texte avec `(?P<payload>.+)` pour le passer à la skill via `memory["_router_entities"]`.

#### Etape 3 :

Déclarer la skill, l'enregistrer dans l'aide et relier l'intent `"caps"` à l'instance.

Dans `main.py` :

```
from assistant.skills.skill_caps import CapsSkill
# ...
def build_assistant() -> Assistant:
    greet = GreetSkill()
    time_skill = TimeSkill()
    caps = CapsSkill()  # <- new

    registry = {
        greet.name: greet.description,
        time_skill.name: time_skill.description,
        caps.name: caps.description,  # <- new
        "help": "Liste les commandes disponibles.",
        "router": "Route les requêtes selon l'intention (priorité maximale).",
    }
    help_skill = HelpSkill(registry)

    intent_map = {
        "greet": greet,
        "time": time_skill,
        "help": help_skill,
        "caps": caps,  # <- new
    }
    router = RegexIntentRouterSkill(intent_map=intent_map)

    skills = [router, greet, time_skill, caps, help_skill]  # <- caps incluse
    return Assistant(skills=skills)
```

Explications :
- `registry` permet de liste la skill dans `help`.
- `intent_map` pour que le router sache vers quelle instance envoyer `"caps"`.
- `skills` permet d'inclure l'instance pour que le cœur puisse l'appeler.

#### Etape 4 :

Lire les *entities* du router dans la skill (bien qu'optionnel, permet que si le router a extrait `payload`, 
la skill en question peut le récupérer proprement).

Dans `CapsSkill.handle` on lit l'entity avant d'extraire "à la main" :

```
entities = memory.get("_router_entities") or {}
payload = entities.get("payload")
if not payload:
    # fallback si appel direct sans router
    text = user_text.strip()
    if text.lower().startswith("caps "):
        payload = text[5:]
    elif text.lower().startswith("crie "):
        payload = text[5:]
    else:
        payload = text
return payload.upper() if payload else "Que veux-tu mettre en majuscules ?"
```

Explications :
- C'est un bon réflexe de préférer les entities du router. Cette méthode est plus fiable. 

#### Etape 5 :

Tester en CLI.\
Penser à **tester son code**, rapidement, pour voir si le squelette principal fonctionne et que l'intégrité est maintenue.

Pense-bête :

> `help` doit montrer la nouvelle skill.\
> Les deux triggers doivent fonctionner.

#### Etape 6 :

Ajouter un test minimal est un bon réflexe ingé IA. On automatise donc un test simple.\
On crée un dossier `test/` à la racine du projet, dans lequel on vient créer `test_caps.py` :

```
# tests/test_caps.py
from assistant.skills.skill_caps import CapsSkill

def test_caps_can_handle():
    s = CapsSkill()
    assert s.can_handle("caps bonjour")
    assert s.can_handle("crie la batcave")
    assert not s.can_handle("bonjour")  # ne doit pas déclencher

def test_caps_handle_basic():
    s = CapsSkill()
    memory = {}
    assert s.handle("caps hello", memory) == "HELLO"
    assert s.handle("crie gotham", memory) == "GOTHAM"
```

Explications :
- Deux tests ici : la détection et le comportement.
- On garde ça simple et rapide.

#### Etape 7 :

**DOCUMENTER SON TRAVAIL.**
