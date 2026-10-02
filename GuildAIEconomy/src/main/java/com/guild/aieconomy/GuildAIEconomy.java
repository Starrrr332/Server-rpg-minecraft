package com.guild.aieconomy;

import com.guild.aieconomy.ai.GeminiClient;
import com.guild.aieconomy.commands.MerchantCommand;
import com.guild.aieconomy.economy.*;
import com.guild.aieconomy.holograms.HologramManager;
import com.guild.aieconomy.npc.MerchantListener;
import com.guild.aieconomy.npc.MerchantVillager;
import com.guild.aieconomy.ranks.GuildRankManager;
import org.bukkit.Material;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.Map;

public class GuildAIEconomy extends JavaPlugin {

    private static GuildAIEconomy instance;
    private VaultHook vaultHook;
    private DynamicMarketEngine marketEngine;
    private BotChestManager chestManager;
    private MerchantVillager merchantVillager;
    private GeminiClient geminiClient;
    private CustomItemManager customItemManager;
    private EliteMobsHook eliteMobsHook;
    private DatabaseManager databaseManager;
    private GuildRankManager rankManager;
    private HologramManager hologramManager;
    private ItemResolver itemResolver;

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();

        // Inicializar Resolvedor de Ítems Multilingüe
        this.itemResolver = new ItemResolver();

        // Inicializar economía Vault
        this.vaultHook = new VaultHook(this);
        if (vaultHook.hasEconomy()) {
            getLogger().info("Conectado exitosamente con Vault Economy.");
        } else {
            getLogger().warning("Vault no detectado. Se utilizará simulación económica de prueba.");
        }

        // Inicializar Hook EliteMobs
        this.eliteMobsHook = new EliteMobsHook(this);

        // Inicializar Base de Datos SQL
        this.databaseManager = new DatabaseManager(this);

        // Inicializar Gestor de Rangos del Gremio
        this.rankManager = new GuildRankManager(this);

        // Inicializar Gestor de Hologramas
        this.hologramManager = new HologramManager(this);

        // Inicializar Motor Económico
        this.marketEngine = new DynamicMarketEngine();
        this.marketEngine.loadFromConfig(getConfig());

        // Cargar ítems adicionales desde la Base de Datos
        Map<Material, Double> dbPrices = databaseManager.loadExtensiveItems();
        for (Map.Entry<Material, Double> entry : dbPrices.entrySet()) {
            this.marketEngine.getBasePrices().putIfAbsent(entry.getKey(), entry.getValue());
        }

        // Inicializar Gestores de Ítems Custom y Cofre
        this.customItemManager = new CustomItemManager(this);
        this.chestManager = new BotChestManager(this);

        // Escanear e Integrar ítems de EliteMobs automáticamente en segundo plano (Async)
        getServer().getScheduler().runTaskAsynchronously(this, () -> {
            this.eliteMobsHook.scanAndRegisterEliteMobsItems(this.customItemManager);
        });

        // Inicializar Aldeano NPC
        this.merchantVillager = new MerchantVillager(this);

        // Inicializar Cliente Gemini IA
        String apiKey = getConfig().getString("gemini.api_key", "");
        String model = getConfig().getString("gemini.model", "gemini-2.5-flash");
        this.geminiClient = new GeminiClient(apiKey, model);

        // Registrar Eventos y Comandos
        getServer().getPluginManager().registerEvents(new MerchantListener(this), this);
        if (getCommand("guildai") != null) {
            getCommand("guildai").setExecutor(new MerchantCommand(this));
        }

        getLogger().info("============================================");
        getLogger().info(" GuildAIEconomy v1.3.0 - Gremio Activado!");
        getLogger().info(" Mercaderes IA, Hologramas y Rangos Listos.");
        getLogger().info("============================================");
    }

    @Override
    public void onDisable() {
        if (databaseManager != null) {
            databaseManager.close();
        }
        getLogger().info("GuildAIEconomy desactivado.");
    }

    public void reloadPluginConfig() {
        reloadConfig();
        this.marketEngine.loadFromConfig(getConfig());
        this.chestManager.loadChestLocation();
        this.customItemManager.load();
        getServer().getScheduler().runTaskAsynchronously(this, () -> {
            this.eliteMobsHook.scanAndRegisterEliteMobsItems(this.customItemManager);
        });
        String apiKey = getConfig().getString("gemini.api_key", "");
        String model = getConfig().getString("gemini.model", "gemini-2.5-flash");
        this.geminiClient = new GeminiClient(apiKey, model);
    }

    public static GuildAIEconomy getInstance() {
        return instance;
    }

    public VaultHook getVaultHook() {
        return vaultHook;
    }

    public DynamicMarketEngine getMarketEngine() {
        return marketEngine;
    }

    public BotChestManager getChestManager() {
        return chestManager;
    }

    public MerchantVillager getMerchantVillager() {
        return merchantVillager;
    }

    public GeminiClient getGeminiClient() {
        return geminiClient;
    }

    public CustomItemManager getCustomItemManager() {
        return customItemManager;
    }

    public EliteMobsHook getEliteMobsHook() {
        return eliteMobsHook;
    }

    public DatabaseManager getDatabaseManager() {
        return databaseManager;
    }

    public GuildRankManager getRankManager() {
        return rankManager;
    }

    public HologramManager getHologramManager() {
        return hologramManager;
    }

    public ItemResolver getItemResolver() {
        return itemResolver;
    }
}
