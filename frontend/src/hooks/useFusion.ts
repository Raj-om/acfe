import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/store';
import { triggerManualFusion } from '../api/fusionApi';
import { setFusingStatus, setFusionResult } from '../store/fusionSlice';

export const useFusion = () => {
  const dispatch = useDispatch();
  const { currentFusion, fusionHistory, isFusing, systemStatus } = useSelector((state: RootState) => state.fusion);

  const runFusion = async () => {
    dispatch(setFusingStatus(true));
    try {
      const result = await triggerManualFusion();
      dispatch(setFusionResult(result));
    } catch (error) {
      console.error("Fusion failed", error);
    } finally {
      dispatch(setFusingStatus(false));
    }
  };

  return { currentFusion, fusionHistory, isFusing, systemStatus, runFusion };
};
