import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { Alert } from '../types/sensor'

interface AlertState {
  alerts: Alert[];
  unreadCount: number;
}

const initialState: AlertState = {
  alerts: [],
  unreadCount: 0,
}

export const alertSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    addAlert: (state, action: PayloadAction<Alert>) => {
      state.alerts.unshift(action.payload);
      if (!action.payload.acknowledged) {
        state.unreadCount += 1;
      }
      if (state.alerts.length > 100) {
        state.alerts.pop();
      }
    },
    acknowledgeAlert: (state, action: PayloadAction<string>) => {
      const alert = state.alerts.find(a => a.id === action.payload);
      if (alert && !alert.acknowledged) {
        alert.acknowledged = true;
        state.unreadCount = Math.max(0, state.unreadCount - 1);
      }
    },
    clearAlerts: (state) => {
      state.alerts = [];
      state.unreadCount = 0;
    }
  },
})

export const { addAlert, acknowledgeAlert, clearAlerts } = alertSlice.actions
export default alertSlice.reducer
