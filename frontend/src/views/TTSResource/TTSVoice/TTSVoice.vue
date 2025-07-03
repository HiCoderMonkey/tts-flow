<template>
  <ContentWrap>
    <Search :schema="allSchemas.searchSchema" @search="setSearchParams" @reset="setSearchParams" />
    <div class="mb-10px">
      <BaseButton type="primary" @click="AddAction">新增音色</BaseButton>
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
import { getVoiceList, createVoice, updateVoice, deleteVoice, getPlatformList } from '@/api/ttsResource'
import type { TTSVoice } from '@/api/ttsResource/types'
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
    label: '音色名称',
    search: { component: 'Input' },
    form: { component: 'Input', colProps: { span: 24 } },
    detail: { span: 24 }
  },
  {
    field: 'platformName',
    label: 'TTS平台',
    search: { component: 'Input' },
    form: { component: 'Input' },
    detail: {}
  },
  {
    field: 'roleId',
    label: '角色ID',
    search: { hidden: true },
    form: { hidden: true },
    detail: {}
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
    const res = await getVoiceList()
    return {
      list: res.data?.list || res.data || [],
      total: res.data?.total || 0
    }
  },
  fetchDelApi: async () => {
    const res = await deleteVoice(unref(ids)[0])
    return !!res
  }
})
const { loading, dataList, total } = tableState
const currentPage = tableState.currentPage
const pageSize = tableState.pageSize
const { getList, getElTableExpose, delList } = tableMethods

const searchParams = ref({})
const setSearchParams = (params: any) => {
  searchParams.value = params
  getList()
}

const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentRow = ref<TTSVoice | null>(null)
const actionType = ref('')
const AddAction = () => {
  dialogTitle.value = '新增音色'
  currentRow.value = {
    id: '',
    name: '',
    platform_id: '',
    language: '',
    gender: '',
    description: '',
    created_at: '',
    updated_at: '',
    extensionJson: ''
  } as any
  dialogVisible.value = true
  saveLoading.value = false
  actionType.value = ''
}

const delLoading = ref(false)
const delData = async (row: TTSVoice | null) => {
  const elTableExpose = await getElTableExpose()
  ids.value = row ? [row.id] : elTableExpose?.getSelectionRows().map((v: TTSVoice) => v.id) || []
  delLoading.value = true
  await delList(unref(ids).length).finally(() => {
    delLoading.value = false
  })
}

const action = (row: TTSVoice, type: string) => {
  dialogTitle.value = type === 'edit' ? '编辑音色' : '音色详情'
  actionType.value = type
  currentRow.value = row
  dialogVisible.value = true
  saveLoading.value = false
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
      res = await updateVoice(formData)
    } else {
      res = await createVoice(formData)
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
    res = await updateVoice(formData)
  } else {
    res = await createVoice(formData)
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
.tts-voice {
  .header {
    margin-bottom: 20px;
  }
}
</style> 