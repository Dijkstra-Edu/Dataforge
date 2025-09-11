from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.location_entity import CreateLocation, UpdateLocation, ReadLocation
from Services.User.location_service import LocationService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/location", tags=["Locations"])

@router.post("/", response_model=ReadLocation)
def create_location(location_create: CreateLocation, session: Session = Depends(get_session)):
    service = LocationService(session)
    logger.info(f"Creating Location: {location_create.city}, {location_create.country}")
    try:
        location = service.create_location(location_create)
        logger.info(f"Created Location with ID: {location.id}")
        return location
    except ValueError as e:
        logger.warning(f"Failed to create location: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating location: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{location_id}", response_model=ReadLocation)
def get_location(location_id: UUID, session: Session = Depends(get_session)):
    service = LocationService(session)
    logger.info(f"Fetching Location with ID: {location_id}")
    location = service.get_location(location_id)
    if not location:
        logger.warning(f"Location not found: {location_id}")
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.get("/", response_model=List[ReadLocation])
def list_locations(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    session: Session = Depends(get_session),
):
    service = LocationService(session)
    logger.info(
        f"Listing Locations: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"city={city}, state={state}, country={country}"
    )
    locations = service.list_locations(
        skip,
        limit,
        sort_by,
        order,
        city,
        state,
        country,
    )
    logger.info(f"Returned {len(locations)} locations")
    return locations

@router.get("/autocomplete/", response_model=List[ReadLocation])
def autocomplete_locations(
    query: str,
    field: str = Query("city", description="Field to search against"),
    limit: int = 10,
    session: Session = Depends(get_session),
):
    service = LocationService(session)
    logger.info(f"Location autocomplete query='{query}' field='{field}' limit={limit}")
    results = service.autocomplete_locations(query, field, limit)
    logger.info(f"Location autocomplete returned {len(results)} results")
    return results

@router.put("/{location_id}", response_model=ReadLocation)
def update_location(
    location_id: UUID, location_update: UpdateLocation, session: Session = Depends(get_session)
):
    service = LocationService(session)
    logger.info(
        f"Updating Location ID: {location_id} with data: {location_update.dict(exclude_unset=True)}"
    )
    try:
        location = service.update_location(location_id, location_update)
        if not location:
            logger.warning(f"Attempted update for missing Location: {location_id}")
            raise HTTPException(status_code=404, detail="Location not found")
        logger.info(f"Updated Location ID: {location.id}")
        return location
    except ValueError as e:
        logger.warning(f"Failed to update location: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating location: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{location_id}", response_model=ReadLocation)
def delete_location(location_id: UUID, session: Session = Depends(get_session)):
    service = LocationService(session)
    logger.info(f"Deleting Location ID: {location_id}")
    location = service.delete_location(location_id)
    if not location:
        logger.warning(f"Attempted delete for missing Location: {location_id}")
        raise HTTPException(status_code=404, detail="Location not found")
    logger.info(f"Deleted Location ID: {location.id}")
    return location