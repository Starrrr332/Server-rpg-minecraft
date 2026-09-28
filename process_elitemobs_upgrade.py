# -*- coding: utf-8 -*-
"""
Script de optimización y traducción integral para EliteMobs y el Gremio de Aventureros.
Trabaja exclusivamente en gremio_aventureros_lab/ para pruebas locales.
"""

import os
import yaml
import re

LAB_DIR = 'gremio_aventureros_lab'

# ==========================================
# 1. TRADUCCIÓN DE ROLES DE NPCs
# ==========================================
ROLE_TRANSLATIONS = {
    'Blacksmith': 'Herrero del Gremio',
    'Special Blacksmith': 'Herrero Especial del Gremio',
    'Enchanter': 'Encantador Arcano',
    'Repairman': 'Maestro Armero',
    'Scrapper': 'Desguazador de Reliquias',
    'Unbinder': 'Desvinculador de Almas',
    'Scroll Applier': 'Grabador de Pergaminos',
    'Fletcher': 'Flechero del Gremio',
    'Barkeep': 'Tabernero del Gremio',
    'Quest Giver': 'Emisor de Misiones',
    'Story Mode Quests': 'Misiones de Historia',
    'Arena Master': 'Maestro del Coliseo',
    'Guild Attendant': 'Recepcionista del Gremio',
    'Guide': 'Guía de Aventureros',
    'Transporter': 'Transportador Místico',
    'Travelling Merchant': 'Comerciante Errante',
    'Combat Instructor': 'Instructor de Combate',
    'Adventurer Instructor': 'Instructor de Aventureros',
    'Berserker Instructor': 'Instructor Berserker',
    'Cleric Instructor': 'Instructor Clérigo',
    'Paladin Instructor': 'Instructor Paladín',
    'Ranger Instructor': 'Instructor Montaraz',
    'Spellcaster Instructor': 'Instructor Hechicero',
    'Blackjack Dealer': 'Crupier de Blackjack',
    'Card Shark': 'Tahúr de Cartas',
    'Coin Flipper': 'Lanzador de Monedas',
    'Gambling Den Owner': 'Dueño de la Taberna de Apuestas',
    'Slot Machine': 'Tragaperras Arcana',
    'Fireworks': 'Pirotécnico del Gremio',
    'Santa!': '¡Santa Claus!',
    'Invasion': 'Portal de Invasión',
    'Dark Spire': 'Aguja Oscura',
    'Binder of Worlds Teleport': 'Teletransporte: Vinculador de Mundos',
    'Dark Cathedral': 'Catedral Sombría',
    'Pirate Ship': 'Navío Corsario',
    "Craftenmine's Lab": 'Laboratorio de Craftenmine',
    'The Mines': 'Las Minas Abandonadas',
    'Sewers': 'Las Cloacas Antiguas',
    'Yggdrasil': 'Árbol Sagrado Yggdrasil',
    'Vampire Manor': 'Mansión Vampírica',
    'Catacombs': 'Las Catacumbas',
    'The Climb': 'La Gran Escalada',
    'Airship': 'Aeronave Imperial',
    'The Nether Bell': 'La Campana del Nether',
    "Beast's Sanctuary": 'Santuario de las Bestias',
    'The City': 'La Ciudadela Perdida',
    'Under Grove': 'Bosque Umbrío',
    'The Bridge': 'El Gran Puente',
    'The Cave': 'La Caverna Prohibida',
    'The Quarry': 'La Cantera Olvidada',
    "Knight's Castle": 'Castillo de los Caballeros',
    'Frost Palace': 'Palacio Escarchado',
    'North Pole': 'Polo Norte',
    'The Deep Mines': 'Minas Abisales',
    'Goblin Kingdom': 'Reino Goblin',
    'Hallosseum': 'El Halliseo',
    'The Nether Wastes': 'Páramos del Nether',
    'The Ruins': 'Ruinas Ancestrales',
    'Hallowed Haunt': 'Guarida Consagrada',
    'Colosseum': 'El Coliseo de Élite',
    'The Palace': 'El Palacio Real',
    'Bone Monastery': 'Monasterio de Huesos',
    'Steamworks': 'Fábrica de Vapor'
}

# ==========================================
# 2. TRADUCCIÓN DE FRASES / DIÁLOGOS DE NPCs
# ==========================================
PHRASE_TRANSLATIONS = {
    # Saludos generales
    "Welcome to our shop!": "¡Bienvenido a mi tienda, noble aventurero!",
    "Sell your goods here!": "¡Aquí compro tus botines por las mejores monedas!",
    "Fresh goods, just for you!": "¡Mercancía selecta, recién forjada!",
    "Got something to sell?": "¿Tienes tesoros o armas para tasar?",
    "Want to buy something good?": "¿Buscas equipamiento de élite para tu aventura?",
    "Fresh goods every time!": "¡Siempre la mejor calidad garantizada!",
    "Need a drink?": "¿Sediento de gloria y una buena bebida fría?",
    "Want a drink": "¿Te apetece una copa para calentar el espíritu?",
    "Greetings, traveler.": "Saludos, viajero de tierras lejanas.",
    "Looking for a challenge?": "¿Estás buscando un verdadero desafío de combate?",
    "Step right up!": "¡Acércate sin miedo, aventurero!",
    "Welcome to the Adventurer's Guild!": "¡Bienvenido a la sede del Gremio de Aventureros!",
    "Ready for your next mission?": "¿Listo para emprender tu próxima misión?",
    "Talk to me when you're ready.": "Habla conmigo cuando tengas todo listo.",
    "The arena awaits you!": "¡La arena de combate aguarda a los valientes!",

    # Diálogos educativos y consejos
    "Higher level mobs drop\\nhigher value items!": "¡Los monstruos de mayor nivel\\nsueltan objetos de mucho más valor!",
    "Items with lots of \\nenchantments are worth more!": "¡Las armas y armaduras con más\\nencantamientos valen muchas más monedas!",
    "Higher level mobs drop\\nbetter items!": "¡Cuanto más fuerte sea el jefe,\\nmejores serán las armas que obtengas!",
    "Higher level mobs have\\na higher chance of dropping loot!": "¡Las criaturas de mayor nivel tienen\\nmayor probabilidad de soltar botín épico!",
    "Elite mobs are attracted to\\ngood armor, the better the\\narmor the higher their\nlevel!": "¡Los monstruos de élite se sienten atraídos\\npor buen equipamiento! ¡Entre mejor armadura\\nlleves, más alto será su nivel!",
    "Some items have special\\npotion effects!": "¡Ciertas armas y armaduras poseen\\nefectos de poción continuos especiales!",
    "Some items have unique\\neffects!": "¡Los objetos legendarios esconden\\nhabilidades pasivas únicas!",
    "The hunter enchantment\\nattracts elite mobs to your\\nlocation!": "¡El encantamiento Cazador atrae\\nmonstruos de élite hacia tu posición!",
    "Special weapons and armor\\ndropped by elite mobs can\\nbe sold here!": "¡Las armas y armaduras de élite que\\nconsigas puedes venderlas aquí por oro!",
    "Higher guild ranks will\\nincrease the quality of the\\nloot from elite mobs!": "¡Alcanzar rangos más altos en el Gremio\\nmejora la calidad del botín que obtienes!",
    "Have one of our house specialties.": "Prueba una de nuestras especialidades de la casa.",
    "Special drinks won't find them\\nanywhere else.": "Bebidas exclusivas que no hallarás\\nen ninguna otra taberna del reino."
}

def translate_role(raw_role):
    if not raw_role:
        return raw_role
    for en, es in ROLE_TRANSLATIONS.items():
        if en in raw_role:
            return raw_role.replace(en, es)
    return raw_role

def translate_text(text):
    if not isinstance(text, str):
        return text
    # Direct match
    if text in PHRASE_TRANSLATIONS:
        return PHRASE_TRANSLATIONS[text]
    # Partial replacements for common patterns
    res = text
    for en, es in PHRASE_TRANSLATIONS.items():
        if en in res:
            res = res.replace(en, es)
    return res

def process_npcs():
    npc_dir = os.path.join(LAB_DIR, 'npcs')
    count = 0
    for fn in os.listdir(npc_dir):
        if not fn.endswith('.yml'):
            continue
        fp = os.path.join(npc_dir, fn)
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            data = yaml.safe_load(f) or {}

        modified = False

        # Translate role
        if 'role' in data and data['role']:
            old_role = data['role']
            new_role = translate_role(old_role)
            if old_role != new_role:
                data['role'] = new_role
                modified = True

        # Translate greetings
        if 'greetings' in data and isinstance(data['greetings'], list):
            new_greetings = []
            for g in data['greetings']:
                t = translate_text(g)
                new_greetings.append(t)
            data['greetings'] = new_greetings
            modified = True

        # Translate dialog
        if 'dialog' in data and isinstance(data['dialog'], list):
            new_dialog = []
            for d in data['dialog']:
                t = translate_text(d)
                new_dialog.append(t)
            data['dialog'] = new_dialog
            modified = True

        if modified:
            with open(fp, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            count += 1

    print(f"[OK] {count} NPCs traducidos y actualizados en el laboratorio.")

# ==========================================
# 3. TRADUCCIÓN DE MENÚS (menus/)
# ==========================================
def process_menus():
    menu_dir = os.path.join(LAB_DIR, 'menus')
    
    # 1. buy_or_sell_menu.yml
    p = os.path.join(menu_dir, 'buy_or_sell_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['shopName'] = '&6&l[Gremio] &eComprar o Vender'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 2. repair_menu.yml
    p = os.path.join(menu_dir, 'repair_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['shopName'] = '&6&l[Gremio] &eTaller de Reparación'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 3. scrapper_menu.yml
    p = os.path.join(menu_dir, 'scrapper_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['shopName'] = '&6&l[Gremio] &eDesguazador de Reliquias'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 4. unbind_menu.yml
    p = os.path.join(menu_dir, 'unbind_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['shopName'] = '&6&l[Gremio] &eDesvincular Objeto de Alma'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 5. custom_shop_menu.yml
    p = os.path.join(menu_dir, 'custom_shop_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['shopName'] = '&6&l[Gremio] &eBazar Especializado'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 6. arrow_shop_menu.yml
    p = os.path.join(menu_dir, 'arrow_shop_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['shopName'] = '&2&lArmería del Flechero - Flechas Especiales'
        d['insufficientFundsMessage'] = '&c[Gremio] &7¡No tienes suficientes Monedas de Élite! Requieres &f%price% &7monedas.'
        d['purchaseSuccessMessage'] = '&a[Gremio] &7¡Has comprado &f%amount%x %item% &7por &f%price% &7Monedas de Élite!'
        d['inventoryFullMessage'] = '&c[Gremio] &7¡Tu inventario está completamente lleno!'
        d['arrowDisplayName'] = '&fFlechas Estándar'
        d['spectralArrowDisplayName'] = '&eFlechas Espectrales'
        d['arrowOfPoisonDisplayName'] = '&2Flecha de Veneno'
        d['arrowOfSlownessDisplayName'] = '&8Flecha de Lentitud'
        d['arrowOfWeaknessDisplayName'] = '&7Flecha de Debilidad'
        d['arrowOfHarmingDisplayName'] = '&4Flecha de Daño Inmediato'
        d['arrowOfHealingDisplayName'] = '&dFlecha de Curación'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 7. arena_menu.yml
    p = os.path.join(menu_dir, 'arena_menu.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['invalidArenaMessage'] = '&4[Gremio] &c¡La arena seleccionada no está disponible o no existe!'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 8. player_status_screen.yml
    p = os.path.join(menu_dir, 'player_status_screen.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['landingOverviewLines'] = [
            '<g:#B8860B:#F0C040>Monedas</g>: &f$money &8• <g:#A63D2F:#E97932>Nivel de Combate</g>: &f$combatLevel',
            '<g:#2E7D4F:#69C56F>Misiones Activas</g>: &f$activeQuests &8• <g:#355CA8:#5FA9E8>Puntaje</g>: &f$score'
        ]
        d['indexTexts1'] = '&5&l/ag &7- &6Sede del Gremio'
        d['indexHovers1'] = 'HAZ CLIC PARA VIAJAR\n¡El punto de reunión para aceptar\nmisiones, comerciar con NPCs,\nmejorar tu equipo y progresar!'
        d['indexTexts4'] = '&6&lÍndice General'
        d['indexTexts6'] = '&bp. $statsPage &8- <g:#B8860B:#F0C040>★ Registro de Aventura</g>'
        d['indexHovers6'] = '¡Haz clic para ver tus hazañas!'
        d['indexTexts7'] = '&bp. $gearPage &8- <g:#A63D2F:#E97932>⚔ Equipo de Combate</g>'
        d['indexHovers7'] = '¡Haz clic para ver tu armadura y armas!'
        d['indexTexts8'] = '&bp. $teleportsPage &8- <g:#355CA8:#5FA9E8>↔ Teletransportes</g>'
        d['indexHovers8'] = '¡Haz clic para viajar a mazmorras!'
        d['indexTexts9'] = '&bp. $commandsPage &8- <g:#267A78:#58B8A9>⚡ Acciones Rápidas</g>'
        d['indexHovers9'] = 'Comandos y utilidades del Gremio'
        d['indexTexts10'] = '&bp. $questsPage &8- <g:#2E7D4F:#69C56F>✉ Misiones</g>'
        d['indexHovers10'] = '¡Haz clic para ver tus misiones activas!'
        d['indexTexts11'] = '&bp. $bossTrackingPage &8- <g:#7A1F2B:#C2414A>☠ Rastreador de Jefes</g>'
        d['indexHovers11'] = '¡Haz clic para rastrear jefes vivos!'
        d['indexTexts12'] = '&bp. $skillsPage &8- <g:#6D3AA8:#A855F7>⚗ Habilidades</g>'
        d['indexHovers12'] = '¡Haz clic para ver tus habilidades!'
        d['indexTexts13'] = '<g:#A04468:#E07A9A>♥ Grupo / Party</g>'
        d['indexHovers13'] = 'Crea, invita o abandona un grupo de mazmorra'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    print("[OK] Menús de interfaz traducidos al español.")

# ==========================================
# 4. TRADUCCIÓN DE CONFIGURACIONES BASE
# ==========================================
def process_configs():
    # 1. AdventurersGuild.yml
    p = os.path.join(LAB_DIR, 'configs', 'AdventurersGuild.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['adventurersGuildMenuName'] = '&6&lGremio de Aventureros'
        d['gearRestrictionMessage'] = '&c[Gremio] ¡Necesitas nivel $itemLevel de $skillType para equipar esto! (Tu nivel: $skillLevel)'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 2. Quests.yml
    p = os.path.join(LAB_DIR, 'configs', 'Quests.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['questJoinMessage'] = '&a¡Has aceptado la misión &e$questName&a!'
        d['questLeaveMessage'] = '&cHas abandonado la misión &e$questName&c.'
        d['questCompleteMessage'] = '&2¡Completaste con éxito la misión &a$questName&2!'
        d['leaveWhenNoActiveQuestsExist'] = '&c¡No tienes ninguna misión activa en este momento!'
        d['questStartTitle'] = '&a¡Misión Aceptada!'
        d['questCompleteTitle'] = '&2¡Misión Completada!'
        d['questLeaveTitle'] = '&c¡Misión Abandonada!'
        d['killQuestChatProgressionMessage'] = '&8[Gremio] &7➤ Eliminar &f$name&7: $color$current&7/$color$target'
        d['fetchQuestChatProgressionMessage'] = '&8[Gremio] &7➤ Obtener &f$name&7: $color$current&7/$color$target'
        d['dialogQuestChatProgressionMessage'] = '&8[Gremio] &7➤ Hablar con &f$name&7: $color$current&7/$color$target'
        d['questCapMessage'] = '&8[Gremio] &c¡Has alcanzado el límite máximo de misiones activas (10)! &4Abandona o completa al menos una para aceptar más.'
        d['killQuestScoreboardProgressionMessage'] = '&7➤ Eliminar &f$name&7: $color$current&7/$color$target'
        d['fetchQuestScoreboardProgressionMessage'] = '&7➤ Conseguir &f$name&7: $color$current&7/$color$target'
        d['dialogQuestScoreboardProgressionMessage'] = '&7➤ Hablar con &f$name&7: $color$current&7/$color$target'
        d['arenaQuestScoreboardProgressionMessage'] = '&7➤ Superar arena &f$arenaName'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 3. EconomySettings.yml
    p = os.path.join(LAB_DIR, 'configs', 'EconomySettings.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['currencyName'] = 'Monedas de Élite'
        d['chatCurrencyShowerMessage'] = '&7[Gremio] ¡Has recogido &a$amount $currency_name&7!'
        d['actionbarCurrencyShowerMessage'] = '&7[Gremio] +&a$amount $currency_name'
        d['adventurersGuildNotificationMessages'] = '&7[Gremio] ¿Monedas para gastar? ¡Usa &a/ag&7 para ir a la sede!'
        d['walletCommandMessage'] = 'Tienes &2$balance $currency_name'
        d['shopBuyMessage'] = '&a¡Has comprado $item_name &apor $item_value $currency_name!'
        d['shopCurrentBalanceMessage'] = '&aTu saldo actual: $currency_amount $currency_name.'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 4. MobCombatSettings.yml (Traducción + Optimización)
    p = os.path.join(LAB_DIR, 'configs', 'MobCombatSettings.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        # Traducciones
        d['bossLocationMessage'] = '&7[Gremio] &a[¡Haz clic para rastrear!]'
        d['bossKillParticipationMessage'] = '&eTu daño infligido al jefe: &a$playerDamage'
        d['defaultOtherWorldBossLocationMessage'] = '&c$name: ¡En otra dimensión!'
        d['weakText'] = '&9&l¡Debilidad!'
        d['resistText'] = '&c&l¡Resistencia!'
        # Optimizaciones de rendimiento de combate
        d['hideEliteMobPowersUntilAggro'] = True       # Ahorra CPU mientras los mobs no están en combate
        d['doSpawnerEliteMobVisualEffects'] = False     # Evita lag de partículas en granjas
        d['doNaturalEliteMobVisualEffects'] = True
        d['regenerateCustomBossHealthOnCombatEnd'] = True
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 5. config.yml (Traducción + Optimización)
    p = os.path.join(LAB_DIR, 'configs', 'config.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['trackMessage'] = 'Rastrear a $name'
        d['chestCooldownMessage'] = '&7[Gremio] &c¡Ya abriste este cofre del tesoro recientemente! Espera $time.'
        d['treasureChestNoDropMessage'] = '&8[Gremio] &c¡El cofre estaba vacío! ¡Más suerte en tu próxima expedición!'
        d['bossAlreadyGoneMessage'] = '&c[Gremio] ¡Este jefe ya ha sido derrotado o desapareció!'
        # Optimizaciones
        d['notificationThrottleSeconds'] = 10
        d['defaultTransitiveBlockLimiter'] = 400
        d['onlyUseBedrockMenus'] = True
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # 6. dungeons.yml
    p = os.path.join(LAB_DIR, 'configs', 'dungeons.yml')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['joinDungeonAsPlayerText'] = '&aEntrar a $dungeonName como jugador'
        d['joinDungeonAsSpectatorText'] = '&7Entrar a $dungeonName como espectador'
        with open(p, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    print("[OK] Configuraciones base de EliteMobs traducidas y optimizadas.")

# ==========================================
# 5. TRADUCCIÓN DE MISIONES (customquests/)
# ==========================================
def process_quests():
    q_dir = os.path.join(LAB_DIR, 'customquests')
    
    # ag_welcome_quest_0.yml
    p0 = os.path.join(q_dir, 'ag_welcome_quest_0.yml')
    if os.path.exists(p0):
        with open(p0, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['name'] = '&2¡Encontrando el Gremio de Aventureros!'
        d['questLore'] = [
            '¡Descubre la sede central del Gremio de Aventureros usando el comando &2/ag &0o &2/adventurersguild&f!'
        ]
        d['questAcceptDialog'] = [
            '&8[Dux]&f ¡Excelente! Utiliza &2/ag &fo &2/adventurersguild&f para viajar a la sede del Gremio de Aventureros.',
            '¡Asegúrate de hablar con Casus cuando llegues allí!'
        ]
        if 'customObjectives' in d and 'Objective1' in d['customObjectives']:
            d['customObjectives']['Objective1']['dialog'] = [
                '&8[&aCasus&8]&f ¡Bienvenido a la Sede del Gremio de Aventureros, el centro de reunión para todo héroe!',
                '&8[&aCasus&8]&f Aquí podrás aceptar contratos, comerciar botines y prepararte para desafiar a los jefes más temibles del mundo.'
            ]
        with open(p0, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # ag_welcome_quest_1.yml
    p1 = os.path.join(q_dir, 'ag_welcome_quest_1.yml')
    if os.path.exists(p1):
        with open(p1, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['name'] = '&2¡Bienvenido al Gremio de Aventureros!'
        d['questLore'] = [
            '¡Conoce a los diferentes maestros del Gremio y descubre todas las instalaciones disponibles!'
        ]
        with open(p1, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    # ag_adventurer_training.yml
    p2 = os.path.join(q_dir, 'ag_adventurer_training.yml')
    if os.path.exists(p2):
        with open(p2, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['name'] = '&2Tu Primera Clase de Combate'
        d['questLore'] = [
            'Habla con los instructores del Gremio y elige tu primera clase RPG para desbloquear habilidades marciales.'
        ]
        with open(p2, 'w', encoding='utf-8') as f:
            yaml.dump(d, f, allow_unicode=True, sort_keys=False)

    print("[OK] Misiones del Gremio traducidas al español.")

def main():
    print("=== INICIANDO PROCESAMIENTO EN LABORATORIO LOCAL ===")
    process_npcs()
    process_menus()
    process_configs()
    process_quests()
    print("=== PROCESO COMPLETADO SATISFACTORIAMENTE ===")

if __name__ == '__main__':
    main()
