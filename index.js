require('dotenv').config()
const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const Binance = require('node-binance-api');
const binance = new Binance().options({
    APIKEY: process.env.APIKEY,
    APISECRET: process.env.APISECRET
});


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});




io.on('connection', (socket) => {
    console.log('a user connected');
});


binance.websockets.trades(["BTCUSDT", "BTCBUSD"], (trades) => {
    let { e: eventType, E: eventTime, s: symbol, p: price, q: quantity, m: maker, a: tradeId } = trades;
    console.info(symbol + " trade update. price: " + price + ", quantity: " + quantity + ", maker: " + maker);
    io.sockets.emit("price", price);
});

