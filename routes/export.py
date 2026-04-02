from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
from modules.exporter import export_to_excel
from schemas import ExportData

export_router = APIRouter(prefix="/export", tags=["export"])


@export_router.post('/')
async def export(data: ExportData):
    try:
        from datetime import datetime
        filename = f"analysis_{datetime.today().strftime('%Y%m%d%H%M%S')}.xlsx"

        analysis = [tuple(item) for item in data.analysis]
        entities = [tuple(item) for item in data.entities]

        excel_file = export_to_excel(analysis, entities)
        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        print(f"Export error: {e}")
        raise HTTPException(status_code=500, detail="Error during export")