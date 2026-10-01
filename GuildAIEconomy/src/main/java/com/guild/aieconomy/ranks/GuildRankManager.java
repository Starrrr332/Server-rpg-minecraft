package com.guild.aieconomy.ranks;

import com.guild.aieconomy.GuildAIEconomy;
import org.bukkit.ChatColor;
import org.bukkit.entity.Player;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class GuildRankManager {

    public enum GuildRank {
        RANGO_F("§7[Rango F] Novato", 0, 5.0, 0.0),
        RANGO_E("§f[Rango E] Aprendiz", 100, 4.0, 0.0),
        RANGO_D("§a[Rango D] Cazador", 300, 3.0, 2.0),
        RANGO_C("§b[Rango C] Veterano", 700, 2.0, 5.0),
        RANGO_B("§e[Rango B] Élite", 1500, 1.0, 8.0),
        RANGO_A("§c[Rango A] Heroico", 3000, 0.0, 12.0),
        RANGO_S("§6[Rango S] Leyenda", 6000, 0.0, 15.0);

        private final String displayName;
        private final int requiredExp;
        private final double taxPercent;
        private final double shopDiscountPercent;

        GuildRank(String displayName, int requiredExp, double taxPercent, double shopDiscountPercent) {
            this.displayName = displayName;
            this.requiredExp = requiredExp;
            this.taxPercent = taxPercent;
            this.shopDiscountPercent = shopDiscountPercent;
        }

        public String getDisplayName() {
            return displayName;
        }

        public int getRequiredExp() {
            return requiredExp;
        }

        public double getTaxPercent() {
            return taxPercent;
        }

        public double getShopDiscountPercent() {
            return shopDiscountPercent;
        }

        public GuildRank getNextRank() {
            GuildRank[] ranks = values();
            int nextOrdinal = ordinal() + 1;
            if (nextOrdinal < ranks.length) {
                return ranks[nextOrdinal];
            }
            return null;
        }
    }

    public static class PlayerGuildData {
        private GuildRank rank;
        private int exp;

        public PlayerGuildData(GuildRank rank, int exp) {
            this.rank = rank;
            this.exp = exp;
        }

        public GuildRank getRank() {
            return rank;
        }

        public void setRank(GuildRank rank) {
            this.rank = rank;
        }

        public int getExp() {
            return exp;
        }

        public void setExp(int exp) {
            this.exp = exp;
        }
    }

    private final GuildAIEconomy plugin;
    private final Map<UUID, PlayerGuildData> cachedData = new ConcurrentHashMap<>();

    public GuildRankManager(GuildAIEconomy plugin) {
        this.plugin = plugin;
    }

    public PlayerGuildData getPlayerData(Player player) {
        if (player == null) return new PlayerGuildData(GuildRank.RANGO_F, 0);
        return cachedData.computeIfAbsent(player.getUniqueId(), uuid -> loadFromDb(uuid, player.getName()));
    }

    private PlayerGuildData loadFromDb(UUID uuid, String name) {
        Connection conn = plugin.getDatabaseManager().getConnection();
        if (conn == null) return new PlayerGuildData(GuildRank.RANGO_F, 0);

        String sql = "SELECT rank_name, exp FROM guildai_player_ranks WHERE uuid = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, uuid.toString());
            ResultSet rs = pstmt.executeQuery();
            if (rs.next()) {
                String rName = rs.getString("rank_name");
                int exp = rs.getInt("exp");
                GuildRank rank = GuildRank.RANGO_F;
                try {
                    rank = GuildRank.valueOf(rName);
                } catch (Exception ignored) {}
                return new PlayerGuildData(rank, exp);
            }
        } catch (SQLException e) {
            plugin.getLogger().warning("Error cargando rango de " + name + ": " + e.getMessage());
        }
        return new PlayerGuildData(GuildRank.RANGO_F, 0);
    }

    public void addExp(Player player, int expToAdd) {
        if (player == null || expToAdd <= 0) return;
        PlayerGuildData data = getPlayerData(player);
        int newExp = data.getExp() + expToAdd;
        data.setExp(newExp);

        GuildRank current = data.getRank();
        GuildRank next = current.getNextRank();

        boolean rankedUp = false;
        while (next != null && newExp >= next.getRequiredExp()) {
            data.setRank(next);
            current = next;
            next = current.getNextRank();
            rankedUp = true;
        }

        saveToDbAsync(player.getUniqueId(), player.getName(), data);

        if (rankedUp) {
            player.sendMessage("§a§l[GREMIO DE AVENTUREROS] ¡FELICIDADES!");
            player.sendMessage("§e¡Has subido al §f" + data.getRank().getDisplayName() + " §e!");
            player.sendMessage("§7Nuevo beneficio: Descuento en Tienda RPG: §a" + data.getRank().getShopDiscountPercent() + "%");
        }
    }

    private void saveToDbAsync(UUID uuid, String name, PlayerGuildData data) {
        plugin.getServer().getScheduler().runTaskAsynchronously(plugin, () -> {
            Connection conn = plugin.getDatabaseManager().getConnection();
            if (conn == null) return;

            String sql = """
                INSERT INTO guildai_player_ranks (uuid, player_name, rank_name, exp)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(uuid) DO UPDATE SET
                    player_name = excluded.player_name,
                    rank_name = excluded.rank_name,
                    exp = excluded.exp,
                    updated_at = CURRENT_TIMESTAMP;
            """;
            try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
                pstmt.setString(1, uuid.toString());
                pstmt.setString(2, name);
                pstmt.setString(3, data.getRank().name());
                pstmt.setInt(4, data.getExp());
                pstmt.executeUpdate();
            } catch (SQLException e) {
                // SQLite fallback
                String fallbackSql = "REPLACE INTO guildai_player_ranks (uuid, player_name, rank_name, exp) VALUES (?, ?, ?, ?)";
                try (PreparedStatement pstmt2 = conn.prepareStatement(fallbackSql)) {
                    pstmt2.setString(1, uuid.toString());
                    pstmt2.setString(2, name);
                    pstmt2.setString(3, data.getRank().name());
                    pstmt2.setInt(4, data.getExp());
                    pstmt2.executeUpdate();
                } catch (SQLException ignored) {}
            }
        });
    }

    public String getRankProgressFormatted(Player player) {
        PlayerGuildData data = getPlayerData(player);
        GuildRank current = data.getRank();
        GuildRank next = current.getNextRank();

        if (next == null) {
            return "§6★ Nivel Máximo Alcanzado (Leyenda del Gremio)";
        }

        int currentExp = data.getExp();
        int req = next.getRequiredExp();
        int pct = Math.min(100, (currentExp * 100) / req);

        return "§eEXP: §f" + currentExp + " / " + req + " §7(" + pct + "%) §8➔ " + next.getDisplayName();
    }
}
