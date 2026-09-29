import holy_files
import holy_bot_llm

config_content = """# =========================================================
# Configuración del Plugin GuildAIEconomy
# =========================================================

# Configuración de Inteligencia Artificial (Google Gemini)
gemini:
  api_key: "AQ.Ab8RN6Lq7W8I32mB9eLuc5GSeWYbpIxAl6nRbk5GVebnWPQPfg"
  model: "gemini-1.5-flash"
  system_prompt: "Eres Gilderbot, un comerciante astuto y cómico que administra la tienda del Gremio en Minecraft. Tu objetivo es mantener una economía próspera, evitar la inflación y aconsejar a los jugadores. Responde siempre de forma breve (máximo 2 oraciones) y apta para el chat de Minecraft."

# Configuración del Aldeano NPC Chatbot
merchant:
  name: "§b🤖 [IA] Mercader del Gremio"
  profession: "LIBRARIAN"

# Configuración del Motor Económico Dinámico (Anti-inflación)
economy:
  base_prices:
    DIAMOND: 100.0
    GOLD_INGOT: 25.0
    IRON_INGOT: 10.0
    EMERALD: 50.0
    NETHERITE_INGOT: 500.0
    OAK_LOG: 2.0
    NETHER_STAR: 2000.0

  alpha_sensitivity: 0.15
  min_price_factor: 0.70
  max_price_factor: 1.50
  guild_tax_percent: 5.0
"""

print("[1/2] Actualizando /plugins/GuildAIEconomy/config.yml con la API Key...")
holy_files.write_file("/plugins/GuildAIEconomy/config.yml", config_content)

print("[2/2] Ejecutando /guildai reload en la consola de Minecraft...")
holy_bot_llm.send_command("guildai reload")

print("\n✅ ¡API Key conectada y configuración recargada en vivo sin reiniciar el servidor!")
