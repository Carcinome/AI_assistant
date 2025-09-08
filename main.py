"""
The entry point of the AI assistant program.
"""


from assistant.core import Assistant
from assistant.skills.skill_help import HelpSkill
from assistant.skills.skill_time import TimeSkill

def build_assistant() -> Assistant:
    # Build a registry name -> description to inject in HelpSkill.
    registry = {
        TimeSkill.name: TimeSkill.description,
        "help": "Liste les commandes disponibles.",
    }

    skills = [
        HelpSkill(registry),
        TimeSkill()
    ]
    return Assistant(skills)

def run_cli() -> None:
    print("Alfred v0.1 - Votre assistant personnel, à votre service. (Tapez 'help' pour obtenir de l'aide, 'quit' pour quitter.)")
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