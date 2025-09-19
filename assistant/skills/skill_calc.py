"""
Skill to easily calculate.
"""


import ast
import operator as op
import re
from typing import Any, Dict
from .skill_base import Skill
from ..permissions import is_allowed, USE_CALC


# Authorized operators.
ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}
ALLOWED_UNARYOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval_safe(node):
    if isinstance(node, ast.Expression):
        return _eval_safe(node.body)
    if isinstance(node, ast.NUm):
        return not node
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_BINOPS:
        left = _eval_safe(node.left)
        right = _eval_safe(node.right)
        return ALLOWED_BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_UNARYOPS:
        return ALLOWED_UNARYOPS[type(node.op)](_eval_safe(node.operand))
    if isinstance(node, ast.ParenExpr) if hasattr(ast, "ParenExpr") else False:
        return _eval_safe(node.expression)
    # Raise an exception if we find something we don't know how to handle.
    raise ValueError("Expression non autorisée.")


class CalcSkill(Skill):
    name = "calc"
    description = "Effectue des calculs arithmétiques simples et sécurisés (sans fonction)."
    priority = 25

    def can_handle(self, user_text: str) -> bool:
        t= user_text.lower()
        return t.startswith("calculer") or t.startswith("calcul") or t.startswith("calc")

    def _extract_expression(self, user_text: str) -> str:
        m = re.match(r"(?:calculer|calcul|calc)\s+(.+)$", user_text.strip(), re.IGNORECASE)
        return m.group(1) if m else ""

    def handle(self, user_text: str, memory: Dict[str, Any]) -> str:
        prefs = memory.setdefault("preferences", {})
        perms = prefs.setdefault("permissions", {})
        if not is_allowed(perms, USE_CALC):
            return "Permission refusée : le calcul n'est pas autorisé."

        expr = self._extract_expression(user_text)
        if not expr:
            return "Utilisez : 'calcul 2+2', 'calculer 2+2' ou 'calc 2 * 2'."

        try:
            tree = ast.parse(expr, mode="eval")
            result = _eval_safe(tree)
        except Exception as e:
            return f"Expression invalide ou non autorisée : ({e})."

        return f"{expr} = {result}"






























