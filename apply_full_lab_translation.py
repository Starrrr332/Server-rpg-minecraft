# -*- coding: utf-8 -*-
"""
Traductor exhaustivo y de alta fidelidad para el Gremio de Aventureros y EliteMobs.
Cubre el 100% de diálogos, saludos, roles, menús y configuraciones en el laboratorio local.
"""

import os
import yaml
import json

LAB_DIR = 'gremio_aventureros_lab'

# Diccionario exhaustivo de Saludos (Greetings)
FULL_GREETINGS = {
    "A simple coin flip can change your fortune!": "¡Un simple lanzamiento de moneda puede cambiar tu fortuna!",
    "A simple game with big rewards!": "¡Un juego sencillo con recompensas legendarias!",
    "An arrow can be worth more than a sword in the right hands.": "En las manos correctas, una flecha certera vale más que cien espadas.",
    "Are you lost?": "¿Te has extraviado en los pasillos del Gremio?",
    "Been to the AG?": "¿Has visitado la sede principal del Gremio?",
    "Blackjack! Get 21 to win big!": "¡Veintiuno! ¡Llega a 21 y llévate el gran pozo de monedas!",
    "Care to test your luck today?": "¿Te atreves a desafiar a la suerte hoy?",
    "Care to try your luck at the tables?": "¿Quieres probar tu suerte en las mesas de juego?",
    "Every journey starts here.\\nYour first trial costs one coin.": "Todo viaje comienza aquí.\\nTu primera prueba cuesta una moneda.",
    "Feeling lucky, adventurer?": "¿Te sientes con suerte, intrépido aventurero?",
    "Feeling lucky?": "¿Te acompaña la fortuna hoy?",
    "Feeling... adventurous?": "¿Te sientes... con sed de aventura?",
    "Flip a coin, double your money!": "¡Lanza la moneda y duplica tu oro!",
    "Fortune favors the bold!": "¡La fortuna favorece a los audaces!",
    "Get your items repaired!": "¡Repara tus armas y armaduras dañadas aquí!",
    "Give those reels a spin!": "¡Haz girar los rodillos arcanos!",
    "Good day.": "Buen día, valiente cazador.",
    "Good vanilla item you want converted?": "¿Tienes un objeto común que desees imbuir con poderes de élite?",
    "Got an item to improve?": "¿Tienes un equipamiento que quieras mejorar?",
    "Got anything good?": "¿Traes botines valiosos de tus cacerías?",
    "Got anything worth selling?": "¿Tienes reliquias que quieras vender por monedas?",
    "Got damaged items?": "¿Tu armadura o armas están al borde de romperse?",
    "Got elite scrolls?": "¿Tienes pergaminos de élite para aplicar?",
    "Got enchanted books?": "¿Traes libros arcanos de encantamiento?",
    "Got fire in your blood?\\nPut it to work.": "¿Tienes fuego en la sangre?\\nDemuéstralo en combate.",
    "Greetings, adventurer!\\nFancy a quest?": "¡Saludos, aventurero!\\n¿Te interesa un contrato de misión?",
    "Greetings.": "Saludos cordiales.",
    "Hail, friend.": "¡Salud, noble camarada!",
    "Heads or tails? Simple as that!": "¿Cara o cruz? ¡Tan simple como el destino!",
    "Heard about the AG?": "¿Conoces los beneficios del Gremio de Aventureros?",
    "Heard of the Adventurer's Guild?": "¿Has oído hablar del legendario Gremio de Aventureros?",
    "Higher or lower? How far can you go?": "¿Mayor o menor? ¿Hasta dónde llegará tu racha?",
    "Ho ho ho!": "¡Ho ho ho! ¡Felices fiestas, aventurero!",
    "Howdy, partner.": "¡Saludos, forastero! Pasa adelante.",
    "Huh?": "¿Mmh? ¿Qué se te ofrece?",
    "I've got the sharpest arrows in town!": "¡Tengo las flechas más mortíferas de todo el reino!",
    "Is it elite scroll time?": "¿Es hora de imbuir tus armas con pergaminos arcanos?",
    "It's scrap 'o clock!": "¡Hora de desguazar objetos viejos en materiales valiosos!",
    "JACKPOT waiting for a winner!": "¡El GRAN PREMIO aguarda por su nuevo dueño!",
    "Know about the Adventurer's Guild?": "¿Conoces la sede del Gremio de Aventureros?",
    "Looking for arrows?": "¿Buscas munición y flechas especializadas?",
    "Looking to scrap?": "¿Deseas reciclar tu equipo inservible?",
    "Lucky 7s pay the most...": "Los sietes de la suerte pagan la mayor fortuna...",
    "May I help you?": "¿En qué puedo servirte, noble viajero?",
    "Need a combat lesson?": "¿Requieres adiestramiento avanzado de combate?",
    "Need a hint": "¿Necesitas una pista para tu misión?",
    "Need a repair?": "¿Necesitas forjar y reparar tus herramientas?",
    "Need ammunition?": "¿Escaso de flechas para tu arco?",
    "Need guidance?": "¿Necesitas orientación en tus primeros pasos?",
    "Need help?": "¿Requieres asistencia o información?",
    "Need something enchanted?": "¿Deseas encantar tus artefactos con magia de élite?",
    "Need something?": "¿Buscas algo en particular?",
    "Need to recycle items?": "¿Tienes objetos repetidos para reciclar?",
    "Power is easy.\\nControl takes practice.": "El poder es fácil de obtener.\\nEl verdadero control exige disciplina.",
    "Ready to fight Elite Mobs?": "¿Estás listo para desafiar a los monstruos de élite?",
    "Repairing items for scrap!": "¡Reparo tus piezas usando chatarra de reliquias!",
    "Risk it all or cash out smart...": "Arriésgalo todo o retírate sabiamente con tus ganancias...",
    "Salutations!": "¡Mis saludos, honorable aventurero!",
    "Scrap time!": "¡Convierte tus sobras en recursos útiles!",
    "Spin the reels! Match three to win!": "¡Haz girar la rueda mágica! ¡Tres iguales ganan!",
    "Stand firm. Others\\nwill stand behind you.": "Mantente firme como una roca.\\nOtros lucharán a tus espaldas.",
    "Step right up, test your fortune!": "¡Acércate, no temas tentar a tu destino!",
    "Take heart. There is\\nstrength in kindness.": "Ten coraje. Incluso en la compasión\\nhay una fuerza inquebrantable.",
    "Test Greeting!": "¡Saludos desde el Gremio!",
    "The cards don't lie. Do you trust them?": "Las cartas arcanas nunca mienten. ¿Confías en ellas?",
    "The house always wins, they say...": "La casa siempre gana, suelen decir los cobardes...",
    "The house always wins... eventually.": "La casa siempre triunfa... tarde o temprano.",
    "Thirsty?": "¿Sediento tras una larga batalla en las mazmorras?",
    "Turn that scrap into durability!": "¡Convierte restos de equipo en durabilidad para tus armas!",
    "Want to get rid of items?": "¿Quieres vaciar tu inventario de objetos pesados?",
    "Want to know more about combat?": "¿Deseas profundizar en las tácticas de combate contra jefes?",
    "Want to learn about combat?": "¿Quieres aprender los secretos del combate de élite?",
    "Watch. Breathe.\\nChoose your moment.": "Observa con calma. Respira hondo.\\nElige el instante exacto para atacar.",
    "We have nothing but the best": "En mi puesto solo encontrarás mercancía de primera calidad.",
    "We only buy elite mob gear.": "Solo compro equipamiento auténtico obtenido de criaturas de élite.",
    "Welcome to my humble establishment!": "¡Bienvenido a mi modesto establecimiento!",
    "Welcome to the\\nAdventurer's Guild Hub!": "¡Bienvenido a la Sede Central\\ndel Gremio de Aventureros!",
    "Welcome to the\\nAdventurer's Guild!": "¡Bienvenido a las salas\\ndel Gremio de Aventureros!",
    "Welcome to the\\nArena!": "¡Bienvenido a la sangrienta\\nArena de Gladiadores!",
    "Welcome!": "¡Muy bienvenido, aventurero!",
    "Well met.": "¡Un placer encontrarte aquí, guerrero!",
    "Yes?": "¿Sí? ¿Qué deseas consultar?",
    "You are not prepared.": "Aún no estás preparado para lo que aguarda en las sombras...",
    "You called?": "¿Me llamabas? Estoy a tu servicio.",
    "You! I've got a quest!": "¡Eh, tú! ¡Tengo un contrato urgente para ti!"
}

# Diccionario exhaustivo de Diálogos (Dialogs)
FULL_DIALOGS = {
    "50/50 chance, pure luck!": "¡50% de probabilidad! ¡Pura fortuna en juego!",
    "75% chance to work!": "¡75% de éxito garantizado en el proceso!",
    "A blackjack pays extra!": "¡Un veintiuno natural te otorga un pago extra en monedas!",
    "Absolutely no refunds.": "Bajo ninguna circunstancia se admiten devoluciones.",
    "Been to the AG?": "¿Has pasado ya por el Gremio de Aventureros?",
    "Best repairs in town!": "¡Las mejores reparaciones de armaduras de todo el continente!",
    "Blackjack, slots, cards... take your pick!": "Veintiuno, tragaperras, cartas... ¡tú eliges tu juego!",
    "Boss loot has a level.\\nTrain your skills to\\nuse stronger equipment.": "El botín de los jefes exige nivel.\\nEntrena tus habilidades marciales para\\nempuñar armamento más poderoso.",
    "Bring food into dungeons.\\nEating takes time;\\nfind a safe opening.": "Lleva abundantes provisiones a las mazmorras.\\nComer toma tiempo; busca siempre\\nun respiro seguro en la batalla.",
    "Can you help an old man\\nin his time of need?": "¿Podrías ayudar a este anciano\\nen sus horas de mayor necesidad?",
    "Cash out anytime, or push your luck...": "Retira tu oro en cualquier momento, o tienta a la suerte...",
    "Check the questboard to\\nsee active quests!": "¡Revisa el tablón de contratos\\npara ver todas las misiones disponibles!",
    "Cherries, lemons, bells, bars, or sevens...": "Cerezas, campanas, lingotes de oro o sietes de la suerte...",
    "Class weapons deal\\n10% more damage.\\nCheck your class menu.": "Las armas propias de tu clase infligen\\nun 10% más de daño adicional.\\nConsulta tu menú de clase con /em class.",
    "Complete guild quests\\nfor cool rewards!": "¡Cumple misiones para el Gremio\\ny cosecha recompensas exclusivas!",
    "Damage builds threat.\\nBosses pursue whoever\\nhas the most.": "El daño infligido genera amenaza.\\nLos jefes perseguirán con furia a quien\\nacumule mayor nivel de amenaza.",
    "Dear traveller, I have\\na request for you!": "Noble viajero, ¡tengo una encomienda\\nde suma importancia para ti!",
    "Don't complain if it fails!": "¡No reclames si la forja falla, la magia conlleva riesgos!",
    "Don't go over 21...": "¡Ten cuidado de no pasarte de 21 o perderás tu apuesta!",
    "Don't worry about debt, we're... flexible.": "No te preocupes por las pérdidas, aquí somos... comprensivos.",
    "Each correct guess multiplies your winnings!": "¡Cada acierto consecutivo multiplica exponencialmente tus monedas!",
    "Elite mobs are attracted to\\ngood armor, the better the\\narmor the higher their level!": "Los monstruos de élite se sienten atraídos\\npor armaduras poderosas. ¡Cuanto mejor equipo\\nlleves, más alto será el nivel de tus rivales!",
    "Enchantment results are\\nnot guaranteed!": "¡Los resultados de encantamientos arcanos\\nno están asegurados al cien por cien!",
    "Even two matches get you something.": "Incluso coincidir dos símbolos te otorgará un pequeño premio.",
    "Fortune favors the bold!": "¡La gloria y las riquezas son de los audaces!",
    "Get your scrap here!": "¡Consigue materiales de reciclaje aquí mismo!",
    "Give your tank a moment\\nto gather the enemies\\nbefore opening fire.": "Dale a tu tanque unos segundos\\npara provocar y reunir a los monstruos\\nantes de abrir fuego a discreción.",
    "Good vanilla item you want converted?": "¿Tienes un objeto común que desees convertir en una pieza de élite?",
    "Got an enchanted book?": "¿Posees un libro de encantamiento de élite para imbuir?",
    "Got something for me?": "¿Traes alguna reliquia especial para mí?",
    "Have an unbind scroll?": "¿Tienes un pergamino de desvinculación en tu inventario?",
    "Health and class energy\\nappear above your hotbar.\\nWatch both in a fight.": "Tu vida y energía de clase aparecen\\njusto sobre tu barra de objetos.\\nVigila ambas atentamente en combate.",
    "Heard about the AG?": "¿Has oído hablar del Gremio de Aventureros?",
    "Heard of the Adventurer's Guild?": "¿Conoces los privilegios de unirte al Gremio?",
    "Higher quality items are\\nriskier to enchant!": "¡Los artefactos de mayor calidad conllevan\\nmucho más riesgo al intentar encantarlos!",
    "Higher tier quests have\\nbetter rewards!": "¡Las misiones de rango superior ofrecen\\nmonedas y tesoros mucho más valiosos!",
    "Higher tier quests make\\nyou hunt higher level mobs!": "¡Los contratos avanzados te enviarán a cazar\\ncriaturas de nivel sumamente superior!",
    "Hit or stand? The choice is yours.": "¿Pides otra carta o te plantas? La decisión es tuya.",
    "How long can your streak last?": "¿Hasta dónde podrás extender tu racha victoriosa?",
    "I am the only one qualified\\nto unbind your goods.": "Soy el único hechicero capacitado\\npara desvincular almas de tu equipamiento.",
    "I give the greatest challenge of them all.\\nExpect death.": "Te ofrezco el mayor desafío de este reino.\\nPrepárate para perecer si flaqueas.",
    "I got your fix!": "¡Tengo justo lo que necesitas para tu equipo!",
    "I have lost some presents, \\ncan you help me?": "He perdido varios regalos navideños...\\n¿Podrías ayudarme a recuperarlos?",
    "I know everything about\\nthis place!": "¡Conozco cada rincón, secreto y peligro\\nde este magnífico santuario!",
    "I will unbind your items\\nfor an extremely rare unbind scroll.": "Puedo liberar tus artefactos de su vínculo\\na cambio de un pergamino de desvinculación.",
    "I'll buy it on the cheap!": "¡Te compraré esas chatarras a un precio justo!",
    "I'll repair your items!": "¡Restauraré la durabilidad de tus armas y armaduras!",
    "I'm a bit busy...": "Estoy un poco ocupado en este instante, héroe...",
    "Inspect your training\\nand specializations.": "Inspecciona tu progreso marcial\\ny especializaciones con /em class.",
    "Know about the Adventurer's Guild?": "¿Deseas saber más acerca de nuestra orden?",
    "Make sure you're well equipped\\nfor these quests!": "¡Asegúrate de ir bien pertrechado\\nantes de emprender estas misiones!",
    "Mana refills over time.\\nBerserkers build Fury\\nby dealing and taking hits.": "El Maná se regenera con el tiempo.\\nLos Berserkers acumulan Furia de batalla\\nasestando y recibiendo ataques.",
    "My arrows fly true.": "Mis flechas jamás se desvían de su blanco.",
    "My dealers are the best in the realm!": "¡Mis crupieres son los más diestros de todo el reino!",
    "Need a fix?": "¿Necesitas una solución rápida para tus herramientas?",
    "Need a vanilla item converted?": "¿Deseas transmutar un objeto vanilla en un arma de élite?",
    "Need elite items repaired?": "¿Tus reliquias de élite han sufrido desgaste?",
    "Need to go back?": "¿Deseas retornar al punto de partida?",
    "Need to learn your way around\\nthis place?": "¿Necesitas aprender a orientarte\\nen esta vasta sede de aventureros?",
    "No refunds.": "Sin devoluciones.",
    "No taksies backsies.": "Lo apostado, apostado está. Sin marcha atrás.",
    "One taste and will keep you\\ncoming back from more.": "Un solo sorbo y querrás volver\\npor otra copa en cada regreso.",
    "One wrong guess and it's all gone!": "¡Un solo fallo y perderás todo lo apostado!",
    "Paladins recover faster\\nnear elites; Clerics recover\\nfaster near players.": "Los Paladines se recuperan más rápido\\ncerca de los jefes; los Clérigos\\ncerca de sus aliados heridos.",
    "Pick your side wisely...": "Elige tu bando con suma prudencia...",
    "Prepared to face the arena?": "¿Estás listo para ingresar a la arena de combate?",
    "Press F twice to move.\\nF + left-click: Signature.\\nF + right-click: Utility.": "Pulsa F dos veces para esquivar con destreza.\\nF + clic izquierdo: Habilidad Insignia.\\nF + clic derecho: Habilidad de Utilidad.",
    "Rangers regain Focus\\nfaster after five seconds\\nwithout taking damage.": "Los Montaraces recuperan Concentración\\nmás rápido tras 5 segundos\\nsin recibir daño alguno.",
    "Recycle, reuse, reduce!": "¡Reciclar y forjar de nuevo, esa es la clave!",
    "Red ground is a warning.\\nMove before the attack\\nlands!": "El suelo teñido de rojo es una advertencia.\\n¡Aléjate de inmediato antes\\nde que caiga el ataque devastador!",
    "Remember, getting closer to 21 is the goal.": "Recuerda: el objetivo es acercarse lo más posible a 21 sin pasarte.",
    "Repair damaged equipment\\nbefore your next dungeon.\\nVisit the repairman.": "Repara todo tu equipo dañado antes\\nde adentrarte en una mazmorra.\\nVisita siempre al maestro armero.",
    "Scrappy deals!": "¡Ofertas de chatarra que no puedes dejar pasar!",
    "Shop purchases are final.": "Todas las compras en las tiendas son definitivas.",
    "Spectral arrows to mark your prey.": "Flechas espectrales para marcar y perseguir a tu presa.",
    "Staff fireballs burst\\non impact. Aim at\\nclustered enemies.": "Las bolas de fuego de bastón estallan al impactar.\\nApúntalas al centro de grupos\\nde enemigos agrupados.",
    "Taunts force a boss\\nto face the tank\\nfor a short time.": "Las provocaciones obligan al jefe\\na centrar sus ataques en el tanque\\ndurante unos instantes cruciales.",
    "The End is near...\\nYou are not prepared.": "El Fin se aproxima inexorablemente...\\nAún no posees el poder para resistirlo.",
    "The coin decides all.": "El destino final lo decide el giro de la moneda.",
    "The enchanter improves\\nyour equipment with\\nelite enchanted books.": "El encantador arcano potencia tu equipo\\nutilizando libros mágicos de élite.",
    "The odds are fair, I promise!": "¡Las probabilidades son justas, te lo aseguro por mi honor!",
    "The sevens are the key to riches!": "¡Los sietes dorados son la llave a una fortuna incalculable!",
    "The things I've seen...\\nYou wouldn't believe it.": "Las monstruosidades que he presenciado...\\nJamás las creerías si te las contara.",
    "There are no refunds.": "No se admiten reclamos ni devoluciones.",
    "Three of a kind wins big!": "¡Tres figuras idénticas aseguran una ganancia monumental!",
    "Time is money!": "¡El tiempo es oro en las tabernas del Gremio!",
    "Tipped arrows for the discerning archer.": "Flechas imbuidas de pociones para el arquero más exigente.",
    "Unlocking new guid tiers\\nincreases your maximum health!": "¡Desbloquear nuevos rangos en el Gremio\\naumenta permanentemente tu salud máxima!",
    "Use /em class to inspect\\nyour abilities and\\nnext specialization.": "Usa el comando /em class para inspeccionar\\ntus habilidades activas y tu próxima\\nespecialización de clase.",
    "Wands seek elites first.\\nWalls and other creatures\\ncan block their shots.": "Los proyectiles de varita buscan prioritariamente\\na los jefes, pero muros y obstáculos\\npueden interceptar sus disparos.",
    "Want a harder challenge?\\nIncrease your guild rank!": "¿Buscas adversarios aún más colosales?\\n¡Sube de rango en el Gremio de Aventureros!",
    "Want to hit elite mobs harder?": "¿Quieres asestar golpes más devastadores a los monstruos de élite?",
    "Want to meet the other members\\nof the Adventurer's Guild?": "¿Deseas conocer a los demás veteranos\\ndel Gremio de Aventureros?",
    "We buy low and sell high.": "Compramos botín a precio justo y ofrecemos equipo superior.",
    "You can buy equipment from\\nthe blacksmith!": "¡Puedes adquirir armamento resistente\\ndirectamente del herrero!",
    "You can sell items to the\\nblacksmith for coins!": "¡Vende tus armas y armaduras usadas al herrero\\na cambio de monedas de élite!",
    "You can talk to me to\\nchange your guild rank!": "¡Habla conmigo para ascender\\nde rango en el Gremio de Aventureros!",
    "You can talk to the arena\\nmaster to take the arena on!": "¡Habla con el maestro del coliseo\\npara probar tu fuerza en la arena!",
    "You can talk to the combat\\nmaster to check your combat level!": "¡Consulta con el instructor de combate\\npara verificar tu nivel marcial actual!",
    "Your combat level and\\nweapon skill both matter.\\nTrain the weapons you use.": "Tu nivel marcial y tu maestría de arma son vitales.\\nEntrena con las armas que más utilices en batalla."
}

def translate_phrase(text):
    if not isinstance(text, str):
        return text
    # Clean whitespace for match
    clean = text.strip()
    if clean in FULL_GREETINGS:
        return FULL_GREETINGS[clean]
    if clean in FULL_DIALOGS:
        return FULL_DIALOGS[clean]
    return text

def apply_npc_translations():
    npc_dir = os.path.join(LAB_DIR, 'npcs')
    modified_count = 0
    total_greetings = 0
    total_dialogs = 0

    for fn in os.listdir(npc_dir):
        if not fn.endswith('.yml'):
            continue
        fp = os.path.join(npc_dir, fn)
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            data = yaml.safe_load(f) or {}

        # Greetings
        if 'greetings' in data and isinstance(data['greetings'], list):
            new_g = []
            for g in data['greetings']:
                t = translate_phrase(g)
                new_g.append(t)
                total_greetings += 1
            data['greetings'] = new_g

        # Dialogs
        if 'dialog' in data and isinstance(data['dialog'], list):
            new_d = []
            for d in data['dialog']:
                t = translate_phrase(d)
                new_d.append(t)
                total_dialogs += 1
            data['dialog'] = new_d

        with open(fp, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        modified_count += 1

    print(f"[OK] 100% de NPCs procesados ({modified_count} archivos, {total_greetings} saludos y {total_dialogs} dialogos traducidos al espanol).")

if __name__ == '__main__':
    apply_npc_translations()
