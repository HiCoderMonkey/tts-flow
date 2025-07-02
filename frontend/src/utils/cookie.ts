/**
 * Cookie工具类
 */

const TOKEN_KEY = 'access_token'

/**
 * 设置cookie
 * @param name cookie名称
 * @param value cookie值
 * @param days 过期天数
 */
export function setCookie(name: string, value: string, days: number = 7): void {
  debugger
  const expires = new Date()
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000)
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`
}

/**
 * 获取cookie
 * @param name cookie名称
 * @returns cookie值
 */
export function getCookie(name: string): string | null {
  const nameEQ = name + '='
  const ca = document.cookie.split(';')
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i]
    while (c.charAt(0) === ' ') c = c.substring(1, c.length)
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length)
  }
  return null
}

/**
 * 删除cookie
 * @param name cookie名称
 */
export function deleteCookie(name: string): void {
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`
}

/**
 * 设置access_token
 * @param token token值
 * @param days 过期天数
 */
export function setAccessToken(token: string, days: number = 7): void {
  setCookie(TOKEN_KEY, token, days)
}

/**
 * 获取access_token
 * @returns token值
 */
export function getAccessToken(): string | null {
  return getCookie(TOKEN_KEY)
}

/**
 * 删除access_token
 */
export function removeAccessToken(): void {
  deleteCookie(TOKEN_KEY)
}
