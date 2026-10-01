package com.guild.aieconomy.economy;

import org.bukkit.Material;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.File;
import java.sql.*;
import java.util.HashMap;
import java.util.Map;

public class DatabaseManager {

    private final JavaPlugin plugin;
    private Connection connection;

    public DatabaseManager(JavaPlugin plugin) {
        this.plugin = plugin;
        initDatabase();
    }

    public void initDatabase() {
        try {
            FileConfiguration config = plugin.getConfig();
            boolean useMySQL = config.getBoolean("database.use_mysql", false);

            if (useMySQL) {
                String host = config.getString("database.host", "38.97.61.71");
                int port = config.getInt("database.port", 3306);
                String dbName = config.getString("database.database", "s63121_mc_accounts");
                String user = config.getString("database.user", "u63121_YEHsFXzBrp");
                String pass = config.getString("database.password", "U^TN^^AotPQeST0hg+Vc0KfF");

                String url = "jdbc:mysql://" + host + ":" + port + "/" + dbName + "?useSSL=false&autoReconnect=true";
                this.connection = DriverManager.getConnection(url, user, pass);
                plugin.getLogger().info("[GuildAIEconomy] ¡Conectado exitosamente a la Base de Datos MySQL remota!");
            } else {
                File dbFile = new File(plugin.getDataFolder(), "economy_database.db");
                String url = "jdbc:sqlite:" + dbFile.getAbsolutePath();
                this.connection = DriverManager.getConnection(url);
                plugin.getLogger().info("[GuildAIEconomy] ¡Conectado a la Base de Datos SQLite local!");
            }

            createTables();
            insertDefaultCatalogIfEmpty();
        } catch (SQLException e) {
            plugin.getLogger().warning("[GuildAIEconomy] Usando SQLite local por falta de conexión remota: " + e.getMessage());
            initFallbackSQLite();
        }
    }

    private void initFallbackSQLite() {
        try {
            File dbFile = new File(plugin.getDataFolder(), "economy_database.db");
            String url = "jdbc:sqlite:" + dbFile.getAbsolutePath();
            this.connection = DriverManager.getConnection(url);
            createTables();
            insertDefaultCatalogIfEmpty();
        } catch (SQLException ex) {
            plugin.getLogger().severe("[GuildAIEconomy] Error en base de datos SQLite: " + ex.getMessage());
        }
    }

    private void createTables() throws SQLException {
        if (connection == null || connection.isClosed()) return;

        try (Statement stmt = connection.createStatement()) {
            stmt.executeUpdate("""
                CREATE TABLE IF NOT EXISTS guildai_market_items (
                    id VARCHAR(64) PRIMARY KEY,
                    material VARCHAR(64) NOT NULL,
                    item_name VARCHAR(128),
                    base_price DOUBLE NOT NULL,
                    stock INT NOT NULL DEFAULT 64,
                    demand INT NOT NULL DEFAULT 0,
                    category VARCHAR(32) DEFAULT 'VANILLA'
                );
            """);

            stmt.executeUpdate("""
                CREATE TABLE IF NOT EXISTS guildai_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name VARCHAR(32) NOT NULL,
                    action VARCHAR(10) NOT NULL,
                    item_id VARCHAR(64) NOT NULL,
                    amount INT NOT NULL,
                    total_price DOUBLE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """);
        }
    }

    public Map<Material, Double> loadExtensiveItems() {
        Map<Material, Double> prices = new HashMap<>();
        if (connection == null) return prices;

        String query = "SELECT material, base_price FROM guildai_market_items";
        try (PreparedStatement pstmt = connection.prepareStatement(query);
             ResultSet rs = pstmt.executeQuery()) {
            while (rs.next()) {
                String matStr = rs.getString("material");
                double price = rs.getDouble("base_price");
                Material mat = Material.matchMaterial(matStr);
                if (mat != null) {
                    prices.put(mat, price);
                }
            }
        } catch (SQLException e) {
            plugin.getLogger().warning("Error al cargar catálogo de BD: " + e.getMessage());
        }
        return prices;
    }

    public void insertDefaultCatalogIfEmpty() {
        if (connection == null) return;

        try {
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM guildai_market_items");
            if (rs.next() && rs.getInt(1) == 0) {
                plugin.getLogger().info("[GuildAIEconomy] Poblando base de datos con un catálogo extenso de más de 20 ítems...");
                
                String insertSQL = "INSERT INTO guildai_market_items (id, material, item_name, base_price, stock, category) VALUES (?, ?, ?, ?, ?, ?)";
                try (PreparedStatement pstmt = connection.prepareStatement(insertSQL)) {
                    
                    Object[][] defaultItems = {
                        // Minerales & Valiosos
                        {"diamond", "DIAMOND", "Diamante", 120.0, 128, "MINERALS"},
                        {"netherite_ingot", "NETHERITE_INGOT", "Lingote de Netherita", 750.0, 32, "MINERALS"},
                        {"emerald", "EMERALD", "Esmeralda", 60.0, 200, "MINERALS"},
                        {"gold_ingot", "GOLD_INGOT", "Lingote de Oro", 30.0, 300, "MINERALS"},
                        {"iron_ingot", "IRON_INGOT", "Lingote de Hierro", 12.0, 500, "MINERALS"},
                        {"copper_ingot", "COPPER_INGOT", "Lingote de Cobre", 5.0, 600, "MINERALS"},
                        {"lapis_lazuli", "LAPIS_LAZULI", "Lapislázuli", 8.0, 400, "MINERALS"},
                        {"amethyst_shard", "AMETHYST_SHARD", "Fragmento de Amatista", 15.0, 250, "MINERALS"},

                        // Bloques de Construcción RPG
                        {"oak_log", "OAK_LOG", "Tronco de Roble", 2.0, 1000, "BUILDING"},
                        {"stone", "STONE", "Piedra", 1.0, 2000, "BUILDING"},
                        {"deepslate", "DEEPSLATE", "Pizarra Profunda", 1.5, 1500, "BUILDING"},
                        {"obsidian", "OBSIDIAN", "Obsidiana", 25.0, 200, "BUILDING"},
                        {"crying_obsidian", "CRYING_OBSIDIAN", "Obsidiana Llorosa", 40.0, 100, "BUILDING"},

                        // Tesoros del Nether & End
                        {"nether_star", "NETHER_STAR", "Estrella del Nether", 2500.0, 10, "SPECIAL"},
                        {"elytra", "ELYTRA", "Élitros", 3500.0, 5, "SPECIAL"},
                        {"dragon_breath", "DRAGON_BREATH", "Aliento de Dragón", 150.0, 50, "SPECIAL"},
                        {"shulker_shell", "SHULKER_SHELL", "Caparazón de Shulker", 180.0, 80, "SPECIAL"},
                        {"totem_of_undying", "TOTEM_OF_UNDYING", "Tótem de Inmortalidad", 800.0, 25, "SPECIAL"},

                        // Comida & Consumibles
                        {"golden_apple", "GOLDEN_APPLE", "Manzana Dorada", 75.0, 100, "FOOD"},
                        {"enchanted_golden_apple", "ENCHANTED_GOLDEN_APPLE", "Manzana de Notch", 1500.0, 8, "FOOD"},
                        {"cooked_beef", "COOKED_BEEF", "Filete Cocinado", 4.0, 800, "FOOD"},
                        {"golden_carrot", "GOLDEN_CARROT", "Zanahoria Dorada", 15.0, 300, "FOOD"}
                    };

                    for (Object[] row : defaultItems) {
                        pstmt.setString(1, (String) row[0]);
                        pstmt.setString(2, (String) row[1]);
                        pstmt.setString(3, (String) row[2]);
                        pstmt.setDouble(4, (Double) row[3]);
                        pstmt.setInt(5, (Integer) row[4]);
                        pstmt.setString(6, (String) row[5]);
                        pstmt.addBatch();
                    }
                    pstmt.executeBatch();
                }
            }
        } catch (SQLException e) {
            plugin.getLogger().warning("Error al poblar catálogo por defecto: " + e.getMessage());
        }
    }

    public void logTransaction(String playerName, String action, String itemId, int amount, double totalPrice) {
        if (connection == null) return;

        String sql = "INSERT INTO guildai_transactions (player_name, action, item_id, amount, total_price) VALUES (?, ?, ?, ?, ?)";
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, playerName);
            pstmt.setString(2, action);
            pstmt.setString(3, itemId);
            pstmt.setInt(4, amount);
            pstmt.setDouble(5, totalPrice);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            plugin.getLogger().warning("Error guardando transacción en BD: " + e.getMessage());
        }
    }

    public Connection getConnection() {
        return connection;
    }

    public void close() {
        try {
            if (connection != null && !connection.isClosed()) {
                connection.close();
            }
        } catch (SQLException ignored) {}
    }
}
