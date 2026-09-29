package com.guild.aieconomy.commands;

import com.guild.aieconomy.GuildAIEconomy;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.entity.Villager;

import java.util.Map;

public class MerchantCommand implements CommandExecutor {

    private final GuildAIEconomy plugin;

    public MerchantCommand(GuildAIEconomy plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (args.length == 0) {
            sender.sendMessage("§b=== GuildAIEconomy v1.0.0 ===");
            sender.sendMessage("§e/guildai spawn §7- Spawnea el Aldeano Mercader NPC");
            sender.sendMessage("§e/guildai setchest §7- Vincula el cofre que estás mirando");
            sender.sendMessage("§e/guildai reload §7- Recarga la configuración");
            sender.sendMessage("§e/guildai talk <texto> §7- Habla con el Chatbot IA");
            sender.sendMessage("§e/guildai prices §7- Muestra los precios de mercado actuales");
            return true;
        }

        String sub = args[0].toLowerCase();

        switch (sub) {
            case "spawn" -> {
                if (!(sender instanceof Player player)) {
                    sender.sendMessage("Solo jugadores pueden ejecutar este comando.");
                    return true;
                }
                String customName = plugin.getConfig().getString("merchant.name", "§b🤖 [IA] Mercader del Gremio");
                String profession = plugin.getConfig().getString("merchant.profession", "LIBRARIAN");

                Villager v = plugin.getMerchantVillager().spawnMerchant(player.getLocation(), customName, profession);
                player.sendMessage("§a[GuildAIEconomy] ¡Aldeano Mercader NPC generado exitosamente en tu posición!");
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
            case "reload" -> {
                plugin.reloadPluginConfig();
                sender.sendMessage("§a[GuildAIEconomy] Configuración recargada con éxito.");
            }
            case "prices" -> {
                sender.sendMessage("§b=== PRECIOS DE MERCADO ACTUALES ===");
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
            default -> sender.sendMessage("§cSubcomando desconocido. Usa /guildai para ver la ayuda.");
        }
        return true;
    }
}
