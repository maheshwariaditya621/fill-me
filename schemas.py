from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from enum import Enum
from datetime import datetime

# --- ENUMS FOR STRICT VALIDATION ---

class AgeGroup(str, Enum):
    BELOW_20 = "Below 20"
    RANGE_20_30 = "20–30"
    RANGE_31_40 = "31–40"
    RANGE_41_50 = "41–50"
    ABOVE_50 = "Above 50"

class HouseholdType(str, Enum):
    NUCLEAR = "Nuclear family"
    JOINT = "Joint family"
    LIVING_ALONE = "Living alone"

class Platform(str, Enum):
    ZEPTO = "Zepto"
    BLINKIT = "Blinkit"
    SWIGGY = "Swiggy Instamart"
    BIGBASKET = "BigBasket Now"
    OTHERS = "Others"

class UsageFrequency(str, Enum):
    DAILY = "Daily"
    TWO_THREE_TIMES = "2–3 times a week"
    ONCE_A_WEEK = "Once a week"
    OCCASIONALLY = "Occasionally"
    RARELY = "Rarely"

class OrderValue(str, Enum):
    BELOW_300 = "Below ₹300"
    RANGE_300_600 = "₹300–₹600"
    RANGE_600_1000 = "₹600–₹1000"
    ABOVE_1000 = "Above ₹1000"

class TimeSaved(str, Enum):
    LESS_15 = "Less than 15 minutes"
    RANGE_15_30 = "15–30 minutes"
    RANGE_30_60 = "30–60 minutes"
    MORE_1H = "More than 1 hour"

class ProductCategory(str, Enum):
    GROCERIES = "Groceries & staples"
    DAIRY = "Dairy & bakery"
    SNACKS = "Snacks & beverages"
    PERSONAL_CARE = "Personal care items"
    EMERGENCY = "Emergency / last-minute items"
    ELECTRONICS = "Electronics & accessories"
    HOUSEHOLD = "Household essentials"
    STATIONERY = "Stationery & office supplies"
    MEDICINES = "Medicines & health products"
    PET_SUPPLIES = "Pet supplies"

class PurchaseFreqChange(str, Enum):
    INC_SIGNIFICANT = "Increasing significantly"
    INC_SLIGHT = "Increasing slightly"
    NO_CHANGE = "No change"
    REDUCING = "Reducing"

class LikertAgree(str, Enum):
    STRONGLY_AGREE = "Strongly agree"
    AGREE = "Agree"
    NEUTRAL = "Neutral"
    DISAGREE = "Disagree"
    STRONGLY_DISAGREE = "Strongly disagree"

class PriceComparison(str, Enum):
    MUCH_HIGHER = "Much higher"
    SLIGHTLY_HIGHER = "Slightly higher"
    ALMOST_SAME = "Almost the same"
    SLIGHTLY_LOWER = "Slightly lower"
    MUCH_LOWER = "Much lower"

class LocalShopImpact(str, Enum):
    YES_SIG = "Yes, significantly"
    YES_SOME = "Yes, to some extent"
    NO_CHANGE = "No change"
    INCREASED = "Increased visits to local shops"

class ImportanceRating(str, Enum):
    VERY_IMP = "Very Important"
    IMPORTANT = "Important"
    NEUTRAL = "Neutral"
    NOT_IMP = "Not Important"

class Satisfaction(str, Enum):
    VERY_SAT = "Very satisfied"
    SATISFIED = "Satisfied"
    NEUTRAL = "Neutral"
    DISSATISFIED = "Dissatisfied"
    VERY_DISSATISFIED = "Very dissatisfied"

class FutureUsage(str, Enum):
    YES = "Yes"
    NO = "No"
    NOT_SURE = "Not sure"

# --- PYDANTIC MODELS ---

class SurveyResponseBase(BaseModel):
    # Section A
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    age_group: AgeGroup
    household_type: HouseholdType

    # Section B
    awareness: bool
    platforms_used: List[str]
    other_platform_name: Optional[str] = None
    most_used_platform: str
    usage_frequency: UsageFrequency

    # Section C
    average_order_value: OrderValue
    time_saved: TimeSaved

    # Section D
    product_categories: List[str]
    purchase_frequency_change: PurchaseFreqChange
    impulse_buying: LikertAgree

    # Section E
    price_sensitivity: int = Field(..., ge=1, le=5)
    price_comparison: PriceComparison
    local_shops_impact: LocalShopImpact

    # Section F
    importance_delivery: ImportanceRating
    importance_convenience: ImportanceRating
    importance_pricing: ImportanceRating
    importance_availability: ImportanceRating

    # Section G
    overall_satisfaction: Satisfaction
    future_usage_intent: FutureUsage

    # Section H
    qualitative_response: Optional[str] = None

    @validator("platforms_used", "product_categories")
    def must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Must select at least one option")
        return v


class SurveyResponseCreate(SurveyResponseBase):
    pass


class SurveyResponseOut(SurveyResponseBase):
    id: int
    submitted_at: datetime

    class Config:
        from_attributes = True
