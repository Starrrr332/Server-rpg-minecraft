package com.guild.aieconomy.economy;

import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.ChatColor;

import java.util.HashMap;
import java.util.Map;

public class ItemResolver {

    private final Map<String, Material> multiLangMap = new HashMap<>();

    public ItemResolver() {
        initMultiLangMap();
    }

    private void initMultiLangMap() {
        // --- ESPAÑOL ---
        multiLangMap.put("diamante", Material.DIAMOND);
        multiLangMap.put("bloque de diamante", Material.DIAMOND_BLOCK);
        multiLangMap.put("oro", Material.GOLD_INGOT);
        multiLangMap.put("lingote de oro", Material.GOLD_INGOT);
        multiLangMap.put("bloque de oro", Material.GOLD_BLOCK);
        multiLangMap.put("hierro", Material.IRON_INGOT);
        multiLangMap.put("lingote de hierro", Material.IRON_INGOT);
        multiLangMap.put("bloque de hierro", Material.IRON_BLOCK);
        multiLangMap.put("esmeralda", Material.EMERALD);
        multiLangMap.put("bloque de esmeralda", Material.EMERALD_BLOCK);
        multiLangMap.put("netherita", Material.NETHERITE_INGOT);
        multiLangMap.put("lingote de netherita", Material.NETHERITE_INGOT);
        multiLangMap.put("bloque de netherita", Material.NETHERITE_BLOCK);
        multiLangMap.put("cobre", Material.COPPER_INGOT);
        multiLangMap.put("lingote de cobre", Material.COPPER_INGOT);
        multiLangMap.put("lapislazuli", Material.LAPIS_LAZULI);
        multiLangMap.put("lapis", Material.LAPIS_LAZULI);
        multiLangMap.put("carbon", Material.COAL);
        multiLangMap.put("roble", Material.OAK_LOG);
        multiLangMap.put("madera", Material.OAK_LOG);
        multiLangMap.put("tronco de roble", Material.OAK_LOG);
        multiLangMap.put("tablas de roble", Material.OAK_PLANKS);
        multiLangMap.put("piedra", Material.STONE);
        multiLangMap.put("adoquin", Material.COBBLESTONE);
        multiLangMap.put("arena", Material.SAND);
        multiLangMap.put("grava", Material.GRAVEL);
        multiLangMap.put("tierra", Material.DIRT);
        multiLangMap.put("obsidiana", Material.OBSIDIAN);
        multiLangMap.put("obsidiana llorosa", Material.CRYING_OBSIDIAN);
        multiLangMap.put("estrella", Material.NETHER_STAR);
        multiLangMap.put("estrella del nether", Material.NETHER_STAR);
        multiLangMap.put("elitros", Material.ELYTRA);
        multiLangMap.put("elytra", Material.ELYTRA);
        multiLangMap.put("manzana", Material.APPLE);
        multiLangMap.put("manzana dorada", Material.GOLDEN_APPLE);
        multiLangMap.put("manzana encantada", Material.ENCHANTED_GOLDEN_APPLE);
        multiLangMap.put("filete", Material.COOKED_BEEF);
        multiLangMap.put("carne", Material.COOKED_BEEF);
        multiLangMap.put("zanahoria", Material.CARROT);
        multiLangMap.put("zanahoria dorada", Material.GOLDEN_CARROT);
        multiLangMap.put("patata", Material.POTATO);
        multiLangMap.put("trigo", Material.WHEAT);
        multiLangMap.put("pan", Material.BREAD);
        multiLangMap.put("totem", Material.TOTEM_OF_UNDYING);
        multiLangMap.put("totem de inmortalidad", Material.TOTEM_OF_UNDYING);
        multiLangMap.put("flecha", Material.ARROW);
        multiLangMap.put("arco", Material.BOW);
        multiLangMap.put("antorcha", Material.TORCH);
        multiLangMap.put("cristal", Material.GLASS);
        multiLangMap.put("vidrio", Material.GLASS);

        // --- ENGLISH ---
        multiLangMap.put("diamond", Material.DIAMOND);
        multiLangMap.put("diamond block", Material.DIAMOND_BLOCK);
        multiLangMap.put("gold", Material.GOLD_INGOT);
        multiLangMap.put("gold ingot", Material.GOLD_INGOT);
        multiLangMap.put("gold block", Material.GOLD_BLOCK);
        multiLangMap.put("iron", Material.IRON_INGOT);
        multiLangMap.put("iron ingot", Material.IRON_INGOT);
        multiLangMap.put("iron block", Material.IRON_BLOCK);
        multiLangMap.put("emerald", Material.EMERALD);
        multiLangMap.put("emerald block", Material.EMERALD_BLOCK);
        multiLangMap.put("netherite", Material.NETHERITE_INGOT);
        multiLangMap.put("netherite ingot", Material.NETHERITE_INGOT);
        multiLangMap.put("netherite block", Material.NETHERITE_BLOCK);
        multiLangMap.put("copper", Material.COPPER_INGOT);
        multiLangMap.put("copper ingot", Material.COPPER_INGOT);
        multiLangMap.put("coal", Material.COAL);
        multiLangMap.put("wood", Material.OAK_LOG);
        multiLangMap.put("oak log", Material.OAK_LOG);
        multiLangMap.put("oak planks", Material.OAK_PLANKS);
        multiLangMap.put("stone", Material.STONE);
        multiLangMap.put("cobblestone", Material.COBBLESTONE);
        multiLangMap.put("sand", Material.SAND);
        multiLangMap.put("gravel", Material.GRAVEL);
        multiLangMap.put("dirt", Material.DIRT);
        multiLangMap.put("obsidian", Material.OBSIDIAN);
        multiLangMap.put("nether star", Material.NETHER_STAR);
        multiLangMap.put("apple", Material.APPLE);
        multiLangMap.put("golden apple", Material.GOLDEN_APPLE);
        multiLangMap.put("steak", Material.COOKED_BEEF);
        multiLangMap.put("beef", Material.COOKED_BEEF);
        multiLangMap.put("golden carrot", Material.GOLDEN_CARROT);
        multiLangMap.put("totem of undying", Material.TOTEM_OF_UNDYING);

        // --- PORTUGUÊS ---
        multiLangMap.put("ouro", Material.GOLD_INGOT);
        multiLangMap.put("ferro", Material.IRON_INGOT);
        multiLangMap.put("pedra", Material.STONE);
        multiLangMap.put("madeira", Material.OAK_LOG);
        multiLangMap.put("maca", Material.APPLE);

        // Populate direct Material enum matching for all 800+ Minecraft materials
        for (Material mat : Material.values()) {
            if (!mat.isItem() || mat.isAir()) continue;
            String nameLower = mat.name().toLowerCase();
            multiLangMap.putIfAbsent(nameLower, mat);
            multiLangMap.putIfAbsent(nameLower.replace("_", " "), mat);
        }
    }

    public Material resolveVanillaMaterial(String query) {
        if (query == null || query.isBlank()) return null;
        String clean = query.toLowerCase().trim().replace("ñ", "n");

        // 1. Direct multi-lang dictionary lookup
        if (multiLangMap.containsKey(clean)) {
            return multiLangMap.get(clean);
        }

        // 2. Substring matching for multi-word phrases
        for (Map.Entry<String, Material> entry : multiLangMap.entrySet()) {
            String key = entry.getKey();
            if (clean.contains(key) || key.contains(clean)) {
                return entry.getValue();
            }
        }

        // 3. Fallback Bukkit Material match
        return Material.matchMaterial(clean.toUpperCase().replace(" ", "_"));
    }

    public String getItemDisplayName(Material mat) {
        if (mat == null) return "Ítem";
        String name = mat.name().replace("_", " ").toLowerCase();
        String[] words = name.split(" ");
        StringBuilder sb = new StringBuilder();
        for (String w : words) {
            if (!w.isEmpty()) {
                sb.append(Character.toUpperCase(w.charAt(0))).append(w.substring(1)).append(" ");
            }
        }
        return sb.toString().trim();
    }
}
