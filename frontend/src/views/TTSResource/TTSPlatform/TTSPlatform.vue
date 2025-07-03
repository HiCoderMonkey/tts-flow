<template>
  <ContentWrap>
    <Search :schema="allSchemas.searchSchema" @search="setSearchParams" @reset="setSearchParams" />
    <div class="mb-10px">
      <BaseButton type="primary" @click="AddAction">新增平台</BaseButton>
      <BaseButton :loading="delLoading" type="danger" @click="delData(null)">批量删除</BaseButton>
    </div>
    <Table
      v-model:pageSize="pageSize"
      v-model:currentPage="currentPage"
      :columns="allSchemas.tableColumns"
      :data="dataList"
      :loading="loading"
      :pagination="{ total: total }"
      @register="tableRegister"
    />
  </ContentWrap>
  <Dialog v-model="dialogVisible" :title="dialogTitle">
    <Write
      v-if="actionType !== 'detail'"
      ref="writeRef"
      :current-row="currentRow"
      @submit="handleSubmit"
    />
    <Detail
      v-if="actionType === 'detail'"
      :detail-schema="allSchemas.detailSchema"
      :current-row="currentRow"
    />
    <template #footer>
      <BaseButton
        v-if="actionType !== 'detail'"
        type="primary"
        :loading="saveLoading"
        @click="save"
      >保存</BaseButton>
      <BaseButton @click="dialogVisible = false">关闭</BaseButton>
    </template>
  </Dialog>
</template>

<script setup lang="tsx">
import { ContentWrap } from '@/components/ContentWrap'
import { Search } from '@/components/Search'
import { Dialog } from '@/components/Dialog'
import { useI18n } from '@/hooks/web/useI18n'
import { ElTag } from 'element-plus'
import { Table } from '@/components/Table'
import { getPlatformList, createPlatform, updatePlatform, deletePlatform } from '@/api/ttsResource'
import type { TTSPlatform } from '@/api/ttsResource/types'
import { useTable } from '@/hooks/web/useTable'
import { ref, unref, reactive } from 'vue'
import { CrudSchema, useCrudSchemas } from '@/hooks/web/useCrudSchemas'
import { BaseButton } from '@/components/Button'
import Write from './components/Write.vue'
import Detail from './components/Detail.vue'

const ids = ref<string[]>([])
const { t } = useI18n()

const crudSchemas = reactive<CrudSchema[]>([
  {
    field: 'selection',
    search: { hidden: true },
    form: { hidden: true },
    detail: { hidden: true },
    table: { type: 'selection' }
  },
  {
    field: 'index',
    label: '序号',
    type: 'index',
    search: { hidden: true },
    form: { hidden: true },
    detail: { hidden: true }
  },
  {
    field: 'name',
    label: '平台名称',
    search: { component: 'Input' },
    form: { component: 'Input', colProps: { span: 24 } },
    detail: { span: 24 }
  },
  {
    field: 'type',
    label: '平台类型',
    search: { hidden: true },
    form: {
      component: 'Select',
      componentProps: {
        options: [
          { label: '火山引擎', value: 'volcano' }
        ]
      }
    },
    detail: {},
    table: {
      slots: {
        default: (data: any) => (
          <ElTag>
            {data.row.type === 'volcano' ? '火山引擎' : data.row.type}
          </ElTag>
        )
      }
    }
  },
  {
    field: 'status',
    label: '状态',
    search: { hidden: true },
    form: { component: 'Switch' },
    detail: {},
    table: {
      slots: {
        default: (data: any) => (
          <ElTag type={data.row.status ? 'success' : 'danger'}>
            {data.row.status ? '启用' : '禁用'}
          </ElTag>
        )
      }
    }
  },
  {
    field: 'config',
    label: '平台配置',
    search: { hidden: true },
    table: {hidden: true},
    form: {
      hidden: true,
    },
    detail: { hidden: true }
  },
  {
    field: 'createTime',
    label: '创建时间',
    search: { hidden: true },
    form: { hidden: true },
    detail: {},
    table: {}
  },
  {
    field: 'action',
    width: '200px',
    label: '操作',
    search: { hidden: true },
    form: { hidden: true },
    detail: { hidden: true },
    table: {
      slots: {
        default: (data: any) => (
          <>
            <BaseButton type="primary" onClick={() => action(data.row, 'edit')}>编辑</BaseButton>
            <BaseButton type="danger" onClick={() => delData(data.row)}>删除</BaseButton>
          </>
        )
      }
    }
  }
])

const { allSchemas } = useCrudSchemas(crudSchemas)

const {
  tableRegister,
  tableState,
  tableMethods
} = useTable({
  fetchDataApi: async () => {
    const { currentPage, pageSize } = tableState
    const res = await getPlatformList({ pageIndex: currentPage.value, pageSize: pageSize.value })
    return {
      list: res.data?.list || [],
      total: res.data?.total || 0
    }
  },
  fetchDelApi: async () => {
    const res = await deletePlatform(unref(ids)[0])
    return !!res
  }
})
const { loading, dataList, total, currentPage, pageSize } = tableState
const { getList, getElTableExpose, delList } = tableMethods

const searchParams = ref({})
const setSearchParams = (params: any) => {
  searchParams.value = params
  getList()
}

const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentRow = ref<TTSPlatform | null>(null)
const actionType = ref('')

const AddAction = () => {
  dialogTitle.value = '新增平台'
  currentRow.value = {
    id: '',
    name: '',
    type: '',
    status: true,
    config: {},
    created_at: '',
    updated_at: ''
  }
  dialogVisible.value = true
  actionType.value = ''
}

const delLoading = ref(false)
const delData = async (row: TTSPlatform | null) => {
  const elTableExpose = await getElTableExpose()
  ids.value = row ? [row.id] : elTableExpose?.getSelectionRows().map((v: TTSPlatform) => v.id) || []
  delLoading.value = true
  await delList(unref(ids).length).finally(() => {
    delLoading.value = false
  })
}

const action = (row: TTSPlatform, type: string) => {
  dialogTitle.value = type === 'edit' ? '编辑平台' : '平台详情'
  actionType.value = type
  currentRow.value = row
  dialogVisible.value = true
}

const writeRef = ref<any>()
const saveLoading = ref(false)

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  if (formData) {
    saveLoading.value = true
    let res
    if (actionType.value === 'edit') {
      res = await updatePlatform(formData)
    } else {
      res = await createPlatform(formData)
    }
    if (res) {
      dialogVisible.value = false
      currentPage.value = 1
      getList()
    }
    saveLoading.value = false
  }
}


const handleSubmit = async (formData: any) => {
  saveLoading.value = true
  let res
  if (actionType.value === 'edit') {
    res = await updatePlatform(formData)
  } else {
    res = await createPlatform(formData)
  }
  if (res) {
    dialogVisible.value = false
    currentPage.value = 1
    getList()
  }
  saveLoading.value = false
}
</script>

<style scoped lang="less">
.tts-platform {
  .header {
    margin-bottom: 20px;
  }
}
</style> 