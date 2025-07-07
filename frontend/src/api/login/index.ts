import request from '@/axios'
import type { UserLoginType, RegisterType, LoginResponse, UserType } from './types'

interface RoleParams {
  roleName: string
}

// 登录接口，对接后端 /api/v1/auth/login
export const loginApi = (data: UserLoginType): Promise<IResponse<LoginResponse>> => {
  return request.post({ url: '/api/v1/auth/login', data })
}

// 注册接口，对接后端 /api/v1/auth/register
export const registerApi = (data: RegisterType) => {
  return request.post({ url: '/api/v1/auth/register', data })
}

export const loginOutApi = (): Promise<IResponse> => {
  return request.get({ url: '/mock/user/loginOut' })
}

export const getUserListApi = ({ params }: AxiosConfig) => {
  return request.get<{
    code: string
    data: {
      list: UserType[]
      total: number
    }
  }>({ url: '/mock/user/list', params })
}

export const getAdminRoleApi = (
  params: RoleParams
): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
  return request.get({ url: '/api/v1/role/list', params })
}

export const getTestRoleApi = (params: RoleParams): Promise<IResponse<string[]>> => {
  return request.get({ url: '/mock/role/list2', params })
}
