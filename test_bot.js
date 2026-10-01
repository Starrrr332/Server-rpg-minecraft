const mineflayer = require('mineflayer');
const mcdef = require('minecraft-data');

// Inspeccionar versiones soportadas en mineflayer / minecraft-data
console.log("Versiones conocidas en mineflayer:", Object.keys(mcdef.versionsByMinecraftVersion).filter(v => v.startsWith('1.2')));

const host = '38.97.61.71';
const port = 19618;
const username = 'TestBot_AI';

console.log(`🤖 [TestBot] Intentando conectar a ${host}:${port}...`);

// Desactivar temporalmente la verificación estricta de string de versión si la lanza minecraft-protocol
const bot = mineflayer.createBot({
    host: host,
    port: port,
    username: username,
    version: '1.21.4',
    checkTimeoutInterval: 30000
});

bot.on('login', () => {
    console.log(`✅ [TestBot] ¡CONECTADO AL SERVIDOR como ${bot.username}!`);
    setTimeout(() => {
        bot.chat('!bot hola');
    }, 2000);
    setTimeout(() => {
        bot.quit();
        process.exit(0);
    }, 5000);
});

bot.on('message', (msg) => {
    console.log('[CHAT]', msg.toAnsi());
});

bot.on('error', (err) => {
    console.error('❌ [Error]:', err.message);
});

bot.on('kicked', (reason) => {
    console.log('⚠️ [Kicked]:', reason);
});
