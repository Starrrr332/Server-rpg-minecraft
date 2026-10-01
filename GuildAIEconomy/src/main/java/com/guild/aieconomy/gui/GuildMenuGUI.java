package com.guild.aieconomy.gui;

import com.guild.aieconomy.GuildAIEconomy;
import com.guild.aieconomy.gui.ShopGUI.ShopType;
import com.guild.aieconomy.ranks.GuildRankManager.PlayerGuildData;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GuildMenuGUI implements InventoryHolder {

    private final GuildAIEconomy plugin;
    private final Inventory inventory;

    public GuildMenuGUI(GuildAIEconomy plugin, Player player) {
        this.plugin = plugin;
        this.inventory = Bukkit.createInventory(this, 27, "§8🏰 Gremio de Aventureros - Menú");
        setupItems(player);
    }

    private void setupItems(Player player) {
        inventory.clear();

        // Cristal decorativo
        ItemStack glass = createGuiItem(Material.BLUE_STAINED_GLASS_PANE, " ", null);
        for (int i = 0; i < 27; i++) {
            inventory.setItem(i, glass);
        }

        // 1. Tienda Vanilla (Slot 10)
        List<String> vanillaLore = Arrays.asList(
                "§7Comprar y vender bloques e ítems generales.",
                "§7Precios ajustados por oferta y demanda.",
                "",
                "§a▶ Clic para abrir Tienda Vanilla"
        );
        inventory.setItem(10, createGuiItem(Material.CHEST, "§b🧱 Tienda Vanilla (Comercio)", vanillaLore));

        // 2. Tienda Custom RPG (Slot 12)
        List<String> customLore = Arrays.asList(
                "§7Armas, Armaduras y Artefactos de EliteMobs.",
                "§7Precios base: §e25,000+ monedas",
                "",
                "§d▶ Clic para abrir Tienda RPG & Élite"
        );
        inventory.setItem(12, createGuiItem(Material.NETHERITE_SWORD, "§d⚔️ Tienda Custom RPG", customLore));

        // 3. Progreso de Rango del Jugador (Slot 14)
        PlayerGuildData data = plugin.getRankManager().getPlayerData(player);
        List<String> rankLore = new ArrayList<>();
        rankLore.add("§7Rango Actual: " + data.getRank().getDisplayName());
        rankLore.add("§7EXP Acumulada: §e" + data.getExp() + " Puntos");
        rankLore.add("§7Descuento Impuestos: §a" + data.getRank().getShopDiscountPercent() + "%");
        rankLore.add("");
        rankLore.add("§7Progreso: " + plugin.getRankManager().getRankProgressFormatted(player));
        rankLore.add("");
        rankLore.add("§e▶ Completa cacerías para subir de Rango");
        inventory.setItem(14, createGuiItem(Material.GOLDEN_HELMET, "§a🏆 Tu Rango en el Gremio", rankLore));

        // 4. Teletransporte al Gremio (Slot 16)
        List<String> tpLore = Arrays.asList(
                "§7Viaja al Salón Principal del Gremio",
                "§7(Mundo em_adventurers_guild)",
                "",
                "§e▶ Clic para Teletransportarse"
        );
        inventory.setItem(16, createGuiItem(Material.COMPASS, "§6📍 Teletransporte al Gremio", tpLore));
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

    public void open(Player player) {
        player.openInventory(inventory);
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }
}
