package com.guild.aieconomy.economy;

import org.bukkit.Material;
import org.bukkit.configuration.file.FileConfiguration;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class DynamicMarketEngine {

    private final Map<Material, Double> basePrices = new HashMap<>();
    private final Map<Material, Integer> recentDemand = new ConcurrentHashMap<>();
    
    private double alphaSensitivity = 0.15;
    private double minPriceFactor = 0.70;
    private double maxPriceFactor = 1.50;
    private double guildTaxPercent = 5.0;

    public void loadFromConfig(FileConfiguration config) {
        basePrices.clear();
        if (config.isConfigurationSection("economy.base_prices")) {
            for (String key : config.getConfigurationSection("economy.base_prices").getKeys(false)) {
                Material mat = Material.matchMaterial(key);
                if (mat != null) {
                    double price = config.getDouble("economy.base_prices." + key, 10.0);
                    basePrices.put(mat, price);
                }
            }
        }
        this.alphaSensitivity = config.getDouble("economy.alpha_sensitivity", 0.15);
        this.minPriceFactor = config.getDouble("economy.min_price_factor", 0.70);
        this.maxPriceFactor = config.getDouble("economy.max_price_factor", 1.50);
        this.guildTaxPercent = config.getDouble("economy.guild_tax_percent", 5.0);

        populateAllObtainableVanillaBlocks();
    }

    public void populateAllObtainableVanillaBlocks() {
        for (Material mat : Material.values()) {
            if (!mat.isItem() || !mat.isBlock()) continue;
            if (mat.isAir()) continue;
            String name = mat.name();
            if (name.startsWith("LEGACY_")) continue;

            // Excluir bloques técnicos / inobtenibles / de comandos
            if (name.contains("COMMAND_BLOCK") || name.equals("BEDROCK") || name.equals("BARRIER") ||
                name.contains("STRUCTURE") || name.equals("JIGSAW") || name.equals("LIGHT") ||
                name.contains("PORTAL") || name.contains("CAULDRON") || name.contains("STEM") ||
                name.equals("FIRE") || name.equals("SOUL_FIRE") || name.equals("WATER") || name.equals("LAVA") ||
                name.equals("BUBBLE_COLUMN") || name.equals("POWDER_SNOW") || name.contains("PISTON") ||
                name.contains("VINES_PLANT") || name.equals("FROGSPAWN") || name.equals("TRIPWIRE")) {
                continue;
            }

            if (!basePrices.containsKey(mat)) {
                double price = calculateDefaultVanillaBlockPrice(mat);
                basePrices.put(mat, price);
            }
        }
    }

    private double calculateDefaultVanillaBlockPrice(Material mat) {
        String name = mat.name();
        if (name.contains("DIRT") || name.contains("COBBLESTONE") || name.contains("SAND") || name.contains("GRAVEL") || name.contains("NETHERRACK") || name.equals("STONE")) {
            return 2.0;
        }
        if (name.contains("DEEPSLATE") || name.contains("TUFF") || name.contains("MUD") || name.contains("GRANITE") || name.contains("DIORITE") || name.contains("ANDESITE") || name.contains("BASALT")) {
            return 3.0;
        }
        if (name.contains("LOG") || name.contains("WOOD") || name.contains("PLANKS") || name.contains("BRICKS") || name.contains("GLASS") || name.contains("TERRACOTTA") || name.contains("WOOL") || name.contains("CONCRETE")) {
            return 5.0;
        }
        if (name.contains("QUARTZ") || name.contains("PRISMARINE") || name.contains("PURPUR") || name.contains("COPPER") || name.contains("GLOWSTONE") || name.contains("SEA_LANTERN") || name.contains("SPONGE")) {
            return 25.0;
        }
        if (name.contains("COAL_BLOCK") || name.contains("IRON_BLOCK") || name.contains("REDSTONE_BLOCK") || name.contains("LAPIS_BLOCK")) {
            return 90.0;
        }
        if (name.contains("GOLD_BLOCK") || name.contains("EMERALD_BLOCK")) {
            return 300.0;
        }
        if (name.contains("DIAMOND_BLOCK")) {
            return 900.0;
        }
        if (name.contains("NETHERITE_BLOCK")) {
            return 4500.0;
        }
        return 10.0;
    }

    public Map<Material, Double> getBasePrices() {
        return basePrices;
    }

    public void registerDemand(Material material, int delta) {
        recentDemand.merge(material, delta, Integer::sum);
    }

    public double calculateBuyPrice(Material material, int currentStock) {
        Double base = basePrices.getOrDefault(material, 10.0);
        int demand = recentDemand.getOrDefault(material, 1);

        double supplyRatio = Math.max(1.0, currentStock);
        double demandFactor = 1.0 + (alphaSensitivity * (demand / supplyRatio));

        double clampedFactor = Math.min(maxPriceFactor, Math.max(minPriceFactor, demandFactor));
        double finalPrice = base * clampedFactor;

        return Math.round(finalPrice * 100.0) / 100.0;
    }

    public double calculateSellPrice(Material material, int currentStock) {
        double buyPrice = calculateBuyPrice(material, currentStock);
        double sellPrice = buyPrice * 0.70 * (1.0 - (guildTaxPercent / 100.0));
        return Math.max(0.1, Math.round(sellPrice * 100.0) / 100.0);
    }

    public String getTrendIndicator(Material material, int currentStock) {
        double buyPrice = calculateBuyPrice(material, currentStock);
        double basePrice = basePrices.getOrDefault(material, 10.0);
        if (buyPrice > basePrice * 1.05) {
            return "§c📈 En Alza (+ demandado)";
        } else if (buyPrice < basePrice * 0.95) {
            return "§a📉 En Baja (abundante)";
        }
        return "§e➖ Estable";
    }

    public double getGuildTaxPercent() {
        return guildTaxPercent;
    }
}
