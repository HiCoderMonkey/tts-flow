<template>
  <svg fill="currentColor" class="icon" viewBox="0 0 1024 1024" :width="size" :height="size">
    <path d="M474 152m8 0l60 0q8 0 8 8l0 704q0 8-8 8l-60 0q-8 0-8-8l0-704q0-8 8-8Z" p-id="7249" />
    <path d="M168 474m8 0l672 0q8 0 8 8l0 60q0 8-8 8l-672 0q-8 0-8-8l0-60q0-8 8-8Z" p-id="7250" />
  </svg>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      default: '40'
    }
  }
}
</script>
