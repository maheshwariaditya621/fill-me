from sqlalchemy.orm import Session
import models, schemas
import json

def create_survey_response(db: Session, response: schemas.SurveyResponseCreate):
    # Convert lists to JSON for storage
    db_response = models.SurveyResponse(
        full_name=response.full_name,
        email=response.email,
        age_group=response.age_group.value,
        household_type=response.household_type.value,
        awareness=response.awareness,
        platforms_used=response.platforms_used,  # SQLAlchemy JSON type handles list automatically
        other_platform_name=response.other_platform_name, # New field
        most_used_platform=response.most_used_platform,
        usage_frequency=response.usage_frequency.value,
        average_order_value=response.average_order_value.value,
        time_saved=response.time_saved.value,
        product_categories=response.product_categories, # SQLAlchemy JSON type handles list automatically
        purchase_frequency_change=response.purchase_frequency_change.value,
        impulse_buying=response.impulse_buying.value,
        price_sensitivity=response.price_sensitivity,
        price_comparison=response.price_comparison,
        local_shops_impact=response.local_shops_impact.value,
        importance_delivery=response.importance_delivery.value,
        importance_convenience=response.importance_convenience.value,
        importance_pricing=response.importance_pricing.value,
        importance_availability=response.importance_availability.value,
        overall_satisfaction=response.overall_satisfaction.value,
        future_usage_intent=response.future_usage_intent.value,
        qualitative_response=response.qualitative_response
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def get_responses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SurveyResponse).offset(skip).limit(limit).all()

def get_all_responses_for_export(db: Session):
    return db.query(models.SurveyResponse).all()
