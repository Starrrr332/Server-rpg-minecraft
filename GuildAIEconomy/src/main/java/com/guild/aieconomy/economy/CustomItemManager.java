package com.guild.aieconomy.economy;

import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataType;
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
                double rawBuy = config.getDouble("items." + key + ".buy_price", 25000.0);
                double buyPrice = Math.max(25000.0, rawBuy);
                double sellPrice = config.getDouble("items." + key + ".sell_price", buyPrice * 0.70);
                if (item != null) {
                    customItems.put(key, new CustomEconomyItem(key, item, buyPrice, sellPrice));
                }
            }
        }

        if (customItems.isEmpty()) {
            loadDefaultRPGItems();
        }

        plugin.getLogger().info("[GuildAIEconomy] Cargados " + customItems.size() + " ítems RPG personalizados a 25,000+ monedas/pieza.");
    }

    private void loadDefaultRPGItems() {
        addCustomItemInternal("espada_elite_dragon", createSampleItem(Material.DIAMOND_SWORD, "§6⚔️ Espada del Dragón Élite", Arrays.asList("§7Forjada con escamas de dragón legendario", "§eEfecto: Fuego II & Filo V"), Enchantment.DAMAGE_ALL, 5, Enchantment.FIRE_ASPECT, 2), 25000.0, 17500.0, false);
        addCustomItemInternal("arco_elven_legendario", createSampleItem(Material.BOW, "§a🏹 Arco Élfico Legendario", Arrays.asList("§7Bendecido por los ancianos élficos", "§eEfecto: Poder V & Inmortalidad"), Enchantment.ARROW_DAMAGE, 5, Enchantment.ARROW_INFINITE, 1), 25000.0, 17500.0, false);
        addCustomItemInternal("coraza_titan_netherita", createSampleItem(Material.NETHERITE_CHESTPLATE, "§c🛡️ Coraza del Titán", Arrays.asList("§7Forjada en el fuego primigenio del Nether", "§eEfecto: Protección IV & Irrompibilidad III"), Enchantment.PROTECTION_ENVIRONMENTAL, 4, Enchantment.DURABILITY, 3), 35000.0, 24500.0, false);
        addCustomItemInternal("pocion_vida_ancestral", createSampleItem(Material.HONEY_BOTTLE, "§b🧪 Poción de Salud Ancestral", Arrays.asList("§7Restaura la vitalidad por completo"), null, 0, null, 0), 10000.0, 7000.0, false);
        save();
    }

    private ItemStack createSampleItem(Material mat, String name, List<String> lore, Enchantment enc1, int lvl1, Enchantment enc2, int lvl2) {
        ItemStack item = new ItemStack(mat, 1);
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            meta.setDisplayName(name);
            meta.setLore(lore);
            if (enc1 != null) meta.addEnchant(enc1, lvl1, true);
            if (enc2 != null) meta.addEnchant(enc2, lvl2, true);
            item.setItemMeta(meta);
        }
        return item;
    }

    private void addCustomItemInternal(String id, ItemStack item, double buyPrice, double sellPrice, boolean autoSave) {
        if (item == null) return;
        ItemStack singleItem = item.clone();
        singleItem.setAmount(1);

        ItemMeta meta = singleItem.getItemMeta();
        if (meta != null) {
            NamespacedKey key = new NamespacedKey(plugin, "custom_item_id");
            meta.getPersistentDataContainer().set(key, PersistentDataType.STRING, id);
            singleItem.setItemMeta(meta);
        }

        config.set("items." + id + ".item", singleItem);
        config.set("items." + id + ".buy_price", buyPrice);
        config.set("items." + id + ".sell_price", sellPrice);
        if (autoSave) {
            save();
        }

        customItems.put(id, new CustomEconomyItem(id, singleItem, buyPrice, sellPrice));
    }

    public void save() {
        try {
            config.save(file);
        } catch (IOException e) {
            plugin.getLogger().severe("No se pudo guardar custom_items.yml: " + e.getMessage());
        }
    }

    public boolean addCustomItem(String id, ItemStack item, double buyPrice, double sellPrice) {
        return addCustomItem(id, item, buyPrice, sellPrice, true);
    }

    public boolean addCustomItem(String id, ItemStack item, double buyPrice, double sellPrice, boolean autoSave) {
        if (item == null) return false;
        addCustomItemInternal(id, item, buyPrice, sellPrice, autoSave);
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

    public CustomEconomyItem findCustomItem(String query) {
        if (query == null || query.isBlank()) return null;
        String clean = query.toLowerCase().replace("_", " ").trim();
        for (CustomEconomyItem item : customItems.values()) {
            if (item.getId().toLowerCase().equalsIgnoreCase(query) || item.getId().toLowerCase().contains(clean)) {
                return item;
            }
            ItemMeta meta = item.getItemStack().getItemMeta();
            if (meta != null && meta.hasDisplayName()) {
                String nameClean = ChatColor.stripColor(meta.getDisplayName()).toLowerCase();
                if (nameClean.contains(clean) || clean.contains(nameClean)) {
                    return item;
                }
            }
        }
        return null;
    }

    public boolean isSimilarCustomItem(ItemStack stack1, ItemStack stack2) {
        if (stack1 == null || stack2 == null) return false;
        if (stack1.getType() != stack2.getType()) return false;

        ItemMeta meta1 = stack1.getItemMeta();
        ItemMeta meta2 = stack2.getItemMeta();

        if (meta1 == null && meta2 == null) return true;
        if (meta1 == null || meta2 == null) return false;

        NamespacedKey key = new NamespacedKey(plugin, "custom_item_id");
        if (meta1.getPersistentDataContainer().has(key, PersistentDataType.STRING) &&
            meta2.getPersistentDataContainer().has(key, PersistentDataType.STRING)) {
            String id1 = meta1.getPersistentDataContainer().get(key, PersistentDataType.STRING);
            String id2 = meta2.getPersistentDataContainer().get(key, PersistentDataType.STRING);
            if (Objects.equals(id1, id2)) return true;
        }

        if (meta1.hasDisplayName() && meta2.hasDisplayName()) {
            return Objects.equals(meta1.getDisplayName(), meta2.getDisplayName());
        }

        return false;
    }
}
