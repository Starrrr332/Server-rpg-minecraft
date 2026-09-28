package com.example.shopenhancer;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.plugin.java.JavaPlugin;

public class ShopEnhancerPlugin extends JavaPlugin implements Listener, CommandExecutor {
    private double priceMultiplier = 1.0;

    @Override
    public void onEnable() {
        Bukkit.getPluginManager().registerEvents(this, this);
        this.getCommand("shopinfo").setExecutor(this);
        // Recalcula cada 5 minutos (5*60*20 ticks)
        Bukkit.getScheduler().runTaskTimer(this, this::recalcMultiplier, 0L, 5L * 60L * 20L);
        getLogger().info("ShopEnhancer enabled");
    }

    private void recalcMultiplier() {
        // TODO: implementar métrica real (ventas últimas 1h). Por ahora un placeholder aleatorio.
        int recentSales = (int) (Math.random() * 200);
        priceMultiplier = 1.0 + recentSales / 1000.0;
        getLogger().info("Nuevo multiplicador de precios: " + priceMultiplier);
    }

    // Ejemplo de hook ficticio para una tienda. Reemplazar con el evento real del plugin shop que uses.
    @EventHandler
    public void onShopPurchase(Object e) {
        // Este método es solo ilustrativo; sustituir por el evento correcto.
        // Player p = ...;
        // double basePrice = ...;
        // double finalPrice = basePrice * priceMultiplier;
        // if (PartyUtil.isInSameParty(p)) finalPrice *= 0.95;
        // aplicar durabilidad extra al ítem comprado
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player)) return true;
        sender.sendMessage(ChatColor.GOLD + "Multiplicador de precios actual: " + priceMultiplier);
        sender.sendMessage(ChatColor.GREEN + "Descuento de 5% si estás en party.");
        return true;
    }
}
