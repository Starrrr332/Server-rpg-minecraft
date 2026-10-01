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
    private final NamespacedKey typeKey;

    public MerchantVillager(JavaPlugin plugin) {
        this.plugin = plugin;
        this.npcKey = new NamespacedKey(plugin, "guild_ai_merchant");
        this.typeKey = new NamespacedKey(plugin, "guild_ai_type");
    }

    public NamespacedKey getNpcKey() {
        return npcKey;
    }

    public Villager spawnMerchant(Location location, String customName, String professionName, String merchantType) {
        if (location == null || location.getWorld() == null) return null;

        final String type = (merchantType != null && merchantType.equalsIgnoreCase("custom")) ? "custom" : "vanilla";

        return location.getWorld().spawn(location, Villager.class, villager -> {
            String defaultName = "custom".equals(type)
                    ? "§d⚔️ [IA] Mercader RPG & EliteMobs"
                    : "§b🧱 [IA] Mercader Vanilla";

            String name = (customName != null && !customName.isBlank()) 
                    ? ChatColor.translateAlternateColorCodes('&', customName)
                    : defaultName;

            villager.setCustomName(name);
            villager.setCustomNameVisible(true);
            
            Villager.Profession profession = "custom".equals(type)
                    ? Villager.Profession.WEAPONSMITH
                    : Villager.Profession.LIBRARIAN;

            try {
                if (professionName != null && !professionName.isBlank()) {
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
            villager.getPersistentDataContainer().set(typeKey, PersistentDataType.STRING, type);
        });
    }

    public boolean isMerchantNPC(Entity entity) {
        if (entity instanceof Villager villager) {
            return villager.getPersistentDataContainer().has(npcKey, PersistentDataType.STRING);
        }
        return false;
    }

    public String getMerchantType(Entity entity) {
        if (entity instanceof Villager villager) {
            if (villager.getPersistentDataContainer().has(typeKey, PersistentDataType.STRING)) {
                return villager.getPersistentDataContainer().get(typeKey, PersistentDataType.STRING);
            }
            if (villager.getCustomName() != null) {
                String nameLower = villager.getCustomName().toLowerCase();
                if (nameLower.contains("rpg") || nameLower.contains("custom") || nameLower.contains("elitemobs")) {
                    return "custom";
                }
            }
        }
        return "vanilla";
    }
}
