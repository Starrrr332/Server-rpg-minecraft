package com.guild.aieconomy.gui;

import com.guild.aieconomy.GuildAIEconomy;
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

    public ShopGUI(GuildAIEconomy plugin) {
        this.plugin = plugin;
        this.inventory = Bukkit.createInventory(this, 54, "§8🤖 Tienda del Gremio (IA)");
        setupItems();
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

        // Ítems a la venta
        Map<Material, Double> items = plugin.getMarketEngine().getBasePrices();
        int slot = 10;
        for (Map.Entry<Material, Double> entry : items.entrySet()) {
            Material material = entry.getKey();
            int currentStock = plugin.getChestManager().getItemStock(material);
            double buyPrice = plugin.getMarketEngine().calculateBuyPrice(material, currentStock);
            double sellPrice = plugin.getMarketEngine().calculateSellPrice(material, currentStock);
            String trend = plugin.getMarketEngine().getTrendIndicator(material, currentStock);

            List<String> lore = new ArrayList<>();
            lore.add("§7-----------------------------");
            lore.add("§7Stock disponible: §e" + currentStock + " unidades");
            lore.add("§7Tendencia Mercado: " + trend);
            lore.add("");
            lore.add("§a▶ Clic Izquierdo: §fComprar 1 x " + plugin.getVaultHook().format(buyPrice));
            lore.add("§c▶ Clic Derecho: §fVender 1 x " + plugin.getVaultHook().format(sellPrice));
            lore.add("§7-----------------------------");

            String itemName = "§b" + formatMaterialName(material);
            inventory.setItem(slot, createGuiItem(material, itemName, lore));

            slot++;
            if ((slot % 9) == 8) {
                slot += 2;
            }
            if (slot >= 44) break;
        }

        // Información extra en el slot 49
        List<String> infoLore = new ArrayList<>();
        infoLore.add("§7Impuesto del Gremio: §a" + plugin.getMarketEngine().getGuildTaxPercent() + "%");
        infoLore.add("§7Los precios cambian dinámicamente según");
        infoLore.add("§7el stock del cofre y la oferta/demanda.");
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
}
