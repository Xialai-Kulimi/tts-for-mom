export function downloadFile(fileId: string) {
    const link = document.createElement('a')
    link.href = `/download/${fileId}`;
  
    link.download = `${fileId}.mp3`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
  