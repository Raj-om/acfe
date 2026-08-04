import { configureStore } from '@reduxjs/toolkit'
import fusionReducer from './fusionSlice'
import alertReducer from './alertSlice'

export const store = configureStore({
  reducer: {
    fusion: fusionReducer,
    alerts: alertReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
