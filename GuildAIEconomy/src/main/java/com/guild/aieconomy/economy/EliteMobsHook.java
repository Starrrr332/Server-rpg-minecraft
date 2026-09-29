package com.guild.aieconomy.economy;

import org.bukkit.Bukkit;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.java.JavaPlugin;

public class EliteMobsHook {

    private boolean eliteMobsEnabled = false;

    public EliteMobsHook(JavaPlugin plugin) {
        setupEliteMobs();
    }

    private void setupEliteMobs() {
        Plugin em = Bukkit.getPluginManager().getPlugin("EliteMobs");
        if (em != null && em.isEnabled()) {
            this.eliteMobsEnabled = true;
            Bukkit.getLogger().info("[GuildAIEconomy] ¡Plugin EliteMobs detectado e integrado exitosamente!");
        }
    }

    public boolean isEliteMobsEnabled() {
        return eliteMobsEnabled;
    }

    public boolean isEliteMobsItem(ItemStack item) {
        if (!eliteMobsEnabled || item == null || !item.hasItemMeta()) return false;
        return item.getItemMeta().getPersistentDataContainer().getKeys().stream()
                .anyMatch(key -> key.getNamespace().equalsIgnoreCase("elitemobs"))
                || (item.getItemMeta().hasDisplayName() && item.getItemMeta().getDisplayName().toLowerCase().contains("elitemobs"));
    }
}
