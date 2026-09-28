package com.example.directloot;

import org.bukkit.inventory.ItemStack;
import org.bukkit.util.io.BukkitObjectInputStream;
import org.bukkit.util.io.BukkitObjectOutputStream;
import org.yaml.snakeyaml.external.biz.base64Coder.Base64Coder;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

/**
 * Utility class to serialize and deserialize ItemStack collections to/from Base64 strings.
 * Used by DirectLootPlugin to store pending loot when the player's inventory is full.
 */
public class ItemSerializer {
    /**
     * Serializes a list of ItemStacks to a Base64-encoded string.
     */
    public static String toBase64(List<ItemStack> items) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            BukkitObjectOutputStream bcos = new BukkitObjectOutputStream(baos);
            bcos.writeObject(new ArrayList<>(items));
            bcos.flush();
            return Base64Coder.encodeLines(baos.toByteArray());
        } catch (Exception e) {
            throw new RuntimeException("Failed to serialize ItemStack list", e);
        }
    }

    /**
     * Deserializes a Base64 string back into a list of ItemStacks.
     */
    @SuppressWarnings("unchecked")
    public static List<ItemStack> fromBase64(String base64) {
        try {
            byte[] data = Base64Coder.decodeLines(base64);
            ByteArrayInputStream bais = new ByteArrayInputStream(data);
            BukkitObjectInputStream bcis = new BukkitObjectInputStream(bais);
            return (List<ItemStack>) bcis.readObject();
        } catch (Exception e) {
            throw new RuntimeException("Failed to deserialize ItemStack list", e);
        }
    }
}
