export interface UserLoginType {
  username: string
  password: string
}

export interface RegisterType {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface UserType {
  username: string
  password?: string
  role?: string
  roleId?: string
  email?: string
  full_name?: string
  is_active?: boolean
  is_superuser?: boolean
  is_admin?: boolean
}

export interface UserInfo {
  username: string
  email?: string
  full_name?: string
  is_active?: boolean
  is_superuser?: boolean
  is_admin?: boolean
}
