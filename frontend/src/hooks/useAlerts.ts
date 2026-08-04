import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/store';
import { acknowledgeAlert, clearAlerts } from '../store/alertSlice';

export const useAlerts = () => {
  const dispatch = useDispatch();
  const { alerts, unreadCount } = useSelector((state: RootState) => state.alerts);

  const handleAcknowledge = (id: string) => {
    dispatch(acknowledgeAlert(id));
  };

  const handleClear = () => {
    dispatch(clearAlerts());
  };

  return { alerts, unreadCount, handleAcknowledge, handleClear };
};
