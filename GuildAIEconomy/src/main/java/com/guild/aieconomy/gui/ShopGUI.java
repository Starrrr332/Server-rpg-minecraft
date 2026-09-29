package com.guild.aieconomy.gui;

import com.guild.aieconomy.GuildAIEconomy;
import com.guild.aieconomy.economy.CustomItemManager.CustomEconomyItem;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ShopGUI implements InventoryHolder {

    private final GuildAIEconomy plugin;
    private final Inventory inventory;
    private final int page;

    public ShopGUI(GuildAIEconomy plugin, int page) {
        this.plugin = plugin;
        this.page = Math.max(1, page);
        this.inventory = Bukkit.createInventory(this, 54, "§8🤖 Tienda del Gremio - Pág " + this.page);
        setupItems();
    }

    public int getPage() {
        return page;
    }

    public void setupItems() {
        inventory.clear();

        // Decoración bordes con cristales
        ItemStack glassBorder = createGuiItem(Material.GRAY_STAINED_GLASS_PANE, " ", null);
        for (int i = 0; i < 9; i++) {
            inventory.setItem(i, glassBorder);
            inventory.setItem(45 + i, glassBorder);
        }
        for (int i = 9; i <= 36; i += 9) {
            inventory.setItem(i, glassBorder);
            inventory.setItem(i + 8, glassBorder);
        }

        // Ítems combinados: Vanilla + Custom (EliteMobs)
        List<ShopEntry> entries = new ArrayList<>();

        // Vanilla
        for (Map.Entry<Material, Double> entry : plugin.getMarketEngine().getBasePrices().entrySet()) {
            entries.add(new ShopEntry(entry.getKey(), null));
        }

        // Custom Items
        for (CustomEconomyItem customItem : plugin.getCustomItemManager().getCustomItems()) {
            entries.add(new ShopEntry(null, customItem));
        }

        int itemsPerPage = 28;
        int totalPages = (int) Math.ceil((double) entries.size() / itemsPerPage);
        if (totalPages < 1) totalPages = 1;

        int startIndex = (page - 1) * itemsPerPage;
        int endIndex = Math.min(startIndex + itemsPerPage, entries.size());

        int slot = 10;
        for (int i = startIndex; i < endIndex; i++) {
            ShopEntry entry = entries.get(i);
            if (entry.isVanilla()) {
                Material material = entry.material;
                int currentStock = plugin.getChestManager().getItemStock(material);
                double buyPrice = plugin.getMarketEngine().calculateBuyPrice(material, currentStock);
                double sellPrice = plugin.getMarketEngine().calculateSellPrice(material, currentStock);
                String trend = plugin.getMarketEngine().getTrendIndicator(material, currentStock);

                List<String> lore = new ArrayList<>();
                lore.add("§7-----------------------------");
                lore.add("§7Tipo: §eVanilla");
                lore.add("§7Stock disponible: §e" + currentStock + " unidades");
                lore.add("§7Tendencia Mercado: " + trend);
                lore.add("");
                lore.add("§a▶ Clic Izquierdo: §fComprar 1 x " + plugin.getVaultHook().format(buyPrice));
                lore.add("§c▶ Clic Derecho: §fVender 1 x " + plugin.getVaultHook().format(sellPrice));
                lore.add("§7-----------------------------");

                inventory.setItem(slot, createGuiItem(material, "§b" + formatMaterialName(material), lore));
            } else {
                CustomEconomyItem custom = entry.customItem;
                ItemStack baseItem = custom.getItemStack();
                int currentStock = plugin.getChestManager().getItemStock(baseItem.getType());
                double buyPrice = custom.getBuyPrice();
                double sellPrice = custom.getSellPrice();

                ItemMeta meta = baseItem.getItemMeta();
                List<String> lore = (meta != null && meta.hasLore()) ? new ArrayList<>(meta.getLore()) : new ArrayList<>();
                lore.add("§7-----------------------------");
                lore.add("§7Tipo: §dCustom / RPG (EliteMobs)");
                lore.add("§7Stock disponible: §e" + currentStock + " unidades");
                lore.add("");
                lore.add("§a▶ Clic Izquierdo: §fComprar 1 x " + plugin.getVaultHook().format(buyPrice));
                lore.add("§c▶ Clic Derecho: §fVender 1 x " + plugin.getVaultHook().format(sellPrice));
                lore.add("§7-----------------------------");

                String name = (meta != null && meta.hasDisplayName()) ? meta.getDisplayName() : "§d" + formatMaterialName(baseItem.getType());
                
                ItemStack guiStack = baseItem.clone();
                ItemMeta guiMeta = guiStack.getItemMeta();
                if (guiMeta != null) {
                    guiMeta.setDisplayName(name);
                    guiMeta.setLore(lore);
                    guiStack.setItemMeta(guiMeta);
                }
                inventory.setItem(slot, guiStack);
            }

            slot++;
            if ((slot % 9) == 8) {
                slot += 2;
            }
        }

        // Botones navegación de páginas
        if (page > 1) {
            inventory.setItem(48, createGuiItem(Material.ARROW, "§a⬅️ Página Anterior (" + (page - 1) + ")", null));
        }
        if (page < totalPages) {
            inventory.setItem(50, createGuiItem(Material.ARROW, "§a➡️ Página Siguiente (" + (page + 1) + ")", null));
        }

        // Información extra en el slot 49
        List<String> infoLore = new ArrayList<>();
        infoLore.add("§7Página §e" + page + " §7de §e" + totalPages);
        infoLore.add("§7Ítems totales: §a" + entries.size());
        infoLore.add("§7Impuesto del Gremio: §a" + plugin.getMarketEngine().getGuildTaxPercent() + "%");
        inventory.setItem(49, createGuiItem(Material.BOOK, "§e📊 Información Económica", infoLore));
    }

    private ItemStack createGuiItem(Material material, String name, List<String> lore) {
        ItemStack item = new ItemStack(material);
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            meta.setDisplayName(name);
            if (lore != null) meta.setLore(lore);
            item.setItemMeta(meta);
        }
        return item;
    }

    private String formatMaterialName(Material material) {
        String name = material.name().replace("_", " ").toLowerCase();
        String[] words = name.split(" ");
        StringBuilder sb = new StringBuilder();
        for (String w : words) {
            if (!w.isEmpty()) {
                sb.append(Character.toUpperCase(w.charAt(0))).append(w.substring(1)).append(" ");
            }
        }
        return sb.toString().trim();
    }

    public void open(Player player) {
        setupItems();
        player.openInventory(inventory);
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }

    public static class ShopEntry {
        public final Material material;
        public final CustomEconomyItem customItem;

        public ShopEntry(Material material, CustomEconomyItem customItem) {
            this.material = material;
            this.customItem = customItem;
        }

        public boolean isVanilla() {
            return material != null;
        }
    }
}
