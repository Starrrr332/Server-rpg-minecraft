package com.example.directloot;

import org.bukkit.Bukkit;
import org.bukkit.NamespacedKey;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.java.JavaPlugin;
import java.util.ArrayList;
import java.util.List;

public class DirectLootPlugin extends JavaPlugin implements Listener {
    private final NamespacedKey PENDING_LOOT = new NamespacedKey(this, "pending_loot");

    @Override
    public void onEnable() {
        // registrar listener y comando
        Bukkit.getPluginManager().registerEvents(this, this);
        this.getCommand("claimloot").setExecutor((sender, cmd, label, args) -> {
            if (!(sender instanceof Player)) return true;
            Player p = (Player) sender;
            String data = p.getPersistentDataContainer().get(PENDING_LOOT, PersistentDataType.STRING);
            if (data == null) {
                p.sendMessage("§aNo tienes loot pendiente.");
                return true;
            }
            List<ItemStack> items = ItemSerializer.fromBase64(data);
            boolean allAdded = true;
            for (ItemStack it : items) {
                if (!p.getInventory().addItem(it).isEmpty()) {
                    allAdded = false;
                    break;
                }
            }
            if (allAdded) {
                p.getPersistentDataContainer().remove(PENDING_LOOT);
                p.sendMessage("§aLoot reclamado con éxito!");
            } else {
                p.sendMessage("§cTu inventario sigue lleno. Usa /claimloot cuando haya espacio.");
            }
            return true;
        });
        getLogger().info("DirectLoot enabled");
    }

    @EventHandler
    public void onEntityDeath(EntityDeathEvent e) {
        LivingEntity dead = e.getEntity();
        if (dead.getKiller() == null) return;
        Player killer = dead.getKiller();
        List<ItemStack> toRemove = new ArrayList<>();
        for (ItemStack drop : e.getDrops()) {
            if (killer.getInventory().addItem(drop).isEmpty()) {
                toRemove.add(drop);
            }
        }
        e.getDrops().removeAll(toRemove);
        if (!e.getDrops().isEmpty()) {
            String serialized = ItemSerializer.toBase64(e.getDrops());
            killer.getPersistentDataContainer().set(PENDING_LOOT, PersistentDataType.STRING, serialized);
            killer.sendMessage("§eTu inventario está lleno. Usa §f/claimloot §epara recoger el loot.");
        }
    }
}
