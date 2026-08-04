import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { FusionResult, SystemStatus } from '../types/fusion'
import { Sensor } from '../types/sensor'

interface FusionState {
  currentFusion: FusionResult | null;
  fusionHistory: FusionResult[];
  sensors: Sensor[];
  systemStatus: SystemStatus;
  isFusing: boolean;
}

const initialState: FusionState = {
  currentFusion: null,
  fusionHistory: [],
  sensors: [],
  systemStatus: {
    status: 'offline',
    activeSensors: 0,
    totalSensors: 0,
    lastFusionTime: '',
    cpuUsage: 0,
    memoryUsage: 0
  },
  isFusing: false,
}

export const fusionSlice = createSlice({
  name: 'fusion',
  initialState,
  reducers: {
    setFusionResult: (state, action: PayloadAction<FusionResult>) => {
      state.currentFusion = action.payload;
      state.fusionHistory = [...state.fusionHistory.slice(-50), action.payload];
    },
    setSensors: (state, action: PayloadAction<Sensor[]>) => {
      state.sensors = action.payload;
    },
    setSystemStatus: (state, action: PayloadAction<SystemStatus>) => {
      state.systemStatus = action.payload;
    },
    setFusingStatus: (state, action: PayloadAction<boolean>) => {
      state.isFusing = action.payload;
    }
  },
})

export const { setFusionResult, setSensors, setSystemStatus, setFusingStatus } = fusionSlice.actions
export default fusionSlice.reducer
