<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElCalendar, ElMessage, ElButton, ElButtonGroup } from 'element-plus'
import api from '../api'
import dayjs from 'dayjs'

const currentDate = ref(new Date())
const heatData = ref<Record<string, number>>({})
const loading = ref(true)

const fetchHeatData = async () => {
  loading.value = true
  try {
    const res = await api.get('/calendar/summary')
    heatData.value = res.data
  } catch (e) {
    console.error(e)
    // Fallback/Mock data if backend fails (e.g. Auth error)
    // allowing the user to see the UI.
    heatData.value = {
        '2026-01-20': 5,
        '2026-01-21': 3, 
        '2026-01-22': 8
    }
  } finally {
    loading.value = false
  }
}


const onDateClick = async (date: Date) => {
    // Format YYYY-MM-DD
    const offset = date.getTimezoneOffset()
    const localDate = new Date(date.getTime() - (offset*60*1000))
    const dateString = localDate.toISOString().split('T')[0]
    
    // 直接增加热度,不需要输入昵称
    try {
        await api.post('/calendar/join', {
            date: dateString,
            nickname: 'anonymous'  // 使用匿名用户
        })
        // 刷新热度数据
        await fetchHeatData()
    } catch (error: any) {
        ElMessage.error('操作失败: ' + (error.response?.data?.detail || error.message))
    }
}


const getHeatLevel = (date: string, dayStr: string) => {
    // dayStr is from scoped slot, usually YYYY-MM-DD
  const count = heatData.value[dayStr] || 0
  if (count === 0) return 0
  if (count < 3) return 1
  if (count < 5) return 2
  if (count < 10) return 3
  return 4 // Max heat
}

const getHeatColor = (level: number) => {
    switch(level) {
        case 0: return 'transparent';
        case 1: return 'rgba(255, 45, 170, 0.3)'; // Warmer pink
        case 2: return 'rgba(255, 0, 150, 0.5)';
        case 3: return 'rgba(255, 0, 100, 0.8)';
        case 4: return '#ff0055'; // Vibrant red-pink
        default: return 'transparent';
    }
}

const getFireSize = (count: number) => {
    if (count <= 1) return '1.2rem'
    if (count <= 3) return '1rem'
    return '0.8rem'
}

const isToday = (dayStr: string) => {
    const today = new Date()
    const d = new Date(dayStr)
    return today.toDateString() === d.toDateString()
}

const selectDate = (val: string) => {
  const d = dayjs(currentDate.value)
  if (val === 'prev-month') {
    currentDate.value = d.subtract(1, 'month').toDate()
  } else if (val === 'next-month') {
    currentDate.value = d.add(1, 'month').toDate()
  } else {
    currentDate.value = new Date()
  }
}

onMounted(() => {
  fetchHeatData()
})
</script>

<template>
  <div class="calendar-wrapper">
    <el-calendar v-model="currentDate">
      <template #header="{ date }">
        <div class="calendar-header">
          <span class="month-title">{{ dayjs(currentDate).format('YYYY年 MM月') }}</span>
          <el-button-group>
            <el-button size="small" @click="selectDate('prev-month')">上个月</el-button>
            <el-button size="small" @click="selectDate('today')">今天</el-button>
            <el-button size="small" @click="selectDate('next-month')">下个月</el-button>
          </el-button-group>
        </div>
      </template>
      <template #date-cell="{ data }">
        <div 
            class="custom-cell" 
            :class="[{ 'is-today': isToday(data.day) }, `heat-${getHeatLevel(data.date, data.day)}`]"
            @click.stop="onDateClick(data.date)"
        >
          <div class="day-number">{{ data.day.split('-').slice(2).join('') }}</div>
          <div class="fire-container" v-if="heatData[data.day]">
              <span 
                v-for="i in (heatData[data.day] > 6 ? 5 : heatData[data.day])" 
                :key="i"
                class="fire-icon"
                :style="{ fontSize: getFireSize(heatData[data.day]) }"
              >🍻</span>
              <span v-if="heatData[data.day] > 6" class="more-indicator">+</span>
          </div>
        </div>
      </template>
    </el-calendar>
  </div>
</template>

<style>
.el-calendar {
    background: rgba(255, 255, 255, 0.03); /* Glass effect */
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    width: 500px;
    height: 410px; /* Further reduced from 450px */
    max-width: 95vw;
    display: flex;
    flex-direction: column;
    overflow: hidden !important;
}

@media (max-width: 600px) {
    .el-calendar {
        width: 100% !important;
        height: auto !important;
        min-height: 500px;
    }
}
.el-calendar__title {
    color: white;
}
.el-calendar-table {
    width: 100% !important;
    height: 100% !important;
    table-layout: fixed !important;
}
.el-calendar-table thead th {
    background: linear-gradient(135deg, #ff00cc, #3333ff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 12px 0;
    opacity: 0.8; /* Slightly more visible but still atmospheric */
}
.calendar-header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px; /* Tightened from 30px */
    width: 100%;
    padding: 2px 5px; /* Tightened vertical padding */
}

@media (max-width: 600px) {
    .el-calendar {
        width: 100% !important;
        height: auto !important;
        min-height: 400px;
    }
    .calendar-header {
        flex-direction: column;
        gap: 2px;
        padding: 4px 5px;
    }
}

.month-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #fff;
}
.el-button-group {
    /* removed padding-right to maintain center balance */
}
.el-button {
    background: transparent !important;
    border: 1px solid rgba(255, 0, 204, 0.4) !important; /* Neon purple border */
    color: rgba(255, 255, 255, 0.8) !important;
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.el-button:hover, .el-button.is-active {
    background: rgba(255, 0, 204, 0.1) !important;
    border-color: #ff00cc !important;
    color: #fff !important;
    box-shadow: 0 0 15px rgba(255, 0, 204, 0.4);
    transform: translateY(-1px);
}
.el-calendar__body {
    padding: 10px 20px 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
}
.el-calendar-table td.is-selected {
    background-color: transparent;
}
.el-calendar-table td {
    border: none;
}
.el-calendar-table .el-calendar-day {
    padding: 0;
    height: 100% !important;
    min-height: 40px; /* Squeezed even more */
    display: flex;
    justify-content: center;
    align-items: center;
}

@media (max-width: 600px) {
    .el-calendar-table .el-calendar-day {
        min-height: 45px;
    }
}
.el-calendar-table:not(.is-range) td.next, .el-calendar-table:not(.is-range) td.prev {
    color: #666;
}
</style>

<style scoped>
.calendar-wrapper {
  padding: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.custom-cell {
  height: 100%;
  width: 100%;
  padding: 2px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  overflow: hidden;
}

.custom-cell.is-today {
    border: 2px solid #ffcc00; /* Gold border for today */
    box-shadow: 0 0 8px rgba(255, 204, 0, 0.4);
    background: rgba(255, 255, 255, 0.05);
}

.custom-cell:hover {
    transform: scale(1.02);
    background-color: rgba(255, 255, 255, 0.15) !important;
}

.day-number {
  font-weight: 800;
  font-size: 0.85rem; /* Reduced from 1.1rem */
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2px;
}

.fire-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, auto); /* Reduced to 2 rows */
    gap: 1px;
    justify-items: center;
    align-items: center;
    width: fit-content;
    margin: 2px auto 0; /* Tightened */
}

.fire-icon {
    line-height: 1;
    transition: all 0.2s ease;
}

.more-indicator {
    font-size: 0.7rem;
    color: #ffaa00;
    font-weight: bold;
}

.heat-level-0 { 
    background-color: rgba(255, 255, 255, 0.05); 
    border: 1px solid rgba(255, 255, 255, 0.02);
}
.heat-level-1 { background-color: rgba(255, 45, 170, 0.4); border: 1px solid rgba(255, 45, 170, 0.6); }
.heat-level-2 { background-color: rgba(255, 0, 150, 0.6); border: 1px solid rgba(255, 0, 150, 0.8); }
.heat-level-3 { background-color: rgba(255, 0, 100, 0.85); border: 1px solid rgba(255, 0, 100, 1); }
.heat-level-4 { 
    background-color: #ff0055; 
    box-shadow: 0 0 20px rgba(255, 0, 85, 0.8);
    border: 2px solid #fff;
}

@media (max-width: 600px) {
    .calendar-wrapper {
        padding: 0.5rem;
    }
    .custom-cell {
        min-width: unset !important;
        min-height: 45px; /* Tightened for mobile */
        padding: 2px;
    }
    .day-number {
        font-size: 0.8rem;
        margin-bottom: 2px;
    }
    .fire-container {
        gap: 1px;
    }
}
</style>
