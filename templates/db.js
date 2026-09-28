const DB_NAME = "ShareRoomDB";
const DB_VERSION = 1;

function getDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = function(event) {
            const db = event.target.result;

            if (!db.objectStoreNames.contains("messages")) {
                const messages = db.createObjectStore("messages", {
                    keyPath: "id",
                    autoIncrement: true
                });
                messages.createIndex("room", "room", { unique: false });
            }

            if (!db.objectStoreNames.contains("files")) {
                const files = db.createObjectStore("files", {
                    keyPath: "id",
                    autoIncrement: true
                });
                files.createIndex("room", "room", { unique: false });
            }
        };

        request.onsuccess = function() {
            resolve(request.result);
        };

        request.onerror = function() {
            reject(request.error);
        };
    });
}

async function saveMessage(message) {
    const db = await getDB();

    return new Promise((resolve, reject) => {
        const transaction = db.transaction("messages", "readwrite");
        const store = transaction.objectStore("messages");

        const request = store.add(message);

        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
    });
}