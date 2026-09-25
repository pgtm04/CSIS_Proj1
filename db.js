export const simpleIDB = {
    initialize() {
        return new Promise((resolve, reject) => {
            let request = indexedDB.open('myDatabase')
            request.onupgradeneeded = function() {
                request.result.createObjectStore('myStore')
            }
            request.onsuccess = function() {
                resolve(request.result)
            }
            request.onerror = function() {
                reject(request.error)
            }
        })
    },

    get(key) {
        return new Promise((resolve, reject) => {
            let oRequest = indexedDB.open('myDatabase')
            oRequest.onsuccess = function() {
                let db = oRequest.result
                let tx = db.transaction('myStore', 'readonly')
                let st = tx.objectStore('myStore')
                let gRequest = st.get(key)
                gRequest.onsuccess = function() {
                    resolve(gRequest.result)
                }
                gRequest.onerror = function() {
                    reject(gRequest.error)
                }
               console.log("set")

            }
            oRequest.onerror = function() {
                reject(oRequest.error)
            }
        })
    },

   set (key, value) {
        return new Promise((resolve, reject) => {
        let oRequest = indexedDB.open('myDatabase')
        oRequest.onsuccess = function() {
            let db = oRequest.result
            let tx = db.transaction('myStore', 'readwrite')
            let st = tx.objectStore('myStore')
            let gRequest = st.put(value, key)
            gRequest.onsuccess = function() {
                resolve(gRequest.result)
            }
            gRequest.onerror = function() {
                reject(gRequest.error)
            }
           console.log("set")

        }
        oRequest.onerror = function() {
            reject(oRequest.error)
        }
    })
   },
   remove (key) {
              return new Promise((resolve, reject) => {
        let oRequest = indexedDB.open('myDatabase')
        oRequest.onsuccess = function() {
            let db = oRequest.result
            let tx = db.transaction('myStore', 'readwrite')
            let st = tx.objectStore('myStore')
            let gRequest = st.delete(key)
            gRequest.onsuccess = function() {
                resolve(gRequest.result)
            }
            gRequest.onerror = function() {
                reject(gRequest.error)
            }
        }
        oRequest.onerror = function() {
            reject(oRequest.error)
        }
    })

   }
}
