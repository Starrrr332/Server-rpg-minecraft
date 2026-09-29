package com.guild.aieconomy.npc;

import com.guild.aieconomy.GuildAIEconomy;
import com.guild.aieconomy.economy.CustomItemManager.CustomEconomyItem;
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

import java.util.HashMap;
import java.util.Map;

public class MerchantListener implements Listener {

    private final GuildAIEconomy plugin;
    private final Map<String, Material> spanishMaterialMap = new HashMap<>();

    public MerchantListener(GuildAIEconomy plugin) {
        this.plugin = plugin;
        initSpanishMaterials();
    }

    private void initSpanishMaterials() {
        spanishMaterialMap.put("diamante", Material.DIAMOND);
        spanishMaterialMap.put("oro", Material.GOLD_INGOT);
        spanishMaterialMap.put("hierro", Material.IRON_INGOT);
        spanishMaterialMap.put("esmeralda", Material.EMERALD);
        spanishMaterialMap.put("netherita", Material.NETHERITE_INGOT);
        spanishMaterialMap.put("cobre", Material.COPPER_INGOT);
        spanishMaterialMap.put("lapislazuli", Material.LAPIS_LAZULI);
        spanishMaterialMap.put("roble", Material.OAK_LOG);
        spanishMaterialMap.put("madera", Material.OAK_LOG);
        spanishMaterialMap.put("piedra", Material.STONE);
        spanishMaterialMap.put("obsidiana", Material.OBSIDIAN);
        spanishMaterialMap.put("estrella", Material.NETHER_STAR);
        spanishMaterialMap.put("elitros", Material.ELYTRA);
        spanishMaterialMap.put("elytra", Material.ELYTRA);
        spanishMaterialMap.put("manzana", Material.GOLDEN_APPLE);
        spanishMaterialMap.put("manzana dorada", Material.GOLDEN_APPLE);
        spanishMaterialMap.put("filete", Material.COOKED_BEEF);
        spanishMaterialMap.put("zanahoria", Material.GOLDEN_CARROT);
        spanishMaterialMap.put("totem", Material.TOTEM_OF_UNDYING);
    }

    @EventHandler(priority = EventPriority.HIGH)
    public void onInteractNPC(PlayerInteractEntityEvent event) {
        if (event.getHand() != EquipmentSlot.HAND) return;

        if (plugin.getMerchantVillager().isMerchantNPC(event.getRightClicked())) {
            event.setCancelled(true);
            Player player = event.getPlayer();
            
            ShopGUI gui = new ShopGUI(plugin, 1);
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

            int slot = event.getRawSlot();

            if (slot == 48 && clickedItem.getType() == Material.ARROW) {
                ShopGUI prevGui = new ShopGUI(plugin, gui.getPage() - 1);
                prevGui.open(player);
                return;
            } else if (slot == 50 && clickedItem.getType() == Material.ARROW) {
                ShopGUI nextGui = new ShopGUI(plugin, gui.getPage() + 1);
                nextGui.open(player);
                return;
            }

            Material mat = clickedItem.getType();
            ClickType click = event.getClick();

            CustomEconomyItem customMatch = null;
            for (CustomEconomyItem item : plugin.getCustomItemManager().getCustomItems()) {
                if (plugin.getCustomItemManager().isSimilarCustomItem(clickedItem, item.getItemStack())) {
                    customMatch = item;
                    break;
                }
            }

            boolean isVanilla = (customMatch == null) && plugin.getMarketEngine().getBasePrices().containsKey(mat);

            if (!isVanilla && customMatch == null) return;

            if (isVanilla) {
                int stock = plugin.getChestManager().getItemStock(mat);
                double buyPrice = plugin.getMarketEngine().calculateBuyPrice(mat, stock);
                double sellPrice = plugin.getMarketEngine().calculateSellPrice(mat, stock);

                if (click.isLeftClick()) {
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
                        plugin.getVaultHook().deposit(player, buyPrice);
                        player.sendMessage("§c🤖 Mercader: Hubo un problema al retirar el ítem del cofre.");
                    }
                } else if (click.isRightClick()) {
                    if (!player.getInventory().containsAtLeast(new ItemStack(mat), 1)) {
                        player.sendMessage("§c🤖 Mercader: ¡No tienes este ítem en tu inventario para vender!");
                        return;
                    }

                    if (plugin.getChestManager().addItemToStock(mat, 1)) {
                        player.getInventory().removeItem(new ItemStack(mat, 1));
                        plugin.getVaultHook().deposit(player, sellPrice);
                        plugin.getMarketEngine().registerDemand(mat, -1);
                        player.sendMessage("§a🤖 Mercader: ¡Has vendido 1x " + mat.name() + " por " + plugin.getVaultHook().format(sellPrice) + "!");
                    } else {
                        player.sendMessage("§c🤖 Mercader: ¡Mi cofre de economía está lleno!");
                    }
                }
            } else {
                ItemStack targetStack = customMatch.getItemStack();
                double buyPrice = customMatch.getBuyPrice();
                double sellPrice = customMatch.getSellPrice();

                if (click.isLeftClick()) {
                    if (!plugin.getVaultHook().withdraw(player, buyPrice)) {
                        player.sendMessage("§c🤖 Mercader: ¡No tienes suficiente dinero! Cuesta " + plugin.getVaultHook().format(buyPrice));
                        return;
                    }
                    player.getInventory().addItem(targetStack.clone());
                    player.sendMessage("§a🤖 Mercader: ¡Has comprado 1x " + customMatch.getId() + " por " + plugin.getVaultHook().format(buyPrice) + "!");
                } else if (click.isRightClick()) {
                    boolean found = false;
                    for (ItemStack invItem : player.getInventory().getContents()) {
                        if (invItem != null && plugin.getCustomItemManager().isSimilarCustomItem(invItem, targetStack)) {
                            invItem.setAmount(invItem.getAmount() - 1);
                            plugin.getVaultHook().deposit(player, sellPrice);
                            player.sendMessage("§a🤖 Mercader: ¡Has vendido 1x " + customMatch.getId() + " por " + plugin.getVaultHook().format(sellPrice) + "!");
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        player.sendMessage("§c🤖 Mercader: ¡No tienes este ítem personalizado en tu inventario para vender!");
                    }
                }
            }

            gui.setupItems();
        }
    }

    @EventHandler(priority = EventPriority.NORMAL)
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        String msg = event.getMessage().trim();
        String lowerMsg = msg.toLowerCase();
        
        if (lowerMsg.startsWith("!bot") || lowerMsg.startsWith("@bot") || lowerMsg.startsWith("bot") || lowerMsg.startsWith("vendedor") || lowerMsg.startsWith("mercader")) {
            String promptText = msg.replaceFirst("(?i)^(!bot|@bot|bot|vendedor|mercader)\\s*", "").trim();
            if (promptText.isEmpty()) {
                promptText = "Hola";
            }
            Player player = event.getPlayer();

            boolean isBuyIntent = lowerMsg.contains("compr") || lowerMsg.contains("quiero") || lowerMsg.contains("dame");
            boolean isSellIntent = lowerMsg.contains("vend") || lowerMsg.contains("te doy");

            CustomEconomyItem matchedCustom = plugin.getCustomItemManager().findCustomItem(promptText);

            Material targetMat = null;
            for (Map.Entry<String, Material> entry : spanishMaterialMap.entrySet()) {
                if (lowerMsg.contains(entry.getKey())) {
                    targetMat = entry.getValue();
                    break;
                }
            }

            if ((matchedCustom != null || targetMat != null) && (isBuyIntent || isSellIntent)) {
                final CustomEconomyItem customItem = matchedCustom;
                final Material mat = targetMat;
                final boolean buy = isBuyIntent;

                Bukkit.getScheduler().runTask(plugin, () -> {
                    if (customItem != null) {
                        double buyPrice = customItem.getBuyPrice();
                        double sellPrice = customItem.getSellPrice();

                        if (buy) {
                            if (!plugin.getVaultHook().withdraw(player, buyPrice)) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Uy " + player.getName() + "! El ítem " + customItem.getId() + " cuesta " + plugin.getVaultHook().format(buyPrice) + ", pero no tienes suficiente dinero.");
                                return;
                            }
                            player.getInventory().addItem(customItem.getItemStack());
                            Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Trato hecho, " + player.getName() + "! Te he entregado 1x " + customItem.getId() + " por " + plugin.getVaultHook().format(buyPrice) + ".");
                        } else {
                            boolean found = false;
                            for (ItemStack invItem : player.getInventory().getContents()) {
                                if (invItem != null && plugin.getCustomItemManager().isSimilarCustomItem(invItem, customItem.getItemStack())) {
                                    invItem.setAmount(invItem.getAmount() - 1);
                                    plugin.getVaultHook().deposit(player, sellPrice);
                                    Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Excelente negocio, " + player.getName() + "! Te he comprado 1x " + customItem.getId() + " por " + plugin.getVaultHook().format(sellPrice) + ".");
                                    found = true;
                                    break;
                                }
                            }
                            if (!found) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡" + player.getName() + ", parece que no tienes ese ítem personalizado en tu inventario!");
                            }
                        }
                    } else {
                        int stock = plugin.getChestManager().getItemStock(mat);
                        if (buy) {
                            double price = plugin.getMarketEngine().calculateBuyPrice(mat, stock);
                            if (stock <= 0) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Hola " + player.getName() + "! Por el momento no tengo stock de " + mat.name() + " en mi cofre.");
                                return;
                            }
                            if (!plugin.getVaultHook().withdraw(player, price)) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Uy " + player.getName() + "! 1x " + mat.name() + " cuesta " + plugin.getVaultHook().format(price) + ", pero no tienes suficiente oro.");
                                return;
                            }

                            if (plugin.getChestManager().removeItemFromStock(mat, 1)) {
                                player.getInventory().addItem(new ItemStack(mat, 1));
                                plugin.getMarketEngine().registerDemand(mat, 1);
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Trato hecho, " + player.getName() + "! Te he vendido 1x " + mat.name() + " por " + plugin.getVaultHook().format(price) + ". ¡Gracias por tu compra!");
                            } else {
                                plugin.getVaultHook().deposit(player, price);
                                Bukkit.broadcastMessage("§b🤖 Mercader: §fHubo un problema con mi cofre de stock.");
                            }
                        } else {
                            double price = plugin.getMarketEngine().calculateSellPrice(mat, stock);
                            if (!player.getInventory().containsAtLeast(new ItemStack(mat), 1)) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡" + player.getName() + ", parece que no tienes 1x " + mat.name() + " en tu inventario para vendérmelo!");
                                return;
                            }

                            if (plugin.getChestManager().addItemToStock(mat, 1)) {
                                player.getInventory().removeItem(new ItemStack(mat, 1));
                                plugin.getVaultHook().deposit(player, price);
                                plugin.getMarketEngine().registerDemand(mat, -1);
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Excelente trato, " + player.getName() + "! Me he quedado con tu 1x " + mat.name() + " y te he entregado " + plugin.getVaultHook().format(price) + ".");
                            } else {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡Mi cofre de economía está lleno por ahora!");
                            }
                        }
                    }
                });
                return;
            }

            player.sendMessage("§b🤖 Mercader (" + player.getName() + "): §7Pensando...");

            String systemPrompt = plugin.getConfig().getString("gemini.system_prompt", "Eres Gilderbot, el amigable y libre conversador mercader del gremio.");
            
            plugin.getGeminiClient().askMerchant(systemPrompt, promptText).thenAccept(reply -> {
                Bukkit.getScheduler().runTask(plugin, () -> {
                    Bukkit.broadcastMessage("§b🤖 Mercader: §f" + ChatColor.translateAlternateColorCodes('&', reply));
                });
            });
        }
    }
}
