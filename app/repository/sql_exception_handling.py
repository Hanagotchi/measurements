from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError, IntegrityError, NoResultFound
from fastapi import status, HTTPException
import logging

logger = logging.getLogger("app")
logger.setLevel("DEBUG")


def handle_common_errors(err):
    if isinstance(err, IntegrityError):
        if isinstance(err.orig, UniqueViolation):
            parsed_error = err.orig.pgerror.split("\n")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": parsed_error[0],
                    "detail": parsed_error[1]
                })

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=format(err))

    if isinstance(err, PendingRollbackError):
        logger.warning(format(err))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=format(err)
        )

    if isinstance(err, NoResultFound):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=format(err)
        )

    logger.error(format(err))
    raise err


def withSQLExceptionsHandle(async_mode: bool = False):
    def decorator(func):
        async def handleAsyncSQLException(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_common_errors(err)

        def handleSyncSQLException(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_common_errors(err)

        return (
            handleAsyncSQLException if async_mode else handleSyncSQLException
        )

    return decorator
