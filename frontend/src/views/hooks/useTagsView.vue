<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useTagsView } from '@/hooks/web/useTagsView'
import { useRouter } from 'vue-router'

const { push } = useRouter()

const { closeAll, closeLeft, closeRight, closeOther, closeCurrent, refreshPage, setTitle } =
  useTagsView()

const closeAllTabs = () => {
  closeAll(() => {
    push('/tts-flow/index')
  })
}

const closeLeftTabs = () => {
  closeLeft()
}

const closeRightTabs = () => {
  closeRight()
}

const closeOtherTabs = () => {
  closeOther()
}

const refresh = () => {
  refreshPage()
}

const closeCurrentTab = () => {
  closeCurrent(undefined, () => {
    push('/tts-flow/index')
  })
}

const setTabTitle = () => {
  setTitle(new Date().getTime().toString())
}

const setAnalysisTitle = () => {
  setTitle(`TTS工作流-${new Date().getTime().toString()}`, '/tts-flow/index')
}
</script>

<template>
  <ContentWrap title="useTagsView">
    <BaseButton type="primary" @click="closeAllTabs"> 关闭所有标签页 </BaseButton>
    <BaseButton type="primary" @click="closeLeftTabs"> 关闭左侧标签页 </BaseButton>
    <BaseButton type="primary" @click="closeRightTabs"> 关闭右侧标签页 </BaseButton>
    <BaseButton type="primary" @click="closeOtherTabs"> 关闭其他标签页 </BaseButton>
    <BaseButton type="primary" @click="closeCurrentTab"> 关闭当前标签页 </BaseButton>
    <BaseButton type="primary" @click="refresh"> 刷新当前标签页 </BaseButton>
    <BaseButton type="primary" @click="setTabTitle"> 修改当前标题 </BaseButton>
    <BaseButton type="primary" @click="setAnalysisTitle"> 修改分析页标题 </BaseButton>
  </ContentWrap>
</template>
