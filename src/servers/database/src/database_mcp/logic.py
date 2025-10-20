from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine

from models import (
    DBConnectionInput, 
    DBStatusOutput, 
    DBQueryInput, 
    DBQueryOutput
)


def check_connection(req: DBConnectionInput) -> DBStatusOutput:
    """Verifying the status of the database connection."""
    
    try:
        engine: Engine = create_engine(req.db_url)
        with engine.connect() as conn:
            dialect = engine.dialect.name
            driver = engine.dialect.driver
        return DBStatusOutput(connected=True, dialect=dialect, driver=driver, trace_id=req.trace_id)
    except SQLAlchemyError:
        return DBStatusOutput(connected=False, dialect="unknown", driver="unknown", trace_id=req.trace_id)


def execute_query(req: DBQueryInput) -> DBQueryOutput:
    """Executing generic SQL queries."""

    engine: Engine = create_engine(req.db_url)
    try:
        with engine.begin() as conn:
            stmt = text(req.query)
            result = conn.execute(stmt)

            if req.query.strip().lower().startswith("select") and req.return_results:
                rows = [dict(row._mapping) for row in result]
                return DBQueryOutput(success=True, rows=rows, affected_rows=len(rows), trace_id=req.trace_id)

            affected = result.rowcount if result.rowcount is not None else 0
            return DBQueryOutput(success=True, affected_rows=affected, trace_id=req.trace_id)
    except SQLAlchemyError as e:
        return DBQueryOutput(success=False, error=str(e), trace_id=req.trace_id)
