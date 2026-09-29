package com.guild.aieconomy.economy;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.File;
import java.util.*;

public class EliteMobsHook {

    private final JavaPlugin plugin;
    private boolean eliteMobsEnabled = false;

    public EliteMobsHook(JavaPlugin plugin) {
        this.plugin = plugin;
        setupEliteMobs();
    }

    private void setupEliteMobs() {
        Plugin em = Bukkit.getPluginManager().getPlugin("EliteMobs");
        if (em != null && em.isEnabled()) {
            this.eliteMobsEnabled = true;
            plugin.getLogger().info("[GuildAIEconomy] ¡Plugin EliteMobs detectado e integrado exitosamente!");
        } else {
            plugin.getLogger().info("[GuildAIEconomy] EliteMobs no está activo actualmente, pero el escáner de archivos procesará la carpeta si existe.");
        }
    }

    public boolean isEliteMobsEnabled() {
        return eliteMobsEnabled;
    }

    public int scanAndRegisterEliteMobsItems(CustomItemManager itemManager) {
        int registeredCount = 0;
        File pluginsDir = plugin.getDataFolder().getParentFile();
        if (pluginsDir == null || !pluginsDir.exists()) return 0;

        File eliteMobsDir = new File(pluginsDir, "EliteMobs");
        if (!eliteMobsDir.exists()) {
            plugin.getLogger().info("[GuildAIEconomy] Carpeta /plugins/EliteMobs/ no encontrada todavía.");
            return 0;
        }

        List<File> ymlFiles = new ArrayList<>();
        findYmlFiles(new File(eliteMobsDir, "items"), ymlFiles);
        findYmlFiles(new File(eliteMobsDir, "customitems"), ymlFiles);
        findYmlFiles(new File(eliteMobsDir, "imports"), ymlFiles);
        findYmlFiles(new File(eliteMobsDir, "procedural_items"), ymlFiles);

        for (File yml : ymlFiles) {
            try {
                YamlConfiguration config = YamlConfiguration.loadConfiguration(yml);
                if (config.contains("isEnabled") && !config.getBoolean("isEnabled")) {
                    continue;
                }

                String id = "elitemobs_" + yml.getName().replace(".yml", "").toLowerCase();

                String rawMat = config.getString("material", config.getString("itemMaterial", config.getString("item.material", "")));
                if (rawMat.isEmpty()) continue;

                Material mat = Material.matchMaterial(rawMat.toUpperCase());
                if (mat == null || mat == Material.AIR) continue;

                String name = config.getString("name", config.getString("displayName", config.getString("item.name", "&dÍtem de EliteMobs")));
                name = ChatColor.translateAlternateColorCodes('&', name);

                List<String> rawLore = config.getStringList("lore");
                if (rawLore.isEmpty()) {
                    rawLore = config.getStringList("item.lore");
                }
                List<String> lore = new ArrayList<>();
                for (String l : rawLore) {
                    lore.add(ChatColor.translateAlternateColorCodes('&', l));
                }
                lore.add(ChatColor.DARK_PURPLE + "✧ Ítem Custom de EliteMobs");

                ItemStack item = new ItemStack(mat, 1);
                ItemMeta meta = item.getItemMeta();
                if (meta != null) {
                    meta.setDisplayName(name);
                    meta.setLore(lore);

                    if (config.contains("customModelData")) {
                        meta.setCustomModelData(config.getInt("customModelData"));
                    }

                    // Enchantments
                    List<String> enchants = config.getStringList("enchantments");
                    for (String encStr : enchants) {
                        String[] parts = encStr.split(",");
                        if (parts.length >= 2) {
                            try {
                                String encName = parts[0].trim().toLowerCase();
                                Enchantment enc = null;
                                if (encName.contains(":")) {
                                    enc = Enchantment.getByKey(NamespacedKey.fromString(encName));
                                } else {
                                    enc = Enchantment.getByKey(NamespacedKey.minecraft(encName));
                                }
                                if (enc != null) {
                                    int level = Integer.parseInt(parts[1].trim());
                                    meta.addEnchant(enc, level, true);
                                }
                            } catch (Exception ignored) {}
                        }
                    }

                    // Marca de PersistentData
                    NamespacedKey key = new NamespacedKey(plugin, "custom_item_id");
                    meta.getPersistentDataContainer().set(key, PersistentDataType.STRING, id);

                    item.setItemMeta(meta);
                }

                double buyPrice = config.getDouble("buyPrice", config.getDouble("price", 350.0));
                double sellPrice = config.getDouble("sellPrice", buyPrice * 0.7);

                if (itemManager.addCustomItem(id, item, buyPrice, sellPrice)) {
                    registeredCount++;
                }
            } catch (Exception e) {
                // Silently skip unparseable non-item files
            }
        }

        plugin.getLogger().info("[GuildAIEconomy] Escaneo completado: " + registeredCount + " ítems de EliteMobs integrados en la tienda.");
        return registeredCount;
    }

    private void findYmlFiles(File folder, List<File> result) {
        if (folder == null || !folder.exists() || !folder.isDirectory()) return;
        File[] files = folder.listFiles();
        if (files == null) return;

        for (File f : files) {
            if (f.isDirectory()) {
                findYmlFiles(f, result);
            } else if (f.getName().endsWith(".yml")) {
                result.add(f);
            }
        }
    }

    public boolean isEliteMobsItem(ItemStack item) {
        if (item == null || !item.hasItemMeta()) return false;
        ItemMeta meta = item.getItemMeta();
        NamespacedKey emKey = new NamespacedKey(plugin, "custom_item_id");
        if (meta.getPersistentDataContainer().has(emKey, PersistentDataType.STRING)) {
            String val = meta.getPersistentDataContainer().get(emKey, PersistentDataType.STRING);
            if (val != null && val.startsWith("elitemobs_")) return true;
        }
        return meta.getPersistentDataContainer().getKeys().stream()
                .anyMatch(key -> key.getNamespace().equalsIgnoreCase("elitemobs"))
                || (meta.hasDisplayName() && meta.getDisplayName().toLowerCase().contains("elitemobs"));
    }
}
