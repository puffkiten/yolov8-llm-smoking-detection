
import { ElMessage } from 'element-plus'
import { googleTokenLogin } from 'vue3-google-login'

export function useGoogleLogin() {
  const startGoogleLogin = () => {
    googleTokenLogin().then((response) => {
      const url = `http://127.0.0.1:8000/api/auth/google/callback?access_token=${response.access_token}`
      window.location.href = url
    }).catch(err => {
      console.error('Google Login Error:', err)
      ElMessage.error('Google 登录取消或失败')
    })
  }

  return { startGoogleLogin }
}
