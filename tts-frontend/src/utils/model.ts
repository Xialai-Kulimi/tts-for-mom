export type SnackBar = {
    status: 'error' | 'warning' | 'success' | 'info',
    message?: string,
    data?: any,
  }
  
export type AudioPair = {
  text: string,
  fileId: string,
}