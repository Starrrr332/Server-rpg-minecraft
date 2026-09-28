# -*- coding: utf-8 -*-
"""
Script de expansión de contenido y enriquecimiento RPG para el Gremio de Aventureros.
Ejecución exclusiva en el entorno aislado gremio_aventureros_lab/.
"""

import os
import yaml

BASE_DIR = r"c:\Users\amaro\OneDrive\Desktop\Bot para server\gremio_aventureros_lab"
QUESTS_DIR = os.path.join(BASE_DIR, "customquests")
BOSSES_DIR = os.path.join(BASE_DIR, "custombosses")
ITEMS_DIR = os.path.join(BASE_DIR, "customitems")
NPCS_DIR = os.path.join(BASE_DIR, "npcs")

# Asegurar directorios
for d in [QUESTS_DIR, BOSSES_DIR, ITEMS_DIR, NPCS_DIR]:
    os.makedirs(d, exist_ok=True)

def write_yaml(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"[OK] Generado: {os.path.basename(filepath)}")

# ==============================================================================
# 1. MISIONES DE PROGRESIÓN POR RANGOS (RANGO F HASTA RANGO S)
# ==============================================================================

def create_rank_quests():
    # RANGO F: Novicio del Gremio
    q_f = {
        'isEnabled': True,
        'name': '&8[&7Rango F&8] <g:#90A4AE:#CFD8DC>El Juramento del Novicio</g>',
        'questLevel': 5,
        'questLore': [
            '&7Todo gran héroe comienza forjando su temple en el barro.',
            '&7Las inmediaciones de la ciudadela han sido asediadas',
            '&7por zombis errantes y arqueros esqueléticos.',
            '&7Empuña tus armas y limpia los alrededores del gremio.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f ¡Bienvenido, recluta! Antes de confiarte misiones de caza mayor,',
            '&e[Kaelen]&f debemos comprobar si tu acero no vacila ante los no-muertos.',
            '&e[Kaelen]&f Acaba con los merodeadores y regresa con vida.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡Excelente trabajo! Has demostrado que tu espíritu no se quiebra.',
            '&e[Kaelen]&f Aquí tienes tu paga y suministros de novicio. ¡Estás listo para el Rango E!'
        ],
        'customObjectives': {
            'EliminarZombis': {
                'objectiveType': 'KILL',
                'entityType': 'ZOMBIE',
                'amount': 12
            },
            'EliminarEsqueletos': {
                'objectiveType': 'KILL',
                'entityType': 'SKELETON',
                'amount': 8
            },
            'RecolectarCarnePodrida': {
                'objectiveType': 'FETCH',
                'material': 'ROTTEN_FLESH',
                'amount': 15
            }
        },
        'customRewards': [
            'currencyAmount=150:amount=1:chance=1.0',
            'filename=pocion_vigor_novicio.yml:amount=2:chance=1.0',
            'filename=elite_scrap_tiny.yml:amount=2:chance=1.0'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 250',
            'tell $player &a[Gremio] ¡Prueba de Rango F superada! Habla con Kaelen para reclamar misiones de Rango E.'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 360,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_f_bautismo_fuego.yml'), q_f)

    # RANGO E: Explorador Aprendiz
    q_e = {
        'isEnabled': True,
        'name': '&8[&aRango E&8] <g:#4CAF50:#81C784>La Purga del Nido Arácnido</g>',
        'questLevel': 20,
        'questLore': [
            '&7Has demostrado temple básico, pero el peligro aumenta.',
            '&7Las cuevas mineras y arboledas periféricas han sido invadidas',
            '&7por arañas venenosas cuyas telarañas asfixian los caminos.',
            '&7Extermina a los arácnidos y recupera ojos fermentados.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f Las arañas de cueva no dan tregua; su veneno desgasta rápidamente.',
            '&e[Kaelen]&f Lleva antídotos o leche. ¡No permitas que te acorralen en sus telas!'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡Magnífico! Las caravanas comerciales vuelven a circular sin peligro.',
            '&e[Kaelen]&f El Gremio reconoce tu ascenso como Explorador de Rango E.'
        ],
        'customObjectives': {
            'EliminarAranasComunes': {
                'objectiveType': 'KILL',
                'entityType': 'SPIDER',
                'amount': 15
            },
            'EliminarAranasCueva': {
                'objectiveType': 'KILL',
                'entityType': 'CAVE_SPIDER',
                'amount': 10
            },
            'RecolectarOjosArana': {
                'objectiveType': 'FETCH',
                'material': 'SPIDER_EYE',
                'amount': 8
            }
        },
        'customRewards': [
            'currencyAmount=350:amount=1:chance=1.0',
            'filename=antidoto_purificador.yml:amount=2:chance=1.0',
            'filename=elite_scrap_tiny.yml:amount=4:chance=1.0'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 500',
            'tell $player &a[Gremio] ¡Insignia de Rango E obtenida! Nuevos contratos de exploración disponibles.'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 720,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_e_nido_aracnido.yml'), q_e)

    # RANGO D: Veterano de Frontera
    q_d = {
        'isEnabled': True,
        'name': '&8[&9Rango D&8] <g:#0288D1:#4FC3F7>La Marea de los Ahogados</g>',
        'questLevel': 40,
        'questLore': [
            '&7Naufragios ancestrales han sido perturbados en las costas.',
            '&7Hordas de ahogados armados con tridentes encantados emergen',
            '&7de los arrecifes, apoyados por creepers volátiles.',
            '&7Protege las líneas de costa del reino con valentía.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f Los tridentes de los ahogados perforan cualquier armadura ligera.',
            '&e[Kaelen]&f Mantén distancia, esquiva sus proyectiles náuticos y rompe sus líneas.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡Las aguas vuelven a estar en calma! Eres oficialmente',
            '&e[Kaelen]&f un Veterano de Frontera Rango D. Toma esta chatarra de refuerzo.'
        ],
        'customObjectives': {
            'EliminarAhogados': {
                'objectiveType': 'KILL',
                'entityType': 'DROWNED',
                'amount': 20
            },
            'EliminarCreepers': {
                'objectiveType': 'KILL',
                'entityType': 'CREEPER',
                'amount': 10
            },
            'RecolectarCobre': {
                'objectiveType': 'FETCH',
                'material': 'COPPER_INGOT',
                'amount': 12
            }
        },
        'customRewards': [
            'currencyAmount=600:amount=1:chance=1.0',
            'filename=elite_scrap_medium.yml:amount=2:chance=1.0',
            'filename=amuleto_marea_abismal.yml:amount=1:chance=0.75'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 900',
            'tell $player &a[Gremio] ¡Condecoración Rango D otorgada por el Consejo del Gremio!'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 720,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_d_marea_corrupta.yml'), q_d)

    # RANGO C: Cazador de Élite
    q_c = {
        'isEnabled': True,
        'name': '&8[&eRango C&8] <g:#FFA000:#FFD54F>El Asedio de los Desoladores</g>',
        'questLevel': 60,
        'questLore': [
            '&7Clanes organizados de Saqueadores e Ilusionistas asaltan aldeas.',
            '&7Montan bestias devastadoras conocidas como Devastadores (Ravagers)',
            '&7capaces de derribar murallas de piedra en segundos.',
            '&7Es momento de actuar como un verdadero Cazador de Élite.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f Un Devastador enfurecido puede partir en dos a un guerrero desprevenido.',
            '&e[Kaelen]&f Coordina tus esquives con la tecla F y ataca tras su embestida.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡Una victoria aplastante! Los saqueadores se dispersan despavoridos.',
            '&e[Kaelen]&f Te has ganado la admiración del reino y el prestigioso Rango C.'
        ],
        'customObjectives': {
            'EliminarSaqueadores': {
                'objectiveType': 'KILL',
                'entityType': 'PILLAGER',
                'amount': 20
            },
            'EliminarVindicadores': {
                'objectiveType': 'KILL',
                'entityType': 'VINDICATOR',
                'amount': 12
            },
            'EliminarDevastadores': {
                'objectiveType': 'KILL',
                'entityType': 'RAVAGER',
                'amount': 3
            }
        },
        'customRewards': [
            'currencyAmount=1100:amount=1:chance=1.0',
            'filename=elite_scrap_large.yml:amount=2:chance=1.0',
            'filename=estandarte_cazador_elite.yml:amount=1:chance=0.8'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 1400',
            'tell $player &a[Gremio] ¡Has sido ascendido a Cazador de Élite Rango C!'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 1440,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_c_asedio_saqueador.yml'), q_c)

    # RANGO B: Héroe del Reino
    q_b = {
        'isEnabled': True,
        'name': '&8[&6Rango B&8] <g:#E65100:#FFB74D>La Forja del Inframundo</g>',
        'questLevel': 80,
        'questLore': [
            '&7Fisuras dimensionales en el Nether se han ensanchado.',
            '&7Las fortalezas infernales hierven bajo el asedio de legiones',
            '&7de esqueletos del wither, blazes centinela y piglins brutos.',
            '&7Incursiona en el fuego eterno y sofoca la rebelión abisal.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f En el Nether, el calor funde la cordura. Los Piglin Brutes no conocen el miedo',
            '&e[Kaelen]&f y las espadas del wither secarán tus venas. ¡Poción de fuego es indispensable!'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡Hazaña colosal! Has purificado la fortaleza con sangre y fuego.',
            '&e[Kaelen]&f Eres un auténtico Héroe del Reino (Rango B). Toma tus reliquias.'
        ],
        'customObjectives': {
            'EliminarEsqueletosWither': {
                'objectiveType': 'KILL',
                'entityType': 'WITHER_SKELETON',
                'amount': 18
            },
            'EliminarBlazes': {
                'objectiveType': 'KILL',
                'entityType': 'BLAZE',
                'amount': 15
            },
            'EliminarPiglinBrutes': {
                'objectiveType': 'KILL',
                'entityType': 'PIGLIN_BRUTE',
                'amount': 6
            }
        },
        'customRewards': [
            'currencyAmount=1800:amount=1:chance=1.0',
            'filename=elite_scrap_huge.yml:amount=2:chance=1.0',
            'filename=nucleo_de_magma_ancestral.yml:amount=1:chance=0.7'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 2200',
            'tell $player &6[Gremio] ¡Eres ahora un Héroe del Reino (Rango B) respetado por todos!'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 1440,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_b_infierno_cenizas.yml'), q_b)

    # RANGO A: Campeón del Gremio
    q_a = {
        'isEnabled': True,
        'name': '&8[&dRango A&8] <g:#7B1FA2:#BA68C8>La Herejía de las Sombras</g>',
        'questLevel': 100,
        'questLore': [
            '&7Nigromantes heréticos y evocadores oscuros intentan desgarrar',
            '&7el tejido cósmico entre las dimensiones del Fin y el reino terrenal.',
            '&7Endermans corrompidos por el vacío acechan en los templos prohibidos.',
            '&7Solo los más insignes Campeones tienen el poder de restaurar el orden.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f Los Evocadores convocan espíritus voraces y colmillos que surgen del suelo.',
            '&e[Kaelen]&f Mantente siempre en movimiento; un segundo de titubeo y serás historia.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡¡IMPRESIONANTE!! ¡Has quebrado la herejía en sus cimientos!',
            '&e[Kaelen]&f El Gran Consejo te nombra Campeón Rango A del Gremio de Aventureros.'
        ],
        'customObjectives': {
            'EliminarEndermans': {
                'objectiveType': 'KILL',
                'entityType': 'ENDERMAN',
                'amount': 25
            },
            'EliminarEvocadores': {
                'objectiveType': 'KILL',
                'entityType': 'EVOKER',
                'amount': 10
            },
            'EliminarBrujas': {
                'objectiveType': 'KILL',
                'entityType': 'WITCH',
                'amount': 8
            }
        },
        'customRewards': [
            'currencyAmount=2800:amount=1:chance=1.0',
            'filename=elite_scrap_huge.yml:amount=4:chance=1.0',
            'filename=reliquia_del_campeon_eterno.yml:amount=1:chance=0.6'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 3200',
            'broadcast &e[GREMIO] &6¡El aventurero &f$player &6ha ascendido a &dCampeón Rango A &6del Gremio de Aventureros!'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 2880,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_a_herejia_vacio.yml'), q_a)

    # RANGO S: Maestro de Caza Supremo
    q_s = {
        'isEnabled': True,
        'name': '&8[&4&lRANGO S&8] <g:#D50000:#AA00FF>El Juicio de las Tres Calamidades</g>',
        'questLevel': 125,
        'questLore': [
            '&4★ CONTRATO DE CAZA SUPREMO Y DEFINITIVO ★',
            '&7Las profecías antiguas se han cumplido: los tres señores del',
            '&7cataclismo han despertado en sus respectivas guaridas:',
            '&c- Lord Valerius, el Caballero de la Peste en las Criptas Olvidadas.',
            '&5- Mor''gath, la Reina del Enjambre Abisal en las Fosas Subterráneas.',
            '&6- Solarius, el Archidruida de la Llama Solar en la Cumbre Mística.',
            '&eErradica a los tres titanes y conviértete en Maestro Supremo de Caza.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f Ésta es la prueba definitiva de tu existencia como aventurero.',
            '&e[Kaelen]&f Pocos han desafiado a uno de estos señores; nadie los ha vencido a los tres.',
            '&e[Kaelen]&f ¡Que los vientos de la victoria guíen tu espada!'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡¡¡HISTÓRICO E INIGUALABLE!!! ¡Has derrotado a las tres calamidades!',
            '&e[Kaelen]&f ¡Me arrodillo ante ti! ¡Recibe la sagrada Corona del Maestro de Caza Supremo!'
        ],
        'customObjectives': {
            'DerrotarLordValerius': {
                'objectiveType': 'KILL_CUSTOM',
                'filename': 'lord_valerius_caballero_peste.yml',
                'amount': '1'
            },
            'DerrotarReinaMorgath': {
                'objectiveType': 'KILL_CUSTOM',
                'filename': 'morgath_reina_enjambre.yml',
                'amount': '1'
            },
            'DerrotarArchidruidaSolarius': {
                'objectiveType': 'KILL_CUSTOM',
                'filename': 'solarius_archidruida_solar.yml',
                'amount': '1'
            }
        },
        'customRewards': [
            'currencyAmount=6000:amount=1:chance=1.0',
            'filename=elite_scrap_huge.yml:amount=10:chance=1.0',
            'filename=corona_del_maestro_cazador_s.yml:amount=1:chance=1.0'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 5000',
            'broadcast &4&l[GREMIO] &6¡¡ATENCIÓN A TODO EL REINO!! &f$player &6¡ha completado el &4RANGO S &6y es el nuevo &c&lMAESTRO DE CAZA SUPREMO&6!'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 4320,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'gremio_rango_s_juicio_absoluto.yml'), q_s)

# ==============================================================================
# 2. MISIONES ESPECÍFICAS DE CAZA PARA LOS 3 JEFES
# ==============================================================================

def create_boss_hunt_quests():
    # Caza de Lord Valerius
    q_v = {
        'isEnabled': True,
        'name': '&8[&4Caza Élite&8] <g:#8B0000:#DC143C>Lord Valerius, el Caballero Peste</g>',
        'questLevel': 45,
        'questLore': [
            '&7En las Criptas Olvidadas mora Lord Valerius, paladín corrompido.',
            '&7Su mandoble infecto drena el vigor vital y quiebra el suelo.',
            '&7Adéntrate en su tumba y pon fin a su maldición eterna.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f ¡Aléjate de sus saltos sísmicos! Cuando el suelo se tiña de rojo,',
            '&e[Kaelen]&f salta hacia atrás con doble pulsación de F para evadir el impacto.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡Lord Valerius ha encontrado la paz! Las criptas están seguras. Toma tu recompensa.'
        ],
        'customObjectives': {
            'CazarValerius': {
                'objectiveType': 'KILL_CUSTOM',
                'filename': 'lord_valerius_caballero_peste.yml',
                'amount': '1'
            }
        },
        'customRewards': [
            'currencyAmount=800:amount=1:chance=1.0',
            'filename=elite_scrap_medium.yml:amount=3:chance=1.0',
            'filename=espada_del_paladin_caido.yml:amount=1:chance=0.4'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 1000'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 720,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'mision_jefe_valerius.yml'), q_v)

    # Caza de Mor'gath
    q_m = {
        'isEnabled': True,
        'name': '&8[&5Caza Abisal&8] <g:#4A0E4E:#AA00FF>Mor''gath, Reina del Enjambre</g>',
        'questLevel': 75,
        'questLore': [
            '&7En las fosas subterráneas más oscuras habita la Reina Mor''gath.',
            '&7Teje redes ácidas y genera vórtices gravitatorios que arrastran',
            '&7a los intrusos directamente hacia sus colmillos venenosos.',
            '&7Corta sus hilos de seda oscura y purga la madriguera.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f Cuando Mor''gath invoque el vórtice, corre en sentido opuesto sin parar.',
            '&e[Kaelen]&f Usa flechas a distancia para desgastarla antes de acercarte con tu arma.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡La Reina del Enjambre ha caído! El nido se desintegra. ¡Excelente caza!'
        ],
        'customObjectives': {
            'CazarMorgath': {
                'objectiveType': 'KILL_CUSTOM',
                'filename': 'morgath_reina_enjambre.yml',
                'amount': '1'
            }
        },
        'customRewards': [
            'currencyAmount=1500:amount=1:chance=1.0',
            'filename=elite_scrap_large.yml:amount=3:chance=1.0',
            'filename=arco_del_tejedor_abisal.yml:amount=1:chance=0.4'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 1800'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 1440,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'mision_jefe_morgath.yml'), q_m)

    # Caza de Solarius
    q_s = {
        'isEnabled': True,
        'name': '&8[&6World Boss&8] <g:#FF6F00:#FFD54F>Solarius, Archidruida de la Llama</g>',
        'questLevel': 110,
        'questLore': [
            '&7En la Cumbre Solar, el Archidruida Solarius canaliza la furia de los astros.',
            '&7Lanza lluvias de meteoros incandescentes, rayos estelares y canaliza',
            '&7trances de regeneración cósmica si sus agresores pierden la concentración.',
            '&7Reúne a tu mejor grupo y desafía al señor del solsticio.'
        ],
        'questAcceptDialog': [
            '&e[Kaelen]&f ¡Cuidado extremo! Cuando Solarius comience a canalizar su trance regenerativo,',
            '&e[Kaelen]&f todos deben golpearlo con sus ataques más potentes para interrumpir el hechizo.'
        ],
        'questCompleteMessage': [
            '&e[Kaelen]&f ¡El fuego solar se apaga y el cielo recupera la calma! ¡Eres una leyenda viva!'
        ],
        'customObjectives': {
            'CazarSolarius': {
                'objectiveType': 'KILL_CUSTOM',
                'filename': 'solarius_archidruida_solar.yml',
                'amount': '1'
            }
        },
        'customRewards': [
            'currencyAmount=3000:amount=1:chance=1.0',
            'filename=elite_scrap_huge.yml:amount=5:chance=1.0',
            'filename=baculo_de_la_corona_solar.yml:amount=1:chance=0.5'
        ],
        'questCompleteCommands': [
            'skills xp add $player fighting 3500',
            'broadcast &6[GREMIO] &e¡El aventurero &f$player &eha sofocado la ira de Solarius, Archidruida Solar!'
        ],
        'turnInNPC': 'maestro_cacerias_guild.yml',
        'questLockoutMinutes': 2880,
        'questAcceptPermission': '',
        'questLockoutPermission': '',
        'temporaryPermissions': []
    }
    write_yaml(os.path.join(QUESTS_DIR, 'mision_jefe_solarius.yml'), q_s)

# ==============================================================================
# 3. LOS 3 JEFES DE ÉLITE PERSONALIZADOS (+ JEFES DE TIER 1-4)
# ==============================================================================

def create_custom_bosses():
    # JEFE 1: Lord Valerius, el Caballero de la Peste
    b_valerius = {
        'isEnabled': True,
        'entityType': 'WITHER_SKELETON',
        'name': '&8[&4Jefe de Cripta&8] <g:#8B0000:#DC143C>Lord Valerius, Caballero de la Peste</g>',
        'level': 45,
        'healthMultiplier': 5.0,
        'damageMultiplier': 1.5,
        'followDistance': 32,
        'announcementPriority': 2,
        'spawnMessage': '&8[ALERTA]&4 ¡Las criptas tiemblan! Lord Valerius desenvaina su mandoble pestilente.',
        'deathMessage:': '&8[GREMIO]&a ¡Lord Valerius ha sido derrotado en las criptas por &f$players&a!',
        'deathMessage': '&8[GREMIO]&a ¡Lord Valerius ha sido derrotado en las criptas por &f$players&a!',
        'escapeMessage': '&8[GREMIO]&7 Lord Valerius se funde entre las tinieblas de la cripta...',
        'locationMessage': '&cLord Valerius aguarda en la Cripta de los Reyes Olvidados.',
        'onDamageMessages': [
            '&8[&4Lord Valerius&8] &c¡Tu carne se corrompe ante mi acero maldito!',
            '&8[&4Lord Valerius&8] &4¡Siente el frío sepulcral de la peste!'
        ],
        'onDamagedMessages': [
            '&8[&4Lord Valerius&8] &4&l¡¡IMPACTO SÍSMICO!! &c¡Aléjense del epicentro antes del colapso!',
            '&8[&4Lord Valerius&8] &2&l¡¡NIEBLA MIASMÁTICA!! &a¡El veneno corrompe sus pulmones!'
        ],
        'powers': [
            'attack_wither.yml',
            'attack_poison.yml',
            'ground_pound.yml',
            'shield_wall.yml',
            'invulnerability_knockback.yml'
        ],
        'trails': [
            'SMOKE',
            'SOUL_FIRE_FLAME'
        ],
        'uniqueLootList': [
            'espada_del_paladin_caido.yml:1',
            'coraza_de_la_peste_profana.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'lord_valerius_caballero_peste.yml'), b_valerius)

    # JEFE 2: Mor'gath, Reina del Enjambre Abisal
    b_morgath = {
        'isEnabled': True,
        'entityType': 'SPIDER',
        'name': '&8[&5Jefe Abisal&8] <g:#4A0E4E:#AA00FF>Mor''gath, Reina del Enjambre</g>',
        'level': 75,
        'healthMultiplier': 6.5,
        'damageMultiplier': 1.8,
        'followDistance': 35,
        'announcementPriority': 2,
        'spawnMessage': '&8[ALERTA]&5 ¡Chasquidos de quijadas resuenan en las fosas! La Reina Mor''gath desciende de su nido.',
        'deathMessage': '&8[GREMIO]&d ¡La Reina Mor''gath ha caído destrozada ante el filo de &f$players&d!',
        'escapeMessage': '&8[GREMIO]&7 Mor''gath trepa a las grietas de la roca madre y se oculta en la oscuridad...',
        'locationMessage': '&dMor''gath acecha en el Nido de las Fosas Profundas.',
        'onDamageMessages': [
            '&8[&5Mor''gath&8] &d¡Tus entrañas alimentarán a mis miles de crías!',
            '&8[&5Mor''gath&8] &a¡El ácido disuelve tu armadura y tu carne!'
        ],
        'onDamagedMessages': [
            '&8[&5Mor''gath&8] &5&l¡¡VÓRTICE ABSORBENTE!! &d¡Corran hacia afuera o serán devorados vivos!',
            '&8[&5Mor''gath&8] &2&l¡¡DESPLIEGUE DE TELARAÑA VENENOSA!! &a¡Destruyan los capullos adhesivos!'
        ],
        'powers': [
            'attack_web.yml',
            'attack_vacuum.yml',
            'attack_poison.yml',
            'taze.yml',
            'invulnerability_knockback.yml'
        ],
        'trails': [
            'SQUID_INK',
            'PORTAL'
        ],
        'uniqueLootList': [
            'arco_del_tejedor_abisal.yml:1',
            'botas_de_la_seda_sombra.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'morgath_reina_enjambre.yml'), b_morgath)

    # JEFE 3: Solarius, Archidruida de la Llama Solar
    b_solarius = {
        'isEnabled': True,
        'entityType': 'EVOKER',
        'name': '&8[&6World Boss Solar&8] <g:#FF6F00:#FFD54F>Solarius, Archidruida de la Llama</g>',
        'level': 110,
        'healthMultiplier': 8.5,
        'damageMultiplier': 2.2,
        'followDistance': 40,
        'announcementPriority': 3,
        'spawnMessage': '&8[CATACLISMO CÓSMICO]&6 ¡Un destello enceguecedor ilumina el cielo! Solarius despierta con la ira del solsticio.',
        'deathMessage': '&8[GREMIO]&6 ¡El fuego solar se apaga! Solarius ha sido derrotado por la alianza de &f$players&6.',
        'escapeMessage': '&8[GREMIO]&e Solarius se disuelve en un haz de luz solar pura y asciende a los cielos...',
        'locationMessage': '&eSolarius aguarda en el Altar de la Cumbre Solar.',
        'onDamageMessages': [
            '&8[&6Solarius&8] &e¡Que el fuego de mil soles consuma tu alma mortal!',
            '&8[&6Solarius&8] &6¡Cenizas a las cenizas, imprudente invasor!'
        ],
        'onDamagedMessages': [
            '&8[&6Solarius&8] &6&l¡¡BOMBARDEO DE METEOROS SOLARES!! &e¡Busquen cobertura tras las columnas inmediatamente!',
            '&8[&6Solarius&8] &c&l¡¡TRANCE DE REGENERACIÓN CÓSMICA!! &4¡Ataquen con todo para quebrar su canalización!'
        ],
        'powers': [
            'attack_fireball.yml',
            'fireworks_barrage.yml',
            'lightning_bolts.yml',
            'channel_healing.yml',
            'invulnerability_fire.yml',
            'invulnerability_knockback.yml'
        ],
        'trails': [
            'FLAME',
            'END_ROD'
        ],
        'uniqueLootList': [
            'baculo_de_la_corona_solar.yml:1',
            'corona_del_sol_naciente.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'solarius_archidruida_solar.yml'), b_solarius)

    # Jefes de misiones Tier 1-4 existentes para consistencia 100%
    b_carnicero = {
        'isEnabled': True,
        'entityType': 'ZOMBIE',
        'name': '&8[&7Tier I&8] <g:#8B0000:#B22222>Carnicero de Almas</g>',
        'level': 15,
        'healthMultiplier': 3.0,
        'damageMultiplier': 1.2,
        'announcementPriority': 1,
        'spawnMessage': '&8[ALERTA]&c ¡El Carnicero de Almas arrastra sus ganchos por el suelo ensangrentado!',
        'deathMessage': '&8[GREMIO]&a ¡El Carnicero de Almas ha sido ejecutado por &f$players&a!',
        'powers': [
            'attack_poison.yml',
            'attack_vacuum.yml',
            'invulnerability_knockback.yml'
        ],
        'uniqueLootList': [
            'totem_de_osamenta.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'carnicero_de_almas.yml'), b_carnicero)

    b_ignis = {
        'isEnabled': True,
        'entityType': 'BLAZE',
        'name': '&8[&6Tier II&8] <g:#FF4500:#FFD700>Ignis, el Coloso de Lava</g>',
        'level': 35,
        'healthMultiplier': 4.0,
        'damageMultiplier': 1.4,
        'announcementPriority': 2,
        'spawnMessage': '&8[ALERTA]&6 ¡Ignis ruge desde el magma incandescente!',
        'deathMessage': '&8[GREMIO]&a ¡Ignis se ha enfriado ante el temple de &f$players&a!',
        'powers': [
            'attack_fireball.yml',
            'attack_fire.yml',
            'invulnerability_fire.yml'
        ],
        'uniqueLootList': [
            'pergamino_lluvia_meteoros.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'ignis_coloso_lava.yml'), b_ignis)

    b_ymir = {
        'isEnabled': True,
        'entityType': 'STRAY',
        'name': '&8[&bTier III&8] <g:#00BFFF:#F0F8FF>Ymir, el Devorador Glacial</g>',
        'level': 65,
        'healthMultiplier': 5.5,
        'damageMultiplier': 1.7,
        'announcementPriority': 2,
        'spawnMessage': '&8[ALERTA]&b ¡Una ventisca gélida anuncia la llegada de Ymir!',
        'deathMessage': '&8[GREMIO]&a ¡El frío glacial de Ymir ha sido quebrado por &f$players&a!',
        'powers': [
            'attack_freeze.yml',
            'frost_walker.yml',
            'shield_wall.yml'
        ],
        'uniqueLootList': [
            'lagrima_invernal.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'ymir_devorador_glacial.yml'), b_ymir)

    b_astraeus = {
        'isEnabled': True,
        'entityType': 'WITHER',
        'name': '&8[&dMÍTICA&8] <g:#FFD700:#8A2BE2>Astraeus, Heraldo de las Estrellas</g>',
        'level': 90,
        'healthMultiplier': 7.5,
        'damageMultiplier': 2.0,
        'announcementPriority': 3,
        'spawnMessage': '&8[JUICIO DE TITANES]&d ¡Astraeus rasga el cosmos sobre el reino!',
        'deathMessage': '&8[GREMIO]&6 ¡¡Astraeus ha sido derrotado por la legendaria alianza de &f$players&6!!',
        'powers': [
            'attack_gravity.yml',
            'lightning_bolts.yml',
            'fireworks_barrage.yml',
            'invulnerability_knockback.yml'
        ],
        'uniqueLootList': [
            'totem_del_heraldo_celestial.yml:1'
        ],
        'dropsEliteMobsLoot': True,
        'dropsVanillaLoot': False
    }
    write_yaml(os.path.join(BOSSES_DIR, 'astraeus_heraldo_estrellas_p4.yml'), b_astraeus)

# ==============================================================================
# 4. TABLAS DE BOTÍN Y RECOMPENSAS TEMÁTICAS (CUSTOMITEMS)
# ==============================================================================

def create_custom_items():
    items = {
        # Lord Valerius Loot
        'espada_del_paladin_caido.yml': {
            'isEnabled': True,
            'material': 'NETHERITE_SWORD',
            'name': '&4Mandoble del Paladín Caído',
            'lore': [
                '&8[Arma Legendaria de Élite - Rango D/C]',
                '&7Forjada en la época dorada de los reyes sagrados,',
                '&7mancillada por siglos en la tumba de Lord Valerius.',
                '&cEl acero exhala una niebla fúnebre que drena vitalidad.',
                '&8--------------------------------',
                '&6Pasiva Rúnica: &eRobo de Vida Profano',
                '&7Restaura un 6% del daño infligido al golpear enemigos.',
                '&8Nivel de maestría requerido: 45'
            ],
            'enchantments': [
                'DAMAGE_ALL,5',
                'FIRE_ASPECT,2',
                'UNBREAKING,4'
            ]
        },
        'coraza_de_la_peste_profana.yml': {
            'isEnabled': True,
            'material': 'NETHERITE_CHESTPLATE',
            'name': '&4Coraza de la Peste Profana',
            'lore': [
                '&8[Armadura Pesada de Élite - Rango D/C]',
                '&7Pechera maciza impregnada de miasma espectral.',
                '&7Su portador siente el latido inquebrantable de la cripta.',
                '&8--------------------------------',
                '&6Pasiva Rúnica: &2Resistencia Miasmática',
                '&7Reduce el daño recibido por veneno y wither en un 50%.',
                '&8Nivel de maestría requerido: 45'
            ],
            'enchantments': [
                'PROTECTION_ENVIRONMENTAL,5',
                'PROTECTION_PROJECTILE,4',
                'UNBREAKING,4'
            ]
        },

        # Mor'gath Loot
        'arco_del_tejedor_abisal.yml': {
            'isEnabled': True,
            'material': 'BOW',
            'name': '&5Arco del Tejedor Abisal',
            'lore': [
                '&8[Arma Mítica de Élite - Rango C/B]',
                '&7Tallado con los colmillos y la seda endurecida de Mor''gath.',
                '&dLas flechas disparadas silban como un enjambre voraz.',
                '&8--------------------------------',
                '&6Pasiva Rúnica: &dTela Inmovilizadora',
                '&7Aplica lentitud y ceguera momentánea a la presa impactada.',
                '&8Nivel de maestría requerido: 70'
            ],
            'enchantments': [
                'ARROW_DAMAGE,6',
                'ARROW_KNOCKBACK,2',
                'ARROW_INFINITE,1',
                'UNBREAKING,5'
            ]
        },
        'botas_de_la_seda_sombra.yml': {
            'isEnabled': True,
            'material': 'NETHERITE_BOOTS',
            'name': '&5Escarpes de Seda Sombra',
            'lore': [
                '&8[Armadura Mítica de Élite - Rango C/B]',
                '&7Confeccionadas con las hebras más densas de la telaraña abisal.',
                '&7Permiten deslizarse en la penumbra con agilidad sobrehumana.',
                '&8--------------------------------',
                '&6Pasiva Rúnica: &bPaso Etéreo',
                '&7Inmunidad completa al daño de caída y movimiento sin fricción.',
                '&8Nivel de maestría requerido: 70'
            ],
            'enchantments': [
                'PROTECTION_ENVIRONMENTAL,5',
                'PROTECTION_FALL,5',
                'DEPTH_STRIDER,3',
                'UNBREAKING,5'
            ]
        },

        # Solarius Loot
        'baculo_de_la_corona_solar.yml': {
            'isEnabled': True,
            'material': 'GOLDEN_HOE',
            'name': '&6Báculo de la Corona Solar',
            'lore': [
                '&8[Reliquia Cósmica Suprema - Rango A/S]',
                '&eEmpuñado por Solarius durante el solsticio primordial.',
                '&6Canaliza llamaradas de plasma estelar que calcinan las defensas enemigas.',
                '&8--------------------------------',
                '&cEfecto de Impacto: &eFulguración Solar',
                '&7Desata un estallido ígneo sobre los enemigos circundantes.',
                '&8Nivel de maestría requerido: 100'
            ],
            'enchantments': [
                'DAMAGE_ALL,7',
                'FIRE_ASPECT,3',
                'SWEEPING_EDGE,4',
                'UNBREAKING,6'
            ]
        },
        'corona_del_sol_naciente.yml': {
            'isEnabled': True,
            'material': 'NETHERITE_HELMET',
            'name': '&6Corona del Sol Naciente',
            'lore': [
                '&8[Reliquia Cósmica Suprema - Rango A/S]',
                '&eDiadema forjada en las llamas de un cometa solar.',
                '&fOtorga visión clara en la noche más oscura y bendición solar.',
                '&8--------------------------------',
                '&6Pasiva Rúnica: &6Bendición Solar',
                '&7Aumenta la regeneración pasiva y previene quemaduras.',
                '&8Nivel de maestría requerido: 100'
            ],
            'enchantments': [
                'PROTECTION_ENVIRONMENTAL,6',
                'PROTECTION_FIRE,6',
                'WATER_WORKER,1',
                'UNBREAKING,6'
            ]
        },

        # Corona de Rango S Supremo
        'corona_del_maestro_cazador_s.yml': {
            'isEnabled': True,
            'material': 'NETHERITE_HELMET',
            'name': '&4&lCorona del Maestro de Caza Supremo',
            'lore': [
                '&8[Insignia Máxima del Gran Consejo del Gremio]',
                '&6Otorgada exclusivamente a los héroes legendarios que han derrotado',
                '&6a las tres calamidades del reino en el Rango S.',
                '&c"Tu temple es de acero; tu voluntad, una leyenda imperecedera."',
                '&8--------------------------------',
                '&ePrestigio de Rango S: &f+15% Daño contra Jefes de Mazmorra',
                '&8Nivel de maestría requerido: 120'
            ],
            'enchantments': [
                'PROTECTION_ENVIRONMENTAL,7',
                'PROTECTION_PROJECTILE,6',
                'PROTECTION_EXPLOSIONS,6',
                'MENDING,1',
                'UNBREAKING,7'
            ]
        },

        # Recompensas de Misiones de Rango
        'pocion_vigor_novicio.yml': {
            'isEnabled': True,
            'material': 'POTION',
            'name': '&aElixir de Vigor del Novicio',
            'lore': [
                '&7Brebaje reconfortante entregado a los reclutas del gremio.',
                '&2Otorga regeneración y resistencia básica en combate.',
                '&8Consumible de campo'
            ],
            'potionEffects': [
                'REGENERATION,0,120',
                'SPEED,0,180'
            ]
        },
        'antidoto_purificador.yml': {
            'isEnabled': True,
            'material': 'POTION',
            'name': '&2Antídoto Purificador del Cazador',
            'lore': [
                '&7Destilado alquímico para neutralizar el veneno de arácnidos.',
                '&aInmuniza temporalmente contra toxinas y parálisis.',
                '&8Consumible de campo'
            ],
            'potionEffects': [
                'HEAL,1,0',
                'RESISTANCE,0,60'
            ]
        },
        'amuleto_marea_abismal.yml': {
            'isEnabled': True,
            'material': 'HEART_OF_THE_SEA',
            'name': '&bAmuleto de la Marea Abisal',
            'lore': [
                '&8[Reliquia de Rango D]',
                '&7Un fragmento marino bendecido por los sacerdotes del puerto.',
                '&3Permite respirar bajo el agua y otorga nado veloz.'
            ],
            'enchantments': [
                'UNBREAKING,3'
            ]
        },
        'estandarte_cazador_elite.yml': {
            'isEnabled': True,
            'material': 'GOLDEN_AXE',
            'name': '&eHacha de Guerra del Cazador de Élite',
            'lore': [
                '&8[Arma Oficial de Rango C]',
                '&7Forjada para quebrar escudos de saqueadores y pieles duras.',
                '&6Inflige un 15% más de daño crítico al impactar.'
            ],
            'enchantments': [
                'DAMAGE_ALL,4',
                'UNBREAKING,3'
            ]
        },
        'nucleo_de_magma_ancestral.yml': {
            'isEnabled': True,
            'material': 'MAGMA_BLOCK',
            'name': '&6Núcleo de Magma Ancestral',
            'lore': [
                '&8[Reliquia de Rango B]',
                '&7Piedra ígnea del corazón de una fortaleza del Nether.',
                '&cIrradia un calor que entibia el acero y fortalece los golpes.'
            ],
            'enchantments': [
                'FIRE_ASPECT,2'
            ]
        },
        'reliquia_del_campeon_eterno.yml': {
            'isEnabled': True,
            'material': 'TOTEM_OF_UNDYING',
            'name': '&dTótem del Campeón Eterno',
            'lore': [
                '&8[Reliquia Suprema de Rango A]',
                '&7Salva a su portador de un golpe mortal con bendición arcana.',
                '&5Forjado con la energía recolectada de la anomalía del Vacío.'
            ]
        },

        # Items de Misiones Tier 1-4 existentes
        'totem_de_osamenta.yml': {
            'isEnabled': True,
            'material': 'BONE',
            'name': '&8Tótem de Osamenta Profanada',
            'lore': [
                '&7Restos óseos impregnados con la esencia del Carnicero.',
                '&8Utilizado para reforzar armaduras en el herrero del gremio.'
            ]
        },
        'pergamino_lluvia_meteoros.yml': {
            'isEnabled': True,
            'material': 'PAPER',
            'name': '&6Pergamino: Lluvia de Meteoros',
            'lore': [
                '&7Un manuscrito arcano obtenido del núcleo ardiente de Ignis.',
                '&ePermite imbuir armas con daño de fuego abrasador.'
            ]
        },
        'lagrima_invernal.yml': {
            'isEnabled': True,
            'material': 'GHAST_TEAR',
            'name': '&bLágrima Invernal de Ymir',
            'lore': [
                '&7Cristal helado que jamás se descongela.',
                '&3Irradia un aura que ralentiza a los enemigos cercanos.'
            ]
        },
        'totem_del_heraldo_celestial.yml': {
            'isEnabled': True,
            'material': 'NETHER_STAR',
            'name': '&dFragmento Estelar de Astraeus',
            'lore': [
                '&5★ Reliquia de los Titanes ★',
                '&7El núcleo estelar de Astraeus, concentrando la energía de una supernova.',
                '&eEl objeto de forja más codiciado de todo Holy Server.'
            ]
        }
    }

    for fn, data in items.items():
        write_yaml(os.path.join(ITEMS_DIR, fn), data)

# ==============================================================================
# 5. ENRIQUECIMIENTO DE DIÁLOGOS DE NPCs INSTRUCTORES Y ALQUIMISTA
# ==============================================================================

def enrich_instructor_npcs():
    # 1. RAGNA: Instructor Berserker (Guerrero Agresivo)
    ragna_path = os.path.join(NPCS_DIR, 'class_trainer_berserker.yml')
    if os.path.exists(ragna_path):
        with open(ragna_path, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['greetings'] = [
            "¿Sientes hervir la sangre en tus venas?\\n¡El combate no es para los indecisos!",
            "¡Saludos, guerrero!\\n¿Listo para desatar la furia de la batalla?",
            "El dolor es combustible.\\n¡Conviértelo en fuerza destructiva!"
        ]
        d['dialog'] = [
            "Inspecciona tu progreso marcial\\ny especializaciones con /em class.",
            "TÁCTICA BERSERKER: La Furia se acumula asestando\\ny recibiendo daño. ¡No te detengas;\\nla pasividad drena tu poder!",
            "TÉCNICA DE SALTO: Pulsa la tecla F dos veces\\npara realizar una carga de evasión rápida.\\nÚsala para esquivar estallidos de jefes.",
            "CONTRA JEFES SÍSMICOS: Cuando un jefe prepare\\nun golpe contra el suelo, no bloquees con escudo;\\n¡salta hacia atrás para evitar la onda expansiva!",
            "SINERGIA MARCIAL: Las hachas de combate desgarran\\narmaduras y provocan sangrado continuo.\\n¡Ideal para derribar esbirros resistentes!",
            "GESTIÓN DE VITALIDAD: Los berserkers luchan al borde\\nde la muerte. Lleva siempre pociones de regeneración\\npara cuando tu furia entre en enfriamiento."
        ]
        d['farewell'] = [
            "Vuelve más fuerte... ¡o con más cicatrices!",
            "¡Que tu hacha nunca pierda su filo!",
            "¡Demuestra de qué madera estás hecho!"
        ]
        write_yaml(ragna_path, d)

    # 2. ALDRIC: Instructor Paladín (Guerrero Protector / Tanque)
    aldric_path = os.path.join(NPCS_DIR, 'class_trainer_paladin.yml')
    if os.path.exists(aldric_path):
        with open(aldric_path, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['greetings'] = [
            "Mantente firme como una muralla de piedra.\\nOtros sobrevivirán al abrigo de tu escudo.",
            "Que la luz sagrada bendiga tus pasos, paladín.",
            "La disciplina y el deber son nuestro mayor estandarte."
        ]
        d['dialog'] = [
            "Inspecciona tu progreso marcial\\ny especializaciones con /em class.",
            "GESTIÓN DE AMENAZA (AGGRO): Como tanque principal,\\ntu deber es golpear primero y usar Provocación.\\n¡Mantén la furia del jefe centrada en ti!",
            "ESCUDO Y POSICIONAMIENTO: Nunca des la espalda\\nal jefe de mazmorra. Bloquear en el instante exacto\\nreduce el retroceso y absorbe el impacto letal.",
            "REGENERACIÓN SAGRADA: La energía de paladín\\nse recupera más rápido mientras te mantengas\\nen combate cuerpo a cuerpo contra el jefe.",
            "PROTECCIÓN DE ALIADOS: Si un mago o cazador\\natrae la amenaza por exceso de daño, interponte\\ninmediatamente y aplica tu habilidad insignia.",
            "AVISO DE BARRERAS: Cuando un jefe invoque una cúpula\\no barrera defensiva, no desgastes tu energía;\\nespera a que la cúpula caiga para asestar el golpe de gracia."
        ]
        d['farewell'] = [
            "Mantén tu juramento inquebrantable.",
            "Que tu escudo nunca caiga en batalla.",
            "Camina con honor bajo la luz."
        ]
        write_yaml(aldric_path, d)

    # 3. ORIN: Instructor Hechicero (Mago / Taumaturgo)
    orin_path = os.path.join(NPCS_DIR, 'class_trainer_spellcaster.yml')
    if os.path.exists(orin_path):
        with open(orin_path, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['greetings'] = [
            "El poder mágico abunda en el aire.\\nEl verdadero desafío reside en controlarlo.",
            "Saludos, iniciado en las artes místicas.\\n¿Vienes a afilar tu mente?",
            "La magia sin disciplina es una invitación al desastre."
        ]
        d['dialog'] = [
            "Inspecciona tu progreso marcial\\ny especializaciones con /em class.",
            "ROTACIÓN DE MANÁ: El maná se recupera de forma pasiva,\\npero lanzar conjuros seguidos agota tus reservas.\\nAlterna ataques básicos entre cada invocación.",
            "VARITAS VS BASTONES: Las varitas disparan proyectiles\\ndirigidos hacia el jefe (mono-objetivo).\\nLos bastones lanzan esferas de fuego que estallan en área.",
            "APUNTADO EN GRUPO: Con bastones de fuego,\\napunta siempre al suelo entre la multitud enemiga;\\nel daño por salpicadura multiplica el impacto.",
            "LÍNEA DE VISIÓN: Recuerda que pilares y muros\\ninterceptan los disparos arcanos. Mantén siempre\\nun ángulo limpio hacia tu objetivo.",
            "INTERRUPCIÓN DE CANALIZACIONES: Cuando un jefe oscuro\\ncomience a flotar o brillar en trance curativo,\\n¡descarga todos tus hechizos para romper su concentración!",
            "AMENAZA MÁGICA: El daño masivo atrae la ira del jefe.\\nDeja que el tanque establezca la amenaza antes de\\ndesatar tu artillería mágica pesada."
        ]
        d['farewell'] = [
            "Sigue cuestionando el tejido de la realidad.",
            "Que la llama arcana ilumine tu senda.",
            "El conocimiento es la armadura más impenetrable."
        ]
        write_yaml(orin_path, d)

    # 4. ROWAN: Instructor Montaraz (Cazador / Tirador)
    rowan_path = os.path.join(NPCS_DIR, 'class_trainer_ranger.yml')
    if os.path.exists(rowan_path):
        with open(rowan_path, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['greetings'] = [
            "Observa en silencio. Respira con calma.\\nEl cazador certero jamás se precipita.",
            "Saludos, explorador. ¿El viento te susurra secretos?",
            "El arco es solo una extensión de tu propia respiración."
        ]
        d['dialog'] = [
            "Inspecciona tu progreso marcial\\ny especializaciones con /em class.",
            "FLUJO DE CONCENTRACIÓN: La Concentración del montaraz\\nse regenera al máximo tras 5 segundos\\nsin recibir daño. ¡Aprende a esquivar constantemente!",
            "TÁCTICA DE FLECHAS ESPECIALES: Usa flechas de veneno\\npara detener la regeneración natural del jefe.\\nUsa flechas de lentitud para facilitar el kiting.",
            "EL ARTE DEL KITING: Corre trazando círculos amplios\\nalrededor del jefe de mazmorra. Mantenerte en movimiento\\nhace que sus proyectiles fallen por completo.",
            "DISPARO A PUNTOS DÉBILES: Los impactos a la cabeza\\nprovocan daño crítico y aumentan la probabilidad\\nde quebrar la postura de los esbirros.",
            "FLECHAS ESPECTRALES: En mazmorras oscuras o laberínticas,\\nmarca al jefe con flechas espectrales. Tu equipo entero\\npodrá rastrear su contorno a través de la niebla."
        ]
        d['farewell'] = [
            "No dejes rastro al marcharte.",
            "Que el viento incline tus flechas hacia el blanco.",
            "Buena caza en la espesura."
        ]
        write_yaml(rowan_path, d)

    # 5. CHARLES: Instructor de Combate General
    charles_path = os.path.join(NPCS_DIR, 'combat_instructor.yml')
    if os.path.exists(charles_path):
        with open(charles_path, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['greetings'] = [
            "¿Quieres dominar las tácticas avanzadas de combate?",
            "¿Listo para entender cómo vencer a los jefes más brutales?",
            "Un buen guerrero entrena su cuerpo; un maestro entrena su mente.",
            "Bienvenido al patio de armas. Escucha atentamente mis consejos."
        ]
        # Conservar y enriquecer diálogos tácticos
        d['dialog'] = [
            "El daño infligido genera amenaza.\\nLos jefes perseguirán con furia a quien\\nacumule mayor nivel de amenaza.",
            "Las provocaciones obligan al jefe\\na centrar sus ataques en el tanque\\ndurante unos instantes cruciales.",
            "Dale a tu tanque unos segundos\\npara provocar y reunir a los monstruos\\nantes de abrir fuego a discreción.",
            "El suelo teñido de rojo es una advertencia.\\n¡Aléjate de inmediato antes\\nde que caiga el ataque devastador!",
            "Tu nivel marcial y tu maestría de arma son vitales.\\nEntrena con las armas que más\\nutilices en batalla.",
            "Las armas propias de tu clase infligen\\nun 10% más de daño adicional.\\nConsulta tu menú de clase con /em class.",
            "Pulsa F dos veces para esquivar con destreza.\\nF + clic izquierdo: Habilidad Insignia.\\nF + clic derecho: Habilidad de Utilidad.",
            "Tu vida y energía de clase aparecen\\njusto sobre tu barra de objetos.\\nVigila ambas atentamente en combate.",
            "El Maná se regenera con el tiempo.\\nLos Berserkers acumulan Furia de batalla\\nasestando y recibiendo ataques.",
            "Los Paladines se recuperan más rápido\\ncerca de los jefes; los Clérigos\\ncerca de sus aliados heridos.",
            "Los Montaraces recuperan Concentración\\nmás rápido tras 5 segundos\\nsin recibir daño alguno.",
            "Los proyectiles de varita buscan prioritariamente\\na los jefes, pero muros y obstáculos\\npueden interceptar sus disparos.",
            "Las bolas de fuego de bastón estallan al impactar.\\nApúntalas al centro de grupos\\nde enemigos agrupados.",
            "Lleva abundantes provisiones a las mazmorras.\\nComer toma tiempo; busca siempre\\nun respiro seguro en la batalla.",
            "Repara todo tu equipo dañado antes\\nde adentrarte en una mazmorra.\\nVisita siempre al maestro armero.",
            "Los jefes de élite poseen mecánicas telegrafiadas.\\nCuando veas avisos en el chat o partículas concentradas,\\n¡reacciona de inmediato según el aviso!"
        ]
        write_yaml(charles_path, d)

    # 6. LYSANDRA: Maestra Alquimista del Gremio (NUEVO NPC)
    alquimista = {
        'isEnabled': True,
        'name': '<g:#2E7D32:#81C784>Lysandra, Maestra Alquimista</g>',
        'role': '<g:#1B5E20:#4CAF50><Alquimia y Boticas de Élite></g>',
        'profession': 'cleric',
        'spawnLocation': 'em_adventurers_guild,282.5,91,222.5,0,0',
        'spawnLocations': [],
        'greetings': [
            "¿Hueles a azufre y lágrimas de ghast?\\nBienvenido a mi laboratorio.",
            "Un guerrero sin elixires es carne de cementerio.",
            "¿Deseas conocer los secretos de la alquimia de combate?"
        ],
        'dialog': [
            "PREPARACIÓN PREVIA A LA INCURSIÓN:\\nBebe una poción de Resistencia al Fuego antes\\nde cruzar la niebla contra Ignis o Solarius.",
            "ANTÍDOTO CONTRA EL VENENO:\\nEl veneno de las arañas abisales no se quita solo.\\nLleva frascos de purificación para no perder vida por segundo.",
            "PURIFICACIÓN DEL WITHER:\\nLord Valerius corrompe tus corazones con wither.\\nElixir sagrado o leche neutralizan la podredumbre al instante.",
            "POCIONES ARROJADIZAS EN GRUPO:\\nLanza pociones arrojadizas de Curación Instantánea\\nal suelo entre tus compañeros para salvarlos en momentos críticos.",
            "POCIÓN DE FUERZA Y VELOCIDAD:\\nPara los jefes con saltos telegrafiados, la poción\\nde velocidad te permite salir del radio rojo sin agotarte.",
            "TRANSMUTACIÓN DE INGREDIENTES:\\nLos ojos fermentados y lágrimas de jefes sirven para\\ncrear los elixires más potentes del Gremio."
        ],
        'farewell': [
            "No bebas de frascos sin etiqueta.",
            "Que tus viales nunca se rompan en tu bolsa.",
            "Vuelve con más ingredientes exóticos de los jefes."
        ],
        'canTalk': True,
        'activationRadius': 3.5,
        'interactionType': 'CHAT',
        'syncMovement': True,
        'scripts': [],
        'transportRoutes': []
    }
    write_yaml(os.path.join(NPCS_DIR, 'alquimista_del_gremio.yml'), alquimista)

    # 7. Actualizar KAELEN (Maestro de Cacerías) para asignar todas las misiones
    kaelen_path = os.path.join(NPCS_DIR, 'maestro_cacerias_guild.yml')
    if os.path.exists(kaelen_path):
        with open(kaelen_path, 'r', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        d['questFileName'] = [
            # Misiones de Progresión Rango F a Rango S
            'gremio_rango_f_bautismo_fuego.yml',
            'gremio_rango_e_nido_aracnido.yml',
            'gremio_rango_d_marea_corrupta.yml',
            'gremio_rango_c_asedio_saqueador.yml',
            'gremio_rango_b_infierno_cenizas.yml',
            'gremio_rango_a_herejia_vacio.yml',
            'gremio_rango_s_juicio_absoluto.yml',
            # Misiones de Caza de Jefes Específicos
            'mision_jefe_valerius.yml',
            'mision_jefe_morgath.yml',
            'mision_jefe_solarius.yml',
            # Misiones de Tier existentes
            'mision_tier1_carnicero.yml',
            'mision_tier2_ignis.yml',
            'mision_tier3_ymir.yml',
            'mision_tier4_astraeus.yml'
        ]
        d['greetings'] = [
            "¡Saludos, honorable cazador del Gremio!",
            "¿Listo para reclamar gloria, oro y renombre?",
            "El tablero de contratos está repleto de desafíos."
        ]
        d['dialog'] = [
            "Tengo contratos clasificados desde el Rango F de Novicio\\nhasta el mítico Rango S de Maestro Supremo.",
            "Cada ascenso de rango desbloquea contratos más prestigiosos\\ny recompensas de mayor calibre.",
            "Para los mayores titanes del reino, coordina un grupo de héroes\\ncon tanque, sanador y atacantes a distancia."
        ]
        d['farewell'] = [
            "Buena caza. Regresa con la victoria.",
            "Mantén tu espada afilada y tu mente alerta.",
            "¡Por la gloria del Gremio de Aventureros!"
        ]
        write_yaml(kaelen_path, d)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("=== INICIANDO EXPANSIÓN Y ENRIQUECIMIENTO RPG PARA EL GREMIO ===")
    print("\n[FASE 1] Creando misiones de progresión por Rangos (F -> S)...")
    create_rank_quests()
    
    print("\n[FASE 2] Creando misiones de caza de jefes personalizados...")
    create_boss_hunt_quests()
    
    print("\n[FASE 3] Creando Jefes de Élite con mecánicas y avisos telegrafiados...")
    create_custom_bosses()
    
    print("\n[FASE 4] Creando armamento, armaduras y objetos temáticos de botín...")
    create_custom_items()
    
    print("\n[FASE 5] Enriqueciendo diálogos de instructores y añadiendo Alquimista...")
    enrich_instructor_npcs()
    
    print("\n=== EXPANSIÓN RPG COMPLETADA CON ÉXITO ===")

if __name__ == '__main__':
    main()
