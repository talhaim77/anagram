from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from models.request_log import RequestLog
from models.word import Word
from dependencies import get_db_session
from fastapi import APIRouter, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse

from settings import settings

router = APIRouter()


@router.get("/request_logs")
async def get_all_request_logs(db: AsyncSession = Depends(get_db_session)):
    """
    Retrieve all records from the request_log table.

    Returns:
        A list of request log records.
    """
    try:
        result = await db.execute(select(RequestLog))
        logs = result.scalars().all()
        return logs
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"error": f"Failed to fetch request logs: {str(e)}"})

@router.get("/stats")
async def get_stats(
    from_date: Optional[datetime] = Query(None, alias="from"),
    to_date: Optional[datetime] = Query(None, alias="to"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Retrieve statistics about the service, optionally filtered by time frame.

    Returns:
     - the total number of words in the words table.
     - the total requests to /api/<ver>/similar endpoint.
     - the average processing time of server requests, excluding /stats.
    """
    try:
        similar_endpoint = f"/api/{settings.API_VERSION}/similar"

        query_words = await db.execute(select(func.count(Word.word)))
        total_words = query_words.scalar() or 0

        try:
            total_requests_endpoint = await db.execute(
                select(func.count(RequestLog.id).label("total_requests"))
                .where(RequestLog.endpoint == similar_endpoint)
                .where(RequestLog.timestamp >= from_date if from_date else True)
                .where(RequestLog.timestamp <= to_date if to_date else True)
            )
            total_request_object = total_requests_endpoint.first()
            total_requests = total_request_object.total_requests if total_request_object.total_requests else 0
        except (TypeError, ValueError):
            total_requests = 0

        try:
            avg_time_endpoint = await db.execute(
                select(func.avg(RequestLog.processing_time).label("avg_processing_time"))
                .where(RequestLog.timestamp >= from_date if from_date else True)
                .where(RequestLog.timestamp <= to_date if to_date else True)
            )
            avg_time_object = avg_time_endpoint.first()
            avg_processing_time_ms = avg_time_object.avg_processing_time if avg_time_object.avg_processing_time else 0
        except (TypeError, ValueError):
            avg_processing_time_ms = 0

        return {
            "totalWords": total_words,
            "totalRequests": total_requests,
            "avgProcessingTimeMs": int(avg_processing_time_ms),
        }


    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch statistics: {str(e)}"
        )