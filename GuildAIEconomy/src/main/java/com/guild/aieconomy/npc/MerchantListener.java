package com.guild.aieconomy.npc;

import com.guild.aieconomy.GuildAIEconomy;
import com.guild.aieconomy.economy.CustomItemManager.CustomEconomyItem;
import com.guild.aieconomy.gui.GuildMenuGUI;
import com.guild.aieconomy.gui.ShopGUI;
import com.guild.aieconomy.gui.ShopGUI.ShopType;
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
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
            
            String merchantType = plugin.getMerchantVillager().getMerchantType(event.getRightClicked());
            if ("cacerias".equalsIgnoreCase(merchantType) || "quests".equalsIgnoreCase(merchantType)) {
                player.performCommand("em quests");
            } else if ("comandante".equalsIgnoreCase(merchantType) || "ranks".equalsIgnoreCase(merchantType)) {
                GuildMenuGUI menu = new GuildMenuGUI(plugin, player);
                menu.open(player);
            } else {
                ShopType shopType = "custom".equalsIgnoreCase(merchantType) ? ShopType.CUSTOM_RPG : ShopType.VANILLA;
                ShopGUI gui = new ShopGUI(plugin, shopType, 1);
                gui.open(player);
            }
        }
    }

    @EventHandler(priority = EventPriority.HIGH)
    public void onShopClick(InventoryClickEvent event) {
        if (event.getInventory().getHolder() instanceof com.guild.aieconomy.gui.GuildMenuGUI) {
            event.setCancelled(true);
            if (!(event.getWhoClicked() instanceof Player player)) return;

            int slot = event.getRawSlot();
            if (slot == 10) {
                ShopGUI gui = new ShopGUI(plugin, ShopType.VANILLA, 1);
                gui.open(player);
            } else if (slot == 12) {
                ShopGUI gui = new ShopGUI(plugin, ShopType.CUSTOM_RPG, 1);
                gui.open(player);
            } else if (slot == 14) {
                player.sendMessage("§a[Gremio] Tu Rango actual es: " + plugin.getRankManager().getPlayerData(player).getRank().getDisplayName());
                player.sendMessage("§eProgreso: " + plugin.getRankManager().getRankProgressFormatted(player));
            } else if (slot == 16) {
                org.bukkit.World gWorld = Bukkit.getWorld("em_adventurers_guild");
                if (gWorld != null) {
                    player.teleport(new org.bukkit.Location(gWorld, 308.5, 78.0, 212.5));
                    player.sendMessage("§a[Gremio] ¡Teletransportado al Salón Principal del Gremio de Aventureros!");
                } else {
                    player.sendMessage("§cEl mundo del Gremio no está cargado.");
                }
            }
            return;
        }

        if (event.getInventory().getHolder() instanceof ShopGUI gui) {
            event.setCancelled(true);
            
            if (!(event.getWhoClicked() instanceof Player player)) return;
            ItemStack clickedItem = event.getCurrentItem();
            if (clickedItem == null || clickedItem.getType() == Material.AIR) return;

            int slot = event.getRawSlot();

            if (slot == 48 && clickedItem.getType() == Material.ARROW) {
                ShopGUI prevGui = new ShopGUI(plugin, gui.getShopType(), gui.getPage() - 1);
                prevGui.open(player);
                return;
            } else if (slot == 50 && clickedItem.getType() == Material.ARROW) {
                ShopGUI nextGui = new ShopGUI(plugin, gui.getShopType(), gui.getPage() + 1);
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
        
        if (lowerMsg.startsWith("!bot") || lowerMsg.startsWith("@bot") || lowerMsg.startsWith("bot") || lowerMsg.startsWith("vendedor") || lowerMsg.startsWith("mercader") || lowerMsg.startsWith("merchant")) {
            String promptText = msg.replaceFirst("(?i)^(!bot|@bot|bot|vendedor|mercader|merchant)\\s*", "").trim();
            if (promptText.isEmpty()) {
                promptText = "Hola";
            }
            Player player = event.getPlayer();

            boolean isBuyIntent = lowerMsg.contains("compr") || lowerMsg.contains("quiero") || lowerMsg.contains("dame") ||
                                  lowerMsg.contains("buy") || lowerMsg.contains("purchase") || lowerMsg.contains("get");

            boolean isSellIntent = lowerMsg.contains("vend") || lowerMsg.contains("te doy") || lowerMsg.contains("sell");

            // Extraer Cantidad (Ej: "vender 64 diamante", "buy 16 gold ingot", "vender todo el hierro")
            int parsedAmount = 1;
            boolean isAll = lowerMsg.contains("todo") || lowerMsg.contains("toda") || lowerMsg.contains("all");

            Matcher numMatcher = Pattern.compile("\\b(\\d+)\\b").matcher(lowerMsg);
            if (numMatcher.find()) {
                try {
                    parsedAmount = Integer.parseInt(numMatcher.group(1));
                } catch (NumberFormatException ignored) {}
            }
            if (parsedAmount < 1 && !isAll) parsedAmount = 1;

            final int requestedAmount = parsedAmount;

            // Coincidencia Ítem Custom / EliteMobs
            CustomEconomyItem matchedCustom = plugin.getCustomItemManager().findCustomItem(promptText);

            // Coincidencia Ítem Vanilla Multilingüe
            Material targetMat = (matchedCustom == null) ? plugin.getItemResolver().resolveVanillaMaterial(promptText) : null;

            if ((matchedCustom != null || targetMat != null) && (isBuyIntent || isSellIntent)) {
                final CustomEconomyItem customItem = matchedCustom;
                final Material mat = targetMat;
                final boolean buy = isBuyIntent;

                Bukkit.getScheduler().runTask(plugin, () -> {
                    if (customItem != null) {
                        double unitBuy = customItem.getBuyPrice();
                        double unitSell = customItem.getSellPrice();
                        ItemStack targetStack = customItem.getItemStack();

                        if (buy) {
                            int amountToBuy = requestedAmount;
                            double totalPrice = unitBuy * amountToBuy;

                            if (!plugin.getVaultHook().withdraw(player, totalPrice)) {
                                String failMsg = "§b🤖 Mercader: §f" + player.getName() + ", " + amountToBuy + "x " + customItem.getId() + " cuestan " + plugin.getVaultHook().format(totalPrice) + ". ¡No tienes suficiente dinero!";
                                Bukkit.broadcastMessage(failMsg);
                                return;
                            }

                            int remainingToGive = amountToBuy;
                            while (remainingToGive > 0) {
                                int stackSize = Math.min(remainingToGive, targetStack.getMaxStackSize());
                                ItemStack batch = targetStack.clone();
                                batch.setAmount(stackSize);
                                player.getInventory().addItem(batch);
                                remainingToGive -= stackSize;
                            }

                            sendConversationalTradeResponse(player, "comprar", amountToBuy, customItem.getId(), totalPrice, msg);
                        } else {
                            int invCount = 0;
                            for (ItemStack is : player.getInventory().getContents()) {
                                if (is != null && plugin.getCustomItemManager().isSimilarCustomItem(is, targetStack)) {
                                    invCount += is.getAmount();
                                }
                            }

                            if (invCount <= 0) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f" + player.getName() + ", ¡no tienes ese ítem personalizado en tu inventario para vendérmelo!");
                                return;
                            }

                            int amountToSell = (isAll || requestedAmount > invCount) ? invCount : requestedAmount;
                            double totalPrice = unitSell * amountToSell;

                            int remainingToRemove = amountToSell;
                            for (ItemStack is : player.getInventory().getContents()) {
                                if (is != null && plugin.getCustomItemManager().isSimilarCustomItem(is, targetStack)) {
                                    int take = Math.min(remainingToRemove, is.getAmount());
                                    is.setAmount(is.getAmount() - take);
                                    remainingToRemove -= take;
                                    if (remainingToRemove <= 0) break;
                                }
                            }

                            plugin.getVaultHook().deposit(player, totalPrice);
                            sendConversationalTradeResponse(player, "vender", amountToSell, customItem.getId(), totalPrice, msg);
                        }
                    } else {
                        int stock = plugin.getChestManager().getItemStock(mat);
                        String itemName = plugin.getItemResolver().getItemDisplayName(mat);

                        if (buy) {
                            if (stock <= 0) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f" + player.getName() + ", sin stock de " + itemName + " en este momento.");
                                return;
                            }

                            int amountToBuy = Math.min(requestedAmount, stock);
                            double unitPrice = plugin.getMarketEngine().calculateBuyPrice(mat, stock);
                            double totalPrice = unitPrice * amountToBuy;

                            if (!plugin.getVaultHook().withdraw(player, totalPrice)) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f" + player.getName() + ", " + amountToBuy + "x " + itemName + " cuestan " + plugin.getVaultHook().format(totalPrice) + ". ¡No tienes dinero suficiente!");
                                return;
                            }

                            if (plugin.getChestManager().removeItemFromStock(mat, amountToBuy)) {
                                int remainingToGive = amountToBuy;
                                while (remainingToGive > 0) {
                                    int stackSize = Math.min(remainingToGive, mat.getMaxStackSize());
                                    player.getInventory().addItem(new ItemStack(mat, stackSize));
                                    remainingToGive -= stackSize;
                                }
                                plugin.getMarketEngine().registerDemand(mat, amountToBuy);
                                sendConversationalTradeResponse(player, "comprar", amountToBuy, itemName, totalPrice, msg);
                            } else {
                                plugin.getVaultHook().deposit(player, totalPrice);
                                Bukkit.broadcastMessage("§b🤖 Mercader: §fHubo un problema al retirar el ítem del cofre.");
                            }
                        } else {
                            int invCount = 0;
                            for (ItemStack is : player.getInventory().getContents()) {
                                if (is != null && is.getType() == mat) {
                                    invCount += is.getAmount();
                                }
                            }

                            if (invCount <= 0) {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f" + player.getName() + ", ¡no tienes " + itemName + " en tu inventario para vendérmelo!");
                                return;
                            }

                            int amountToSell = (isAll || requestedAmount > invCount) ? invCount : requestedAmount;
                            double unitPrice = plugin.getMarketEngine().calculateSellPrice(mat, stock);
                            double totalPrice = unitPrice * amountToSell;

                            if (plugin.getChestManager().addItemToStock(mat, amountToSell)) {
                                int remainingToRemove = amountToSell;
                                for (ItemStack is : player.getInventory().getContents()) {
                                    if (is != null && is.getType() == mat) {
                                        int take = Math.min(remainingToRemove, is.getAmount());
                                        is.setAmount(is.getAmount() - take);
                                        remainingToRemove -= take;
                                        if (remainingToRemove <= 0) break;
                                    }
                                }

                                plugin.getVaultHook().deposit(player, totalPrice);
                                plugin.getMarketEngine().registerDemand(mat, -amountToSell);
                                sendConversationalTradeResponse(player, "vender", amountToSell, itemName, totalPrice, msg);
                            } else {
                                Bukkit.broadcastMessage("§b🤖 Mercader: §f¡El cofre de economía está lleno por ahora!");
                            }
                        }
                    }
                });
                return;
            }

            player.sendMessage("§b🤖 Mercader (" + player.getName() + "): §7Pensando...");

            String systemPrompt = "Eres Gilderbot, el mercader comerciante del Gremio de Aventureros. Eres libre, conversacional, amigable y muy inteligente. IMPORTANTE: Responde SIEMPRE en el MISMO IDIOMA en que te hable el jugador (Español, Inglés, Portugués, Francés, etc.). Responde de forma amigable en 1 a 3 oraciones.";
            
            plugin.getGeminiClient().askMerchant(systemPrompt, msg).thenAccept(reply -> {
                Bukkit.getScheduler().runTask(plugin, () -> {
                    Bukkit.broadcastMessage("§b🤖 Mercader: §f" + ChatColor.translateAlternateColorCodes('&', reply));
                });
            });
        }
    }

    private void sendConversationalTradeResponse(Player player, String action, int amount, String itemName, double totalPrice, String originalPlayerMessage) {
        String formattedPrice = plugin.getVaultHook().format(totalPrice);

        if (plugin.getGeminiClient().isConfigured()) {
            String tradePrompt = String.format("El jugador '%s' acaba de %s %dx '%s' por %s monedas en el servidor. Responde en 1 o 2 oraciones alegres y entusiastas en el MISMO IDIOMA que usó el jugador ('%s') celebrando la transacción.",
                    player.getName(), action, amount, itemName, formattedPrice, originalPlayerMessage);

            String sysPrompt = "Eres Gilderbot, el carismático mercader comerciante del Gremio de Aventureros. Hablas con fluidez el idioma del jugador.";

            plugin.getGeminiClient().askMerchant(sysPrompt, tradePrompt).thenAccept(reply -> {
                Bukkit.getScheduler().runTask(plugin, () -> {
                    Bukkit.broadcastMessage("§b🤖 Mercader: §f" + ChatColor.translateAlternateColorCodes('&', reply));
                });
            });
        } else {
            String defaultReply = action.equals("comprar") 
                    ? "¡Trato hecho, " + player.getName() + "! Te he vendido " + amount + "x " + itemName + " por " + formattedPrice + ". ¡Gracias por tu compra!"
                    : "¡Excelente negocio, " + player.getName() + "! Te he comprado " + amount + "x " + itemName + " por " + formattedPrice + ".";
            Bukkit.broadcastMessage("§b🤖 Mercader: §f" + defaultReply);
        }
    }
}
