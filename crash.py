const { Telegraf, Markup } = require("telegraf");

const bot = new Telegraf("8550954767:AAFD-u5tdLHFshIPK6aQQzAJCn6-Ax1azCA");

const OWNER_ID = 8452357204; // owner telegram id
let botStopped = false;
let premiumUsers = new Set();
let waitingTime = new Set();

// /start
bot.start((ctx) => {
  const id = ctx.from.id;

  ctx.reply(
    `👋 Welcome to Signal Bot\n\n🆔 Your User ID: ${id}`,
    Markup.keyboard([["/signal"]]).resize()
  );
});

// /signal
bot.command("signal", (ctx) => {
  const id = ctx.from.id;

  if (botStopped && !premiumUsers.has(id) && id !== OWNER_ID) {
    return ctx.reply("❌ Bot restricted.\nActivate Premium to continue.");
  }

  waitingTime.add(id);
  ctx.reply("Please send the current time (Example: 10:16)");
});

// Time input
bot.on("text", (ctx) => {
  const id = ctx.from.id;
  if (!waitingTime.has(id)) return;

  const time = ctx.message.text;
  const [h, m] = time.split(":").map(Number);
  if (isNaN(h) || isNaN(m)) return ctx.reply("Invalid time format!");

  const date = new Date();
  date.setHours(h);
  date.setMinutes(m + 5);

  const newTime =
    date.getHours().toString().padStart(2, "0") +
    ":" +
    date.getMinutes().toString().padStart(2, "0");

  waitingTime.delete(id);

  ctx.reply(
    `⏰ Your Time: ${time}\n⏰ Signal Time: ${newTime}\n\n⚠️ Bet on the round AFTER this time.`
  );
});

// /stop (Owner)
bot.command("stop", (ctx) => {
  if (ctx.from.id !== OWNER_ID) return;
  botStopped = true;
  ctx.reply("🚫 Bot stopped for free users.");
});

// /premium <id>
bot.command("premium", (ctx) => {
  if (ctx.from.id !== OWNER_ID) return;

  const id = Number(ctx.message.text.split(" ")[1]);
  if (!id) return ctx.reply("Usage: /premium <userid>");

  premiumUsers.add(id);
  ctx.reply(`✅ Premium activated for ${id}`);
  bot.telegram.sendMessage(id, "✅ Premium Activated! Enjoy the bot.");
});

bot.launch();
