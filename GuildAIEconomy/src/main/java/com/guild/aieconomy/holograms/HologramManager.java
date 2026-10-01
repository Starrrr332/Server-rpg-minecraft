package com.guild.aieconomy.holograms;

import com.guild.aieconomy.GuildAIEconomy;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.ArmorStand;

import java.util.Arrays;
import java.util.List;

public class HologramManager {

    private final GuildAIEconomy plugin;
    private final boolean decentHologramsEnabled;

    public HologramManager(GuildAIEconomy plugin) {
        this.plugin = plugin;
        this.decentHologramsEnabled = Bukkit.getPluginManager().isPluginEnabled("DecentHolograms");
        if (decentHologramsEnabled) {
            plugin.getLogger().info("[GuildAIEconomy] ¡DecentHolograms detectado! Integración de hologramas HD activada.");
        } else {
            plugin.getLogger().info("[GuildAIEconomy] DecentHolograms no activo. Usando ArmorStands como fallback.");
        }
    }

    public void setupGuildHolograms() {
        World world = Bukkit.getWorld("em_adventurers_guild");
        if (world == null) {
            world = Bukkit.getWorlds().get(0);
        }
        if (world == null) return;

        // 1. Holograma Tienda Vanilla
        Location vanillaLoc = new Location(world, 305.5, 80.5, 215.5);
        createHologram("guild_vanilla_shop", vanillaLoc, Arrays.asList(
                "§b§l🧱 PUESTO DE COMERCIO VANILLA",
                "§7Compra y venta de todos los bloques del juego",
                "§e▶ Habla con el Mercader o usa §f/guildai shop"
        ));

        // 2. Holograma Bazar RPG / EliteMobs
        Location customLoc = new Location(world, 311.5, 80.5, 215.5);
        createHologram("guild_custom_rpg_shop", customLoc, Arrays.asList(
                "§d§l⚔️ BAZAR DE RELIQUIAS Y EQUIPO RPG",
                "§7Armas, Armaduras y Objetos Legendarios de EliteMobs",
                "§e▶ Precios a partir de 25,000 monedas | §f/guildai customshop"
        ));

        // 3. Holograma Tablón de Cacerías
        Location questLoc = new Location(world, 285.5, 93.5, 220.5);
        createHologram("guild_quests_board", questLoc, Arrays.asList(
                "§e§l📜 TABLÓN DE CACERÍAS DEL GREMIO",
                "§7Misiones de Mazmorras Tiers 1, 2 y 3 & Modo Historia",
                "§a▶ ¡Habla con Kaelen para reclamar recompensas!"
        ));

        // 4. Holograma Salón del Consejo & Rangos
        Location rankLoc = new Location(world, 308.5, 80.5, 208.5);
        createHologram("guild_ranks_council", rankLoc, Arrays.asList(
                "§a§l🏆 SALÓN DE CONSEJO Y RANGOS",
                "§7Aumenta tu reputación de Aventurero (Rango F ➔ S)",
                "§fDescuentos en Impuestos y Beneficios Exclusivos"
        ));
    }

    private void createHologram(String name, Location location, List<String> lines) {
        if (location == null || location.getWorld() == null) return;

        if (decentHologramsEnabled) {
            try {
                String worldName = location.getWorld().getName();
                double x = location.getX();
                double y = location.getY();
                double z = location.getZ();

                Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "dh remove " + name);
                
                String firstLine = lines.isEmpty() ? "Hologram" : lines.get(0);
                Bukkit.dispatchCommand(Bukkit.getConsoleSender(), String.format("dh create %s %s,%.2f,%.2f,%.2f %s", name, worldName, x, y, z, firstLine));

                for (int i = 1; i < lines.size(); i++) {
                    Bukkit.dispatchCommand(Bukkit.getConsoleSender(), String.format("dh line add %s %s", name, lines.get(i)));
                }
                return;
            } catch (Exception e) {
                plugin.getLogger().warning("Error al crear holograma con DecentHolograms: " + e.getMessage());
            }
        }

        // Fallback usando ArmorStands invisibles
        spawnArmorStandHologram(location, lines);
    }

    private void spawnArmorStandHologram(Location baseLocation, List<String> lines) {
        Location loc = baseLocation.clone();
        for (int i = lines.size() - 1; i >= 0; i--) {
            String line = lines.get(i);
            loc.getWorld().spawn(loc, ArmorStand.class, as -> {
                as.setCustomName(line);
                as.setCustomNameVisible(true);
                as.setInvisible(true);
                as.setGravity(false);
                as.setMarker(true);
                as.setPersistent(true);
            });
            loc.add(0, 0.28, 0);
        }
    }
}
