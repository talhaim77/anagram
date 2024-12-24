from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from backend.models.request_log import RequestLog
from backend.models.word import Word
from backend.dependencies import get_db_session
from fastapi import APIRouter, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse

from backend.settings import settings

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


        query_total_request = select(
            func.count(RequestLog.id).label("total_requests"),
        ).where(RequestLog.endpoint == similar_endpoint)

        query_avg_request = select(
            func.avg(RequestLog.processing_time).label("avg_processing_time")
        )

        if from_date or to_date:
            if from_date and from_date.tzinfo is None:
                from_date = from_date.replace(tzinfo=timezone.utc)
            if to_date and to_date.tzinfo is None:
                to_date = to_date.replace(tzinfo=timezone.utc)

            if from_date and to_date and from_date > to_date:
                raise HTTPException(
                    status_code=400, detail="'from' date must be earlier than 'to' date"
                )

            if from_date:
                query_total_request = query_total_request.where(RequestLog.timestamp >= from_date)
                query_avg_request = query_avg_request.where(RequestLog.timestamp >= from_date)
            if to_date:
                query_total_request = query_total_request.where(RequestLog.timestamp <= to_date)
                query_avg_request = query_avg_request.where(RequestLog.timestamp <= to_date)

        total_requests_endpoint = await db.execute(query_total_request)
        total_request_object = total_requests_endpoint.first()
        avg_time_endpoint = await db.execute(query_avg_request)
        avg_time_object = avg_time_endpoint.first()


        total_requests = total_request_object.total_requests
        avg_processing_time_microsec = avg_time_object.avg_processing_time

        return {
            "totalWords": total_words,
            "totalRequests": total_requests,
            "avgProcessingTimeNs": int(avg_processing_time_microsec),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch statistics: {str(e)}"
        )