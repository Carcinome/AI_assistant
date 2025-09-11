"""
From testing the skill 'caps'.
"""


from assistant.skills.skill_caps import CapsSkill


def test_caps_can_handle():
    s = CapsSkill()
    assert s.can_handle("caps bonjour")
    assert s.can_handle("crie la batcave")
    assert not s.can_handle("bonjour")

def test_caps_handle_basic():
    s = CapsSkill()
    memory = {}
    assert s.handle("caps hello", memory) == "HELLO"
    assert s.handle("crie gotham", memory) == "GOTHAM"