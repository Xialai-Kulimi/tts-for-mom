export function downloadFile(fileId: string) {
    const link = document.createElement('a')
    link.href = `/api/download/${fileId}`;
  
    link.download = `${fileId}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
  