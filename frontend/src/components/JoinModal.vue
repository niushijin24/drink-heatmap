<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElDialog, ElInput, ElButton } from 'element-plus'
import api from '../api'

const props = defineProps<{
  date: string
  visible: boolean
}>()

const emit = defineEmits(['update:visible', 'joined'])

const nickname = ref('')
const loading = ref(false)

const handleJoin = async () => {
  if (!nickname.value) {
    ElMessage.warning('Please enter a nickname')
    return
  }
  
  loading.value = true
  try {
    await api.post('/calendar/join', {
      date: props.date,
      nickname: nickname.value
    })
    ElMessage.success('Joined successfully! 🍻')
    emit('joined')
    handleClose()
  } catch (error: any) {
    ElMessage.error('Failed to join: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  nickname.value = ''
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog
    v-model="props.visible"
    title="Join the Party 🍺"
    width="300px"
    :before-close="handleClose"
    center
    class="join-dialog"
  >
    <div class="content">
      <p>Date: <strong>{{ date }}</strong></p>
      <el-input 
        v-model="nickname" 
        placeholder="Enter your nickname" 
        @keyup.enter="handleJoin"
      />
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button type="primary" :loading="loading" @click="handleJoin">
          Cheers!
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.content {
  text-align: center;
}
p {
  margin-bottom: 1rem;
}
</style>
