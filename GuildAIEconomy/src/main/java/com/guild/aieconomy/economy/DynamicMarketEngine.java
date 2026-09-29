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
        // El precio de venta al bot es 70% del precio de compra menos impuesto del gremio
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
