"""
The entry point of the AI assistant program.
"""


from assistant.core import Assistant
from assistant.skills.skill_help import HelpSkill
from assistant.skills.skill_time import TimeSkill
from assistant.skills.skill_greet import GreetSkill
from assistant.skills.skill_router import RegexIntentRouterSkill


def build_assistant() -> Assistant:
    # Instanciation of the bases skills.
    greet = GreetSkill()
    time_skill = TimeSkill()
    # Build a registry name -> description to inject in HelpSkill.
    registry = {
        greet.name: greet.description,
        TimeSkill.name: TimeSkill.description,
        "help": "Liste les commandes disponibles.",
        "router": "Route les requêtes selon l'intention (priorité maximale).",
    }
    help_skill = HelpSkill(registry)

    # Build the intent_map for the router.
    intent_map = {
        "greet": greet,
        "time": time_skill,
        "help": help_skill,
    }
    router = RegexIntentRouterSkill(intent_map=intent_map)

    # Important: Include skills and let the core list there by priority.
    skills = [
        router,
        greet,
        time_skill,
        help_skill
    ]
    return Assistant(skills=skills)

def run_cli() -> None:
    print("Alfred v0.2 - Votre assistant personnel, à votre service. (Tapez 'help' pour obtenir de l'aide, 'quit' pour quitter.)")
    assistant = build_assistant()
    while True:
        try:
            user = input("Vous > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        reply = assistant.respond(user)
        if reply == "__EXIT__":
            print("Au revoir.")
            break
        print(f"Alfred > {reply}")


if __name__ == "__main__":
    run_cli()