package com.example.backpack;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.plugin.java.JavaPlugin;

public class BackpackPlugin extends JavaPlugin implements CommandExecutor {
    @Override
    public void onEnable() {
        this.getCommand("backpack").setExecutor(this);
        getLogger().info("Backpack plugin enabled");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("Este comando solo puede ser usado por jugadores.");
            return true;
        }
        Player p = (Player) sender;
        Inventory inv = Bukkit.createInventory(p, 27, "Mochila"); // 3 rows (27 slots)
        p.openInventory(inv);
        return true;
    }
}
