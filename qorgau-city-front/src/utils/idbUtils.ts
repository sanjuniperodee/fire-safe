import { openDB, type DBSchema, type IDBPDatabase } from 'idb';

interface MyDB extends DBSchema {
  mediaCache: {
    key: string;
    value: Blob;
  };
}

let db: IDBPDatabase<MyDB>;

export async function initDB() {
  db = await openDB<MyDB>('mediaCache', 1, {
    upgrade(db) {
      db.createObjectStore('mediaCache');
    },
  });
}

export async function cacheMedia(url: string, blob: Blob) {
  if (!db) await initDB();
  await db.put('mediaCache', blob, url);
}

export async function getCachedMedia(url: string): Promise<Blob | undefined> {
  if (!db) await initDB();
  return db.get('mediaCache', url);
}

export const getCachedUrl = async (url: string) => {
  const cachedBlob = await getCachedMedia(url);
  if (cachedBlob) {
    return URL.createObjectURL(cachedBlob);
  }
  const response = await fetch(url);
  const blob = await response.blob();
  await cacheMedia(url, blob);
  return URL.createObjectURL(blob);
}