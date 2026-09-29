import holy_bot_llm

cmd = 'execute at Stargolden run summon villager ~ ~ ~ {CustomName:\'"[IA] Mercader del Gremio"\',CustomNameVisible:1b,NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Tags:["guild_ai_merchant"]}'

print("Enviando comando manual de aparicion de aldeano...")
holy_bot_llm.api_request("/command", method="POST", payload={"command": cmd})
print("[OK] Comando de spawn ejecutado desde la consola!")
