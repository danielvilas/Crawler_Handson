// Step 2 – Insert news manually with mongosh
// Run: mongosh "mongodb://root:example@localhost:27017/" --file 02-insert-manual.js

use("news_db");

db.articles.insertOne({
  title:   "El paro baja en octubre",
  url:     "https://elpais.com/economia/2024/10/01/paro.html",
  np_name: "elpais",
  date:    new Date("2024-10-01"),
  body:    "El número de parados registrados bajó en octubre...",
  tags:    ["economía", "trabajo"]
});

print("Inserted. Total docs:", db.articles.countDocuments());
db.articles.find({}, { title: 1, np_name: 1, _id: 0 }).forEach(printjson);
