package com.guild.aieconomy.npc;

import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.NamespacedKey;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Villager;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.java.JavaPlugin;

public class MerchantVillager {

    private final JavaPlugin plugin;
    private final NamespacedKey npcKey;

    public MerchantVillager(JavaPlugin plugin) {
        this.plugin = plugin;
        this.npcKey = new NamespacedKey(plugin, "guild_ai_merchant");
    }

    public NamespacedKey getNpcKey() {
        return npcKey;
    }

    public Villager spawnMerchant(Location location, String customName, String professionName) {
        if (location == null || location.getWorld() == null) return null;

        return location.getWorld().spawn(location, Villager.class, villager -> {
            String name = (customName != null && !customName.isBlank()) 
                    ? ChatColor.translateAlternateColorCodes('&', customName)
                    : "§b🤖 [IA] Mercader del Gremio";

            villager.setCustomName(name);
            villager.setCustomNameVisible(true);
            
            Villager.Profession profession = Villager.Profession.LIBRARIAN;
            try {
                if (professionName != null) {
                    profession = Villager.Profession.valueOf(professionName.toUpperCase());
                }
            } catch (IllegalArgumentException ignored) {}
            
            villager.setProfession(profession);
            villager.setVillagerType(Villager.Type.PLAINS);
            villager.setAI(false);
            villager.setRemoveWhenFarAway(false);
            villager.setPersistent(true);
            villager.setInvulnerable(true);
            villager.setCollidable(false);

            villager.getPersistentDataContainer().set(npcKey, PersistentDataType.STRING, "guild_ai_bot");
        });
    }

    public boolean isMerchantNPC(Entity entity) {
        if (entity instanceof Villager villager) {
            return villager.getPersistentDataContainer().has(npcKey, PersistentDataType.STRING);
        }
        return false;
    }
}
