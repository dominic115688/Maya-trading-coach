def get_ai_coach_response(message, language="English"):
    if language == "Spanish":
        return f"Entendido sobre '{message}'. Como tu coach de trading, te sugiero revisar siempre tu relación riesgo-beneficio antes de abrir una posición."
    else:
        return f"I received your query about '{message}'. As your trading coach, I suggest always reviewing your risk-to-reward ratio and sticking to your trading plan before entering any position."
