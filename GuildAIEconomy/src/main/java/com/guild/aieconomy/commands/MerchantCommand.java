package com.guild.aieconomy.commands;

import com.guild.aieconomy.GuildAIEconomy;
import com.guild.aieconomy.gui.ShopGUI;
import com.guild.aieconomy.gui.ShopGUI.ShopType;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.block.Block;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.entity.Villager;
import org.bukkit.inventory.ItemStack;

import java.util.Map;

public class MerchantCommand implements CommandExecutor {

    private final GuildAIEconomy plugin;

    public MerchantCommand(GuildAIEconomy plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (args.length == 0 || args[0].equalsIgnoreCase("vanillashop") || args[0].equalsIgnoreCase("shop") || args[0].equalsIgnoreCase("abrir") || args[0].equalsIgnoreCase("tienda")) {
            if (sender instanceof Player player) {
                ShopGUI gui = new ShopGUI(plugin, ShopType.VANILLA, 1);
                gui.open(player);
                return true;
            } else {
                sendHelp(sender);
                return true;
            }
        }

        String sub = args[0].toLowerCase();

        switch (sub) {
            case "menu", "gremio" -> {
                if (sender instanceof Player player) {
                    com.guild.aieconomy.gui.GuildMenuGUI menu = new com.guild.aieconomy.gui.GuildMenuGUI(plugin, player);
                    menu.open(player);
                    return true;
                } else {
                    sendHelp(sender);
                    return true;
                }
            }
            case "rank", "rango" -> {
                if (sender instanceof Player player) {
                    var data = plugin.getRankManager().getPlayerData(player);
                    player.sendMessage("§a[Gremio] Tu Rango: " + data.getRank().getDisplayName());
                    player.sendMessage("§eProgreso: " + plugin.getRankManager().getRankProgressFormatted(player));
                    return true;
                } else {
                    sender.sendMessage("Comando solo para jugadores.");
                    return true;
                }
            }
            case "setup" -> {
                plugin.getHologramManager().setupGuildHolograms();
                sender.sendMessage("§a[GuildAIEconomy] ¡Hologramas 3D del Gremio configurados en sus posiciones!");
                return true;
            }
            case "customshop", "rpgshop" -> {
                if (sender instanceof Player player) {
                    ShopGUI gui = new ShopGUI(plugin, ShopType.CUSTOM_RPG, 1);
                    gui.open(player);
                    return true;
                } else {
                    sendHelp(sender);
                    return true;
                }
            }
            case "spawn" -> {
                if (!(sender instanceof Player player)) {
                    sender.sendMessage("Solo jugadores pueden ejecutar este comando.");
                    return true;
                }
                String type = (args.length >= 2) ? args[1].toLowerCase() : "vanilla";
                
                String customName = switch (type) {
                    case "custom", "rpg" -> "§d⚔️ [IA] Mercader RPG & EliteMobs";
                    case "cacerias", "quests" -> "§e📜 Maestro de Cacerías del Gremio";
                    case "comandante", "ranks" -> "§a🏆 Comandante del Gremio (Rangos)";
                    default -> "§b🧱 [IA] Mercader Vanilla";
                };

                String profession = switch (type) {
                    case "custom", "rpg" -> "WEAPONSMITH";
                    case "cacerias", "quests" -> "FLETCHER";
                    case "comandante", "ranks" -> "ARMORER";
                    default -> "LIBRARIAN";
                };

                Location spawnLoc = player.getLocation();
                Villager v = plugin.getMerchantVillager().spawnMerchant(spawnLoc, customName, profession, type);

                if (v != null && v.isValid()) {
                    player.playSound(spawnLoc, Sound.ENTITY_PLAYER_LEVELUP, 1.0f, 1.0f);
                    player.getWorld().spawnParticle(Particle.VILLAGER_HAPPY, spawnLoc.clone().add(0, 1, 0), 30, 0.3, 0.5, 0.3, 0.1);
                    player.sendMessage("§a[GuildAIEconomy] ¡NPC (" + type.toUpperCase() + ") generado con éxito!");
                } else {
                    player.sendMessage("§c[GuildAIEconomy] Error al generar el NPC.");
                }
            }
            case "additem" -> {
                if (!(sender instanceof Player player)) {
                    sender.sendMessage("Solo jugadores pueden ejecutar este comando.");
                    return true;
                }
                if (!player.hasPermission("guildai.admin")) {
                    player.sendMessage("§cNo tienes permiso para agregar ítems a la economía.");
                    return true;
                }
                if (args.length < 3) {
                    player.sendMessage("Uso: /guildai additem <id_item> <precio_compra> [precio_venta]");
                    return true;
                }

                ItemStack held = player.getInventory().getItemInMainHand();
                if (held == null || held.getType() == Material.AIR) {
                    player.sendMessage("§cDebes sostener el ítem (Vanilla o EliteMobs Custom) en tu mano principal.");
                    return true;
                }

                String itemId = args[1].toLowerCase();
                try {
                    double buyPrice = Double.parseDouble(args[2]);
                    double sellPrice = (args.length >= 4) ? Double.parseDouble(args[3]) : (buyPrice * 0.70);

                    boolean success = plugin.getCustomItemManager().addCustomItem(itemId, held, buyPrice, sellPrice);
                    if (success) {
                        player.sendMessage("§a[GuildAIEconomy] ¡Ítem RPG '" + itemId + "' agregado con precio Compra: " 
                            + plugin.getVaultHook().format(buyPrice) + " | Venta: " + plugin.getVaultHook().format(sellPrice) + "!");
                    }
                } catch (NumberFormatException e) {
                    player.sendMessage("§cLos precios deben ser números válidos.");
                }
            }
            case "removeitem" -> {
                if (!sender.hasPermission("guildai.admin")) {
                    sender.sendMessage("§cNo tienes permiso para remover ítems.");
                    return true;
                }
                if (args.length < 2) {
                    sender.sendMessage("Uso: /guildai removeitem <id_item>");
                    return true;
                }
                String itemId = args[1].toLowerCase();
                if (plugin.getCustomItemManager().removeCustomItem(itemId)) {
                    sender.sendMessage("§a[GuildAIEconomy] Ítem '" + itemId + "' removido de la economía.");
                } else {
                    sender.sendMessage("§cNo se encontró ningún ítem personalizado con id '" + itemId + "'.");
                }
            }
            case "setchest" -> {
                if (!(sender instanceof Player player)) {
                    sender.sendMessage("Solo jugadores pueden ejecutar este comando.");
                    return true;
                }
                Block block = player.getTargetBlockExact(5);
                if (block == null || (block.getType() != Material.CHEST && block.getType() != Material.TRAPPED_CHEST)) {
                    player.sendMessage("§cDebes estar mirando a un Cofre (a menos de 5 bloques).");
                    return true;
                }
                plugin.getChestManager().setChestLocation(block.getLocation());
                player.sendMessage("§a[GuildAIEconomy] ¡Cofre de Economía del Chatbot configurado en X:" + block.getX() + " Y:" + block.getY() + " Z:" + block.getZ() + "!");
            }
            case "setkey" -> {
                if (!sender.hasPermission("guildai.admin")) {
                    sender.sendMessage("§cNo tienes permiso para configurar la API Key de la IA.");
                    return true;
                }
                if (args.length < 2) {
                    sender.sendMessage("§cUso: /guildai setkey <tu_gemini_api_key>");
                    return true;
                }
                String key = args[1].trim();
                plugin.getConfig().set("gemini.api_key", key);
                plugin.saveConfig();
                plugin.reloadPluginConfig();
                sender.sendMessage("§a[GuildAIEconomy] ¡API Key de Gemini guardada correctamente! El bot IA conversacional está activado.");
            }
            case "reload" -> {
                plugin.reloadPluginConfig();
                sender.sendMessage("§a[GuildAIEconomy] Configuración recargada con éxito.");
            }
            case "prices" -> {
                sender.sendMessage("§b=== PRECIOS DE MERCADO VANILLA ===");
                for (Map.Entry<Material, Double> entry : plugin.getMarketEngine().getBasePrices().entrySet()) {
                    Material mat = entry.getKey();
                    int stock = plugin.getChestManager().getItemStock(mat);
                    double buy = plugin.getMarketEngine().calculateBuyPrice(mat, stock);
                    double sell = plugin.getMarketEngine().calculateSellPrice(mat, stock);
                    String trend = plugin.getMarketEngine().getTrendIndicator(mat, stock);
                    sender.sendMessage("§7- §f" + mat.name() + " §7| Stock: §e" + stock + " §7| Compra: §a" + plugin.getVaultHook().format(buy) + " §7| Venta: §c" + plugin.getVaultHook().format(sell) + " " + trend);
                }
            }
            case "talk" -> {
                if (args.length < 2) {
                    sender.sendMessage("Uso: /guildai talk <mensaje>");
                    return true;
                }
                StringBuilder sb = new StringBuilder();
                for (int i = 1; i < args.length; i++) {
                    sb.append(args[i]).append(" ");
                }
                String promptText = sb.toString().trim();
                sender.sendMessage("§b🤖 Mercader: §7Pensando respuesta...");
                String systemPrompt = plugin.getConfig().getString("gemini.system_prompt", "Eres Gilderbot, el mercader del gremio.");
                
                plugin.getGeminiClient().askMerchant(systemPrompt, promptText).thenAccept(reply -> {
                    sender.sendMessage("§b🤖 Mercader: §f" + ChatColor.translateAlternateColorCodes('&', reply));
                });
            }
            default -> {
                if (sender instanceof Player player) {
                    ShopGUI gui = new ShopGUI(plugin, ShopType.VANILLA, 1);
                    gui.open(player);
                } else {
                    sendHelp(sender);
                }
            }
        }
        return true;
    }

    private void sendHelp(CommandSender sender) {
        sender.sendMessage("§b=== GuildAIEconomy v1.3.0 - Gremio de Aventureros ===");
        sender.sendMessage("§e/guildai menu §7- Abre el Menú Principal Interactivo del Gremio");
        sender.sendMessage("§e/guildai rank §7- Muestra tu Rango de Aventurero y Progreso de EXP");
        sender.sendMessage("§e/guildai shop §7- Abre la tienda Vanilla (Bloques y Materiales)");
        sender.sendMessage("§e/guildai customshop §7- Abre la tienda Custom RPG / EliteMobs (25,000+ monedas)");
        sender.sendMessage("§e/guildai spawn <vanilla|custom|cacerias|comandante> §7- Spawnea un NPC en tu posición");
        sender.sendMessage("§e/guildai setup §7- Genera los Hologramas 3D del Gremio en sus puestos");
        sender.sendMessage("§e/guildai setkey <api_key> §7- Configura la Gemini API Key del Bot IA");
        sender.sendMessage("§e/guildai additem <id> <compra> [venta] §7- Agrega ítem RPG en mano");
        sender.sendMessage("§e/guildai removeitem <id> §7- Elimina un ítem RPG custom de la tienda");
        sender.sendMessage("§e/guildai setchest §7- Vincula el cofre de economía que estás mirando");
        sender.sendMessage("§e/guildai reload §7- Recarga la configuración");
        sender.sendMessage("§e/guildai talk <texto> §7- Habla con el Chatbot IA");
        sender.sendMessage("§e/guildai prices §7- Muestra precios del mercado Vanilla");
    }
}
