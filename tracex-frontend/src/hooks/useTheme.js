import { useEffect } from 'react'
import useUIStore from '../store/useUIStore'

export function useTheme() {
  const theme = useUIStore(s => s.theme)
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])
}