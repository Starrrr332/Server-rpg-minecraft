const mineflayer = require('mineflayer');

const host = '38.97.61.71';
const port = 19618;
const username = 'TestBot_AI';

console.log(`🤖 [TestBot] Conectándose al servidor de Minecraft ${host}:${port} como '${username}' (v1.20.6)...`);

const bot = mineflayer.createBot({
    host: host,
    port: port,
    username: username,
    version: '1.20.6'
});

bot.on('login', () => {
    console.log(`✅ [TestBot] ¡INGRESÓ EXITOSAMENTE AL SERVIDOR como ${bot.username}!`);
    
    setTimeout(() => {
        console.log("➡️ [TestBot] Ejecutando comando /guildai...");
        bot.chat('/guildai');
    }, 3000);

    setTimeout(() => {
        console.log("➡️ [TestBot] Ejecutando comando /guildai prices...");
        bot.chat('/guildai prices');
    }, 6000);

    setTimeout(() => {
        console.log("➡️ [TestBot] Enviando mensaje por chat: !bot hola...");
        bot.chat('!bot hola');
    }, 9000);

    setTimeout(() => {
        console.log("➡️ [TestBot] Consultando precios: !bot precio diamante...");
        bot.chat('!bot precio diamante');
    }, 13000);

    setTimeout(() => {
        console.log("👋 [TestBot] Pruebas finalizadas con éxito. Desconectando bot...");
        bot.quit();
        process.exit(0);
    }, 17000);
});

bot.on('message', (message) => {
    console.log(`[CHAT SERVIDOR] ${message.toAnsi()}`);
});

bot.on('error', (err) => {
    console.error('❌ [TestBot Error]:', err.message);
});

bot.on('kicked', (reason) => {
    console.log('⚠️ [TestBot Kicked]:', reason);
});
