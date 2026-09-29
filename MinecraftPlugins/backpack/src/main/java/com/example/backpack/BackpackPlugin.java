package com.example.backpack;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.util.io.BukkitObjectInputStream;
import org.bukkit.util.io.BukkitObjectOutputStream;

import java.io.*;
import java.sql.*;
import java.util.*;

public class BackpackPlugin extends JavaPlugin implements CommandExecutor, Listener {

    private Connection connection;
    private final Map<UUID, Inventory> activeBackpacks = new HashMap<>();

    @Override
    public void onEnable() {
        if (!getDataFolder().exists()) {
            getDataFolder().mkdirs();
        }
        initDatabase();

        this.getCommand("backpack").setExecutor(this);
        Bukkit.getPluginManager().registerEvents(this, this);

        getLogger().info("FreeBackpack Plugin v2.0.0 habilitado - Acceso total sin permisos ni OP.");
    }

    @Override
    public void onDisable() {
        for (Map.Entry<UUID, Inventory> entry : activeBackpacks.entrySet()) {
            saveBackpack(entry.getKey(), entry.getValue());
        }
        activeBackpacks.clear();
        closeDatabase();
        getLogger().info("FreeBackpack Plugin guardado y deshabilitado.");
    }

    private void initDatabase() {
        try {
            File dbFile = new File(getDataFolder(), "backpacks.db");
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection("jdbc:sqlite:" + dbFile.getAbsolutePath());
            try (Statement stmt = connection.createStatement()) {
                stmt.executeUpdate("CREATE TABLE IF NOT EXISTS backpacks (uuid TEXT PRIMARY KEY, items BLOB)");
            }
        } catch (Exception e) {
            getLogger().severe("Error inicializando base de datos SQLite para mochilas: " + e.getMessage());
        }
    }

    private void closeDatabase() {
        try {
            if (connection != null && !connection.isClosed()) {
                connection.close();
            }
        } catch (SQLException e) {
            getLogger().severe("Error cerrando base de datos: " + e.getMessage());
        }
    }

    private synchronized Inventory getOrCreateBackpack(Player p) {
        UUID uuid = p.getUniqueId();
        if (activeBackpacks.containsKey(uuid)) {
            return activeBackpacks.get(uuid);
        }

        Inventory inv = Bukkit.createInventory(p, 54, ChatColor.DARK_GREEN + "Mochila de " + p.getName());
        try (PreparedStatement pstmt = connection.prepareStatement("SELECT items FROM backpacks WHERE uuid = ?")) {
            pstmt.setString(1, uuid.toString());
            ResultSet rs = pstmt.executeQuery();
            if (rs.next()) {
                byte[] bytes = rs.getBytes("items");
                if (bytes != null && bytes.length > 0) {
                    ItemStack[] items = deserializeItems(bytes);
                    if (items != null) {
                        inv.setContents(items);
                    }
                }
            }
        } catch (Exception e) {
            getLogger().warning("No se pudo cargar la mochila de " + p.getName() + ": " + e.getMessage());
        }

        activeBackpacks.put(uuid, inv);
        return inv;
    }

    private synchronized void saveBackpack(UUID uuid, Inventory inv) {
        if (inv == null || connection == null) return;
        try {
            byte[] bytes = serializeItems(inv.getContents());
            if (bytes != null) {
                try (PreparedStatement pstmt = connection.prepareStatement("INSERT INTO backpacks(uuid, items) VALUES(?, ?) ON CONFLICT(uuid) DO UPDATE SET items=excluded.items")) {
                    pstmt.setString(1, uuid.toString());
                    pstmt.setBytes(2, bytes);
                    pstmt.executeUpdate();
                }
            }
        } catch (Exception e) {
            getLogger().severe("Error guardando mochila para UUID " + uuid + ": " + e.getMessage());
        }
    }

    private byte[] serializeItems(ItemStack[] items) {
        try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
             BukkitObjectOutputStream dataOutput = new BukkitObjectOutputStream(outputStream)) {
            dataOutput.writeInt(items.length);
            for (ItemStack item : items) {
                dataOutput.writeObject(item);
            }
            return outputStream.toByteArray();
        } catch (Exception e) {
            getLogger().severe("Error serializando ítems de la mochila: " + e.getMessage());
            return null;
        }
    }

    private ItemStack[] deserializeItems(byte[] bytes) {
        try (ByteArrayInputStream inputStream = new ByteArrayInputStream(bytes);
             BukkitObjectInputStream dataInput = new BukkitObjectInputStream(inputStream)) {
            int length = dataInput.readInt();
            ItemStack[] items = new ItemStack[length];
            for (int i = 0; i < length; i++) {
                items[i] = (ItemStack) dataInput.readObject();
            }
            return items;
        } catch (Exception e) {
            getLogger().severe("Error deserializando ítems de la mochila: " + e.getMessage());
            return null;
        }
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("Este comando solo puede ser ejecutado por jugadores.");
            return true;
        }

        Player p = (Player) sender;
        
        // CERO RESTRICCION DE OP O PERMISOS - CUALQUIER JUGADOR PUEDE ABRIR SU MOCHILA
        Inventory inv = getOrCreateBackpack(p);
        p.openInventory(inv);
        p.sendMessage(ChatColor.GREEN + "Mochila abierta exitosamente.");
        return true;
    }

    @EventHandler
    public void onInventoryClose(InventoryCloseEvent event) {
        if (!(event.getPlayer() instanceof Player)) return;
        Player p = (Player) event.getPlayer();
        UUID uuid = p.getUniqueId();

        if (activeBackpacks.containsKey(uuid) && event.getInventory().equals(activeBackpacks.get(uuid))) {
            saveBackpack(uuid, activeBackpacks.get(uuid));
        }
    }
}
