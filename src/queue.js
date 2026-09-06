const { Queue } = require("bullmq");
const connection = { url: process.env.REDIS_URL || "redis://localhost:6379" };
const notificationQueue = new Queue("notifications", { connection });
module.exports = { notificationQueue, connection };