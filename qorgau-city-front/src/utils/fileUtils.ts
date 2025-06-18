export function getFileExtension(filename: string) {
  return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 2)
}

export function generateUniqueId() {
  return new Date().getSeconds() + Math.random()
}
