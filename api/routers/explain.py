from fastapi import APIRouter

router = APIRouter(tags=["Explanation"])

@router.get("/{fusion_id}")
async def explain_fusion(fusion_id: str):
    return {"fusion_id": fusion_id, "explanation": "Data fused correctly."}
