
import { ElMessage } from 'element-plus'
import { googleTokenLogin } from 'vue3-google-login'
import { buildApiUrl } from '@/utils/http'

export function useGoogleLogin() {
  const startGoogleLogin = () => {
    googleTokenLogin().then((response) => {
      const url = buildApiUrl(`/api/auth/google/callback?access_token=${response.access_token}`)
      window.location.href = url
    }).catch(err => {
      console.error('Google Login Error:', err)
      ElMessage.error('Google 登录取消或失败')
    })
  }

  return { startGoogleLogin }
}
