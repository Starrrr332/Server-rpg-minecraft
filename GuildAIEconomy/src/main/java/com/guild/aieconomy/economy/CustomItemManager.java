package com.guild.aieconomy.economy;

import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class CustomItemManager {

    public static class CustomEconomyItem {
        private final String id;
        private final ItemStack itemStack;
        private final double buyPrice;
        private final double sellPrice;

        public CustomEconomyItem(String id, ItemStack itemStack, double buyPrice, double sellPrice) {
            this.id = id;
            this.itemStack = itemStack;
            this.buyPrice = buyPrice;
            this.sellPrice = sellPrice;
        }

        public String getId() {
            return id;
        }

        public ItemStack getItemStack() {
            return itemStack.clone();
        }

        public double getBuyPrice() {
            return buyPrice;
        }

        public double getSellPrice() {
            return sellPrice;
        }
    }

    private final JavaPlugin plugin;
    private final File file;
    private FileConfiguration config;
    private final Map<String, CustomEconomyItem> customItems = new LinkedHashMap<>();

    public CustomItemManager(JavaPlugin plugin) {
        this.plugin = plugin;
        this.file = new File(plugin.getDataFolder(), "custom_items.yml");
        load();
    }

    public void load() {
        if (!file.exists()) {
            try {
                plugin.getDataFolder().mkdirs();
                file.createNewFile();
            } catch (IOException e) {
                plugin.getLogger().severe("No se pudo crear custom_items.yml: " + e.getMessage());
            }
        }
        config = YamlConfiguration.loadConfiguration(file);
        customItems.clear();

        if (config.isConfigurationSection("items")) {
            for (String key : config.getConfigurationSection("items").getKeys(false)) {
                ItemStack item = config.getItemStack("items." + key + ".item");
                double buyPrice = config.getDouble("items." + key + ".buy_price", 100.0);
                double sellPrice = config.getDouble("items." + key + ".sell_price", 70.0);
                if (item != null) {
                    customItems.put(key, new CustomEconomyItem(key, item, buyPrice, sellPrice));
                }
            }
        }
        plugin.getLogger().info("[GuildAIEconomy] Cargados " + customItems.size() + " ítems personalizados para la economía.");
    }

    public void save() {
        try {
            config.save(file);
        } catch (IOException e) {
            plugin.getLogger().severe("No se pudo guardar custom_items.yml: " + e.getMessage());
        }
    }

    public boolean addCustomItem(String id, ItemStack item, double buyPrice, double sellPrice) {
        if (item == null) return false;
        ItemStack singleItem = item.clone();
        singleItem.setAmount(1);

        config.set("items." + id + ".item", singleItem);
        config.set("items." + id + ".buy_price", buyPrice);
        config.set("items." + id + ".sell_price", sellPrice);
        save();

        customItems.put(id, new CustomEconomyItem(id, singleItem, buyPrice, sellPrice));
        return true;
    }

    public boolean removeCustomItem(String id) {
        if (config.contains("items." + id)) {
            config.set("items." + id, null);
            save();
            customItems.remove(id);
            return true;
        }
        return false;
    }

    public Collection<CustomEconomyItem> getCustomItems() {
        return customItems.values();
    }

    public CustomEconomyItem getById(String id) {
        return customItems.get(id);
    }

    public boolean isSimilarCustomItem(ItemStack stack1, ItemStack stack2) {
        if (stack1 == null || stack2 == null) return false;
        if (stack1.getType() != stack2.getType()) return false;
        
        ItemMeta meta1 = stack1.getItemMeta();
        ItemMeta meta2 = stack2.getItemMeta();

        if (meta1 == null && meta2 == null) return true;
        if (meta1 == null || meta2 == null) return false;

        boolean nameMatch = Objects.equals(meta1.getDisplayName(), meta2.getDisplayName());
        boolean loreMatch = Objects.equals(meta1.getLore(), meta2.getLore());

        return nameMatch && loreMatch;
    }
}
