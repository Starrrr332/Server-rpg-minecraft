package com.guild.aieconomy;

import com.guild.aieconomy.ai.GeminiClient;
import com.guild.aieconomy.commands.MerchantCommand;
import com.guild.aieconomy.economy.BotChestManager;
import com.guild.aieconomy.economy.DynamicMarketEngine;
import com.guild.aieconomy.economy.VaultHook;
import com.guild.aieconomy.npc.MerchantListener;
import com.guild.aieconomy.npc.MerchantVillager;
import org.bukkit.plugin.java.JavaPlugin;

public class GuildAIEconomy extends JavaPlugin {

    private static GuildAIEconomy instance;
    private VaultHook vaultHook;
    private DynamicMarketEngine marketEngine;
    private BotChestManager chestManager;
    private MerchantVillager merchantVillager;
    private GeminiClient geminiClient;

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();

        // Inicializar economía Vault
        this.vaultHook = new VaultHook(this);
        if (vaultHook.hasEconomy()) {
            getLogger().info("Conectado exitosamente con Vault Economy.");
        } else {
            getLogger().warning("Vault no detectado. Se utilizará simulación económica de prueba.");
        }

        // Inicializar Motor Económico
        this.marketEngine = new DynamicMarketEngine();
        this.marketEngine.loadFromConfig(getConfig());

        // Inicializar Gestor de Cofre del Bot
        this.chestManager = new BotChestManager(this);

        // Inicializar Aldeano NPC
        this.merchantVillager = new MerchantVillager(this);

        // Inicializar Cliente Gemini IA
        String apiKey = getConfig().getString("gemini.api_key", "");
        String model = getConfig().getString("gemini.model", "gemini-1.5-flash");
        this.geminiClient = new GeminiClient(apiKey, model);

        // Registrar Eventos y Comandos
        getServer().getPluginManager().registerEvents(new MerchantListener(this), this);
        if (getCommand("guildai") != null) {
            getCommand("guildai").setExecutor(new MerchantCommand(this));
        }

        getLogger().info("============================================");
        getLogger().info(" GuildAIEconomy v1.0.0 activado correctamente!");
        getLogger().info(" Mercader IA listo para comerciar en la Guild.");
        getLogger().info("============================================");
    }

    @Override
    public void onDisable() {
        getLogger().info("GuildAIEconomy desactivado.");
    }

    public void reloadPluginConfig() {
        reloadConfig();
        this.marketEngine.loadFromConfig(getConfig());
        this.chestManager.loadChestLocation();
        String apiKey = getConfig().getString("gemini.api_key", "");
        String model = getConfig().getString("gemini.model", "gemini-1.5-flash");
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
}
