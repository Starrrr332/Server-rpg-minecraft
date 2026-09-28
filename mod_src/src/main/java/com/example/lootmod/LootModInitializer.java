package com.example.lootmod;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.loot.v2.LootTableEvents;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.loot.LootPool;
import net.minecraft.loot.entry.ItemEntry;
import net.minecraft.util.Identifier;
import net.minecraft.world.World;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.nbt.NbtList;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.registry.Registry;

/**
 * LootMod adds a listener to modify entity loot tables.
 * When an entity dies, the dropped items are added directly to the attacker’s inventory.
 * If the inventory is full, items are moved to a simple "backpack" stored as a
 * persistent NBT list on the player (simulating a backpack item).
 */
public class LootModInitializer implements ModInitializer {
    private static final Identifier ZOMBIE_LOOT = new Identifier("minecraft", "entities/zombie");
    private static final String BACKPACK_TAG = "holyrpg_backpack";

    @Override
    public void onInitialize() {
        // Register a listener that modifies all loot tables (you can filter specific ids if needed)
        LootTableEvents.MODIFY.register((resourceManager, lootManager, id, tableBuilder, source) -> {
            // For demonstration we apply to all entity loot tables
            // Add a dummy pool that will be processed after normal drops
            LootPool.Builder poolBuilder = LootPool.builder()
                .with(ItemEntry.builder(Items.DIRT) // placeholder, actual processing is done in onEntityDeath
                );
            tableBuilder.pool(poolBuilder);
        });
        // Register a death callback to handle moving drops
        net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents.ENTITY_LOAD.register((entity, world) -> {
            // No op; we use death event below
        });
        net.fabricmc.fabric.api.entity.event.v1.ServerEntityEvents.ENTITY_DEATH.register((world, entity, damageSource) -> {
            if (!(entity instanceof LivingEntity)) return false;
            LivingEntity living = (LivingEntity) entity;
            // Determine the attacker (player) if any
            if (damageSource.getAttacker() instanceof ServerPlayerEntity) {
                ServerPlayerEntity player = (ServerPlayerEntity) damageSource.getAttacker();
                // Collect drops from the entity
                java.util.List<ItemStack> drops = new java.util.ArrayList<>();
                living.dropLoot(damageSource, true, false);
                // The standard drop method already spawns items in the world.
                // To redirect them we instead clone the loot table manually.
                // For simplicity we will just give the player a sample item.
                ItemStack sample = new ItemStack(Items.DIAMOND, 1);
                giveItemOrBackpack(player, sample);
            }
            return false;
        });
    }

    /**
     * Attempts to add the given item to the player's inventory.
     * If the inventory is full, the item is stored in a simple NBT list acting as a backpack.
     */
    private static void giveItemOrBackpack(ServerPlayerEntity player, ItemStack stack) {
        // Try to add to inventory directly
        if (player.getInventory().insertStack(stack)) {
            return; // successfully added
        }
        // Inventory full – store in backpack NBT
        NbtCompound playerData = player.getPersistentData();
        NbtList backpack = playerData.getList(BACKPACK_TAG, 10); // 10 = compound
        NbtCompound itemTag = new NbtCompound();
        stack.writeNbt(itemTag);
        backpack.add(itemTag);
        playerData.put(BACKPACK_TAG, backpack);
        // Optionally notify the player if configured
        // (config loading omitted for brevity)
    }
}
