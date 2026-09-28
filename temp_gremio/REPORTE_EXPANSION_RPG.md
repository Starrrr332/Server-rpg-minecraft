# 🛡️ Reporte de Expansión de Contenido RPG y Enriquecimiento - Gremio de Aventureros

> **Entorno de Trabajo Aislado:** `c:\Users\amaro\OneDrive\Desktop\Bot para server\gremio_aventureros_lab\`  
> **Servidor:** Holy Server (Minecraft RPG 1.21.1)  
> **Estado de Validación:** 144/144 Archivos YAML Verificados (0 Errores de Sintaxis)  

---

## 📜 1. Estructura de Misiones de Progresión por Rangos (F -> S)

Se ha diseñado e implementado una línea de ascensos del Gremio con lore inmersivo medieval, objetivos dinámicos y balance de recompensas:

| Rango | Archivo de Misión | Título / Lore | Nivel | Recompensas Destacadas |
| :--- | :--- | :--- | :---: | :--- |
| **Rango F** | `gremio_rango_f_bautismo_fuego.yml` | **El Juramento del Novicio**<br>Limpia los alrededores de no-muertos para obtener tu insignia. | Lv. 5 | 150 Monedas, 2x Elixir de Vigor, EXP Fighting +250 |
| **Rango E** | `gremio_rango_e_nido_aracnido.yml` | **La Purga del Nido Arácnido**<br>Purga cuevas mineras asediadas por arañas venenosas. | Lv. 20 | 350 Monedas, 2x Antídoto Purificador, EXP Fighting +500 |
| **Rango D** | `gremio_rango_d_marea_corrupta.yml` | **La Marea de los Ahogados**<br>Defiende las costas de invasores marinos y tridentes corruptos. | Lv. 40 | 600 Monedas, Amuleto de la Marea Abisal, EXP Fighting +900 |
| **Rango C** | `gremio_rango_c_asedio_saqueador.yml` | **El Asedio de los Desoladores**<br>Frena el asalto de saqueadores y bestias Ravager en las fronteras. | Lv. 60 | 1,100 Monedas, Hacha de Guerra de Cazador Élite, EXP +1,400 |
| **Rango B** | `gremio_rango_b_infierno_cenizas.yml` | **La Forja del Inframundo**<br>Incursión en fortalezas del Nether contra Wither Skeletons y Piglin Brutes. | Lv. 80 | 1,800 Monedas, Núcleo de Magma Ancestral, EXP +2,200 |
| **Rango A** | `gremio_rango_a_herejia_vacio.yml` | **La Herejía de las Sombras**<br>Neutraliza rituales oscuros de Evocadores y aberraciones del Vacío. | Lv. 100 | 2,800 Monedas, Tótem del Campeón Eterno, Anuncio Global Broadcast |
| **Rango S** | `gremio_rango_s_juicio_absoluto.yml` | **El Juicio de las Tres Calamidades**<br>★ Contrato Supremo: Vence a Lord Valerius, Mor'gath y Solarius. | Lv. 125 | 6,000 Monedas, Corona del Maestro de Caza Supremo, Prestigio de Servidor |

---

## ☠️ 2. Jefes de Élite Personalizados con Mecánicas Telegrafiadas

Se diseñaron e implementaron 3 nuevos Jefes de Élite con habilidades scriptadas, partículas atmosféricas y avisos telegrafiados en chat durante el combate:

### 1. **Lord Valerius, Caballero de la Peste**
- **Archivo:** `custombosses/lord_valerius_caballero_peste.yml`
- **Tipo de Entidad:** `WITHER_SKELETON` | **Nivel:** 45 | **Multiplicador de Vida:** 5.0x
- **Ubicación de Lore:** Cripta de los Reyes Olvidados (Open World / Mazmorra).
- **Mecánicas & Avisos Telegrafiados:**
  - *Impacto Sísmico:* `ground_pound.yml` + Aviso en chat: `§4§l¡¡IMPACTO SÍSMICO!! §c¡Aléjense del epicentro antes del colapso!` (Castiga jugadores agrupados que no salten con doble F).
  - *Niebla Miasmática:* `attack_poison.yml` + `attack_wither.yml` con aviso telegrafiado.
  - *Muro de Escudos:* `shield_wall.yml` activa bloqueo direccional al caer bajo el 50% de HP.
- **Botín Único:**
  - `espada_del_paladin_caido.yml`: Netherite Sword con filo V y pasiva *Robo de Vida Profano* (+6% vida drenada).
  - `coraza_de_la_peste_profana.yml`: Netherite Chestplate con pasiva *Resistencia Miasmática* (-50% daño de veneno y wither).

### 2. **Mor’gath, Reina del Enjambre Abisal**
- **Archivo:** `custombosses/morgath_reina_enjambre.yml`
- **Tipo de Entidad:** `SPIDER` (Abisal) | **Nivel:** 75 | **Multiplicador de Vida:** 6.5x
- **Ubicación de Lore:** Nido de las Fosas Profundas (Mazmorra Subterránea).
- **Mecánicas & Avisos Telegrafiados:**
  - *Vórtice Absorbente:* `attack_vacuum.yml` + Aviso en chat: `§5§l¡¡VÓRTICE ABSORBENTE!! §d¡Corran hacia afuera o serán devorados vivos!`.
  - *Capullos y Parálisis:* `attack_web.yml` + `taze.yml` inmovilizan a los jugadores en trampas de seda ácida.
- **Botín Único:**
  - `arco_del_tejedor_abisal.yml`: Arco mítico de élite con pasiva *Tela Inmovilizadora* (lentitud y ceguera al impactar).
  - `botas_de_la_seda_sombra.yml`: Netherite Boots con pasiva *Paso Etéreo* (inmunidad a daño de caída + paso ligero).

### 3. **Solarius, Archidruida de la Llama Solar**
- **Archivo:** `custombosses/solarius_archidruida_solar.yml`
- **Tipo de Entidad:** `EVOKER` | **Nivel:** 110 | **Multiplicador de Vida:** 8.5x
- **Ubicación de Lore:** Altar de la Cumbre Solar (World Boss).
- **Mecánicas & Avisos Telegrafiados:**
  - *Bombardeo de Meteoros:* `fireworks_barrage.yml` + `attack_fireball.yml` + Aviso: `§6§l¡¡BOMBARDEO DE METEOROS SOLARES!! §e¡Busquen cobertura tras las columnas inmediatamente!`.
  - *Trance de Regeneración Cósmica:* `channel_healing.yml` + Aviso: `§c§l¡¡TRANCE DE REGENERACIÓN CÓSMICA!! §4¡Ataquen con todo para quebrar su canalización!`.
- **Botín Único:**
  - `baculo_de_la_corona_solar.yml`: Arma cósmica con daño masivo y pasiva *Fulguración Solar* (explosión ígnea en cadena).
  - `corona_del_sol_naciente.yml`: Casco legendario con pasiva *Bendición Solar* (+regeneración pasiva e inmunidad a quemaduras).

---

## 🗣️ 3. Enriquecimiento de NPCs Instructores y Nueva Alquimista

Se reescribieron los diálogos de los instructores con guías prácticas y mecánicas reales de EliteMobs / AuraSkills:

1. **Guerrero Ofensivo (Ragna - Berserker):**
   - Tutorial de acumulación de Furia mediante daño asestado y recibido.
   - Instrucciones para esquivar con doble pulsación de `F` y romper posturas enemigas con hachas.
   - Consejos para evitar la onda de choque sísmica de los jefes sin desgastar el escudo.

2. **Guerrero Defensivo / Tanque (Aldric - Paladín):**
   - Guía completa de generación de amenaza (*Aggro/Threat*) y uso de Provocación.
   - Posicionamiento frontal sin dar la espalda al jefe para amortiguar golpes con escudo.
   - Regeneración pasiva de energía sagrada permaneciendo en rango de melé contra el jefe.

3. **Mago / Taumaturgo (Orin - Hechicero):**
   - Gestión y rotación de Maná; alternancia de hechizos con ataques básicos.
   - Diferencia táctica entre varitas (mono-objetivo guiado al jefe) y bastones de fuego (AoE por salpicadura).
   - Posicionamiento en retaguardia e interrupción de canalizaciones de jefes mágicos.

4. **Cazador / Montaraz (Rowan):**
   - Dinámica de Concentración: regeneración máxima tras 5 segundos sin recibir daño (*kiting* en círculos).
   - Uso estratégico de flechas de veneno (frenar regeneración), lentitud y flechas espectrales para visión en mazmorras oscuras.
   - Disparos críticos a la cabeza para desestabilizar esbirros.

5. **Maestra Alquimista (Lysandra - NUEVO NPC en el Gremio):**
   - Archivo: `npcs/alquimista_del_gremio.yml`
   - Guía de preparación previa con pociones de resistencia al fuego contra Ignis y Solarius.
   - Uso de elixires purificadores contra el Wither de Lord Valerius y antídotos contra toxinas de Mor'gath.
   - Coordinación de pociones arrojadizas de curación instantánea en combates grupales de mazmorra.

6. **Maestro de Cacerías (Kaelen):**
   - Archivo actualizado: `npcs/maestro_cacerias_guild.yml`
   - Asignación sincronizada de las 7 misiones de Rango (F hasta S), 3 misiones de caza de jefes nuevos y 4 misiones de tiers existentes.

---

## 🧪 4. Resultados de Validación y Coherencia

- **Total de Archivos YAML analizados:** 144
- **Errores de Sintaxis:** 0
- **Integridad de Referencias Cruzadas:**
  - Misiones ➡️ Jefes (`KILL_CUSTOM`): 100% Coherente.
  - Jefes ➡️ Botín (`uniqueLootList`): 100% Coherente.
  - Misiones ➡️ Recompensas (`customRewards`): 100% Coherente.
  - NPC Kaelen ➡️ Catálogo de Misiones: 100% Coherente.
