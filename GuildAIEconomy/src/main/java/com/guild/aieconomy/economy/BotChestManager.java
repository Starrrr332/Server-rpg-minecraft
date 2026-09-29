package com.guild.aieconomy.economy;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.block.Chest;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.HashMap;
import java.util.Map;

public class BotChestManager {

    private final JavaPlugin plugin;
    private Location chestLocation;
    private final Map<Material, Integer> virtualStock = new HashMap<>();

    public BotChestManager(JavaPlugin plugin) {
        this.plugin = plugin;
        loadChestLocation();
    }

    public void setChestLocation(Location loc) {
        this.chestLocation = loc;
        FileConfiguration config = plugin.getConfig();
        if (loc != null) {
            config.set("chest.world", loc.getWorld().getName());
            config.set("chest.x", loc.getBlockX());
            config.set("chest.y", loc.getBlockY());
            config.set("chest.z", loc.getBlockZ());
        } else {
            config.set("chest", null);
        }
        plugin.saveConfig();
    }

    public void loadChestLocation() {
        FileConfiguration config = plugin.getConfig();
        if (config.contains("chest.world")) {
            String worldName = config.getString("chest.world");
            int x = config.getInt("chest.x");
            int y = config.getInt("chest.y");
            int z = config.getInt("chest.z");
            if (worldName != null && Bukkit.getWorld(worldName) != null) {
                this.chestLocation = new Location(Bukkit.getWorld(worldName), x, y, z);
            }
        }
    }

    public Inventory getChestInventory() {
        if (chestLocation != null && chestLocation.getWorld() != null) {
            Block block = chestLocation.getBlock();
            if (block.getState() instanceof Chest chest) {
                return chest.getInventory();
            }
        }
        return null;
    }

    public int getItemStock(Material material) {
        Inventory inv = getChestInventory();
        if (inv != null) {
            int amount = 0;
            for (ItemStack item : inv.getContents()) {
                if (item != null && item.getType() == material) {
                    amount += item.getAmount();
                }
            }
            return amount;
        }
        return virtualStock.getOrDefault(material, 64);
    }

    public boolean removeItemFromStock(Material material, int amount) {
        Inventory inv = getChestInventory();
        if (inv != null) {
            int remaining = amount;
            ItemStack[] contents = inv.getContents();
            for (int i = 0; i < contents.length; i++) {
                ItemStack item = contents[i];
                if (item != null && item.getType() == material) {
                    if (item.getAmount() <= remaining) {
                        remaining -= item.getAmount();
                        inv.setItem(i, null);
                    } else {
                        item.setAmount(item.getAmount() - remaining);
                        remaining = 0;
                        break;
                    }
                }
            }
            return remaining == 0;
        } else {
            int current = virtualStock.getOrDefault(material, 64);
            if (current >= amount) {
                virtualStock.put(material, current - amount);
                return true;
            }
            return false;
        }
    }

    public boolean addItemToStock(Material material, int amount) {
        Inventory inv = getChestInventory();
        if (inv != null) {
            HashMap<Integer, ItemStack> leftover = inv.addItem(new ItemStack(material, amount));
            return leftover.isEmpty();
        } else {
            virtualStock.merge(material, amount, Integer::sum);
            return true;
        }
    }

    public Location getChestLocation() {
        return chestLocation;
    }
}
