"""
The entry point of the AI assistant program.
"""


from assistant.core import Assistant
from assistant.skills.skill_help import HelpSkill
from assistant.skills.skill_time import TimeSkill
from assistant.skills.skill_greet import GreetSkill
from assistant.skills.skill_router import RegexIntentRouterSkill
from assistant.skills.skill_caps import CapsSkill
from assistant.skills.skill_todo import TodoSkill
from assistant.skills.skill_calc import CalcSkill
from assistant.skills.skill_files import FileSkill
from assistant.skills.skill_timer import TimerSkill



def build_assistant() -> Assistant:
    # Instanciation of the base skills.
    greet_skill = GreetSkill()
    time_skill = TimeSkill()
    caps_skill = CapsSkill()
    todo_skill = TodoSkill()
    calc_skill = CalcSkill()
    file_skill = FileSkill()
    timer_skill = TimerSkill()

    # Build a registry name -> description to inject in HelpSkill.
    registry = {
        greet_skill.name: greet_skill.description,
        time_skill.name: time_skill.description,
        caps_skill.name: caps_skill.description,
        todo_skill.name: todo_skill.description,
        calc_skill.name: calc_skill.description,
        file_skill.name: file_skill.description,
        timer_skill.name: timer_skill.description,
        "help": "Liste les commandes disponibles.",
        "router": "Route les requêtes selon l'intention (priorité maximale).",
    }
    help_skill = HelpSkill(registry)

    # Build the intent_map for the router.
    intent_map = {
        "greet": greet_skill,
        "time": time_skill,
        "caps": caps_skill,
        "todo": todo_skill,
        "calc": calc_skill,
        "file": file_skill,
        "timer": timer_skill,
        "help": help_skill,
    }
    router = RegexIntentRouterSkill(intent_map=intent_map)

    # Important: Include skills and let the core list there by priority.
    skills = [
        router,
        greet_skill,
        time_skill,
        caps_skill,
        todo_skill,
        calc_skill,
        file_skill,
        timer_skill,
        help_skill
    ]
    return Assistant(skills=skills)

def run_cli() -> None:
    print("Alfred v0.3 - Votre assistant personnel, à votre service. (Tapez 'help' pour obtenir de l'aide, 'quit' pour quitter.)")
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