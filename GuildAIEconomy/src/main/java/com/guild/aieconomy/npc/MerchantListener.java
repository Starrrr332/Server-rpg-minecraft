package com.guild.aieconomy.npc;

import com.guild.aieconomy.GuildAIEconomy;
import com.guild.aieconomy.gui.ShopGUI;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.ClickType;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.event.player.PlayerInteractEntityEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;

public class MerchantListener implements Listener {

    private final GuildAIEconomy plugin;

    public MerchantListener(GuildAIEconomy plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.HIGH)
    public void onInteractNPC(PlayerInteractEntityEvent event) {
        if (event.getHand() != EquipmentSlot.HAND) return;

        if (plugin.getMerchantVillager().isMerchantNPC(event.getRightClicked())) {
            event.setCancelled(true);
            Player player = event.getPlayer();
            
            // Abre la GUI de Tienda
            ShopGUI gui = new ShopGUI(plugin);
            gui.open(player);
        }
    }

    @EventHandler(priority = EventPriority.HIGH)
    public void onShopClick(InventoryClickEvent event) {
        if (event.getInventory().getHolder() instanceof ShopGUI gui) {
            event.setCancelled(true);
            
            if (!(event.getWhoClicked() instanceof Player player)) return;
            ItemStack clickedItem = event.getCurrentItem();
            if (clickedItem == null || clickedItem.getType() == Material.AIR) return;

            Material mat = clickedItem.getType();
            if (!plugin.getMarketEngine().getBasePrices().containsKey(mat)) return;

            int stock = plugin.getChestManager().getItemStock(mat);
            double buyPrice = plugin.getMarketEngine().calculateBuyPrice(mat, stock);
            double sellPrice = plugin.getMarketEngine().calculateSellPrice(mat, stock);

            ClickType click = event.getClick();

            if (click.isLeftClick()) {
                // COMPRAR 1 ÍTEM
                if (stock <= 0) {
                    player.sendMessage("§c🤖 Mercader: ¡No me queda stock de ese material en mi cofre!");
                    return;
                }
                if (!plugin.getVaultHook().withdraw(player, buyPrice)) {
                    player.sendMessage("§c🤖 Mercader: ¡No tienes suficiente dinero! Cuesta " + plugin.getVaultHook().format(buyPrice));
                    return;
                }

                if (plugin.getChestManager().removeItemFromStock(mat, 1)) {
                    player.getInventory().addItem(new ItemStack(mat, 1));
                    plugin.getMarketEngine().registerDemand(mat, 1);
                    player.sendMessage("§a🤖 Mercader: ¡Has comprado 1x " + mat.name() + " por " + plugin.getVaultHook().format(buyPrice) + "!");
                } else {
                    plugin.getVaultHook().deposit(player, buyPrice); // Reembolso de seguridad
                    player.sendMessage("§c🤖 Mercader: Hubo un problema al retirar el ítem del cofre.");
                }
            } else if (click.isRightClick()) {
                // VENDER 1 ÍTEM
                if (!player.getInventory().containsAtLeast(new ItemStack(mat), 1)) {
                    player.sendMessage("§c🤖 Mercader: ¡No tienes este ítem en tu inventario para vender!");
                    return;
                }

                // Intentar añadir al cofre primero
                if (plugin.getChestManager().addItemToStock(mat, 1)) {
                    player.getInventory().removeItem(new ItemStack(mat, 1));
                    plugin.getVaultHook().deposit(player, sellPrice);
                    plugin.getMarketEngine().registerDemand(mat, -1);
                    player.sendMessage("§a🤖 Mercader: ¡Has vendido 1x " + mat.name() + " por " + plugin.getVaultHook().format(sellPrice) + "!");
                } else {
                    player.sendMessage("§c🤖 Mercader: ¡Mi cofre de economía está lleno y no puedo almacenar más ítems!");
                }
            }

            // Actualizar vista de GUI
            gui.setupItems();
        }
    }

    @EventHandler(priority = EventPriority.NORMAL)
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        String msg = event.getMessage().trim();
        String lowerMsg = msg.toLowerCase();
        
        if (lowerMsg.startsWith("!bot") || lowerMsg.startsWith("vendedor") || lowerMsg.startsWith("mercader")) {
            String promptText = msg.replaceFirst("(?i)^(!bot|vendedor|mercader)\\s*", "").trim();
            if (promptText.isEmpty()) {
                promptText = "Hola, ¿cuáles son tus ofertas?";
            }
            Player player = event.getPlayer();

            player.sendMessage("§b🤖 Mercader (" + player.getName() + "): §7Pensando...");

            String systemPrompt = plugin.getConfig().getString("gemini.system_prompt", "Eres Gilderbot, el mercader del gremio.");
            
            plugin.getGeminiClient().askMerchant(systemPrompt, promptText).thenAccept(reply -> {
                Bukkit.getScheduler().runTask(plugin, () -> {
                    Bukkit.broadcastMessage("§b🤖 Mercader: §f" + ChatColor.translateAlternateColorCodes('&', reply));
                });
            });
        }
    }
}
