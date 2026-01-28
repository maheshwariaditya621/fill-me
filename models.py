from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    # Metadata
    id = Column(Integer, primary_key=True, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # SECTION A: RESPONDENT DETAILS
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)  # Q2: Email
    age_group = Column(String(50), nullable=False)  # Q3
    household_type = Column(String(50), nullable=False)  # Q4

    # SECTION B: QUICK COMMERCE AWARENESS & USAGE
    awareness = Column(Boolean, nullable=False)  # Q5
    platforms_used = Column(JSON, nullable=False)  # Q6: Multi-select (JSON List)
    other_platform_name = Column(String(255), nullable=True) # New field for "Others"
    most_used_platform = Column(String(100), nullable=False)  # Q7
    usage_frequency = Column(String(50), nullable=False)  # Q8

    # SECTION C: ORDER VALUE & TIME FACTOR
    average_order_value = Column(String(50), nullable=False)  # Q9
    time_saved = Column(String(50), nullable=False)  # Q10

    # SECTION D: HOUSEHOLD CONSUMPTION BEHAVIOUR
    product_categories = Column(JSON, nullable=False)  # Q11: Multi-select (JSON List)
    purchase_frequency_change = Column(String(50), nullable=False)  # Q12
    impulse_buying = Column(String(50), nullable=False)  # Q13: Likert/Agree

    # SECTION E: PRICE SENSITIVITY & LOCAL SHOPS
    price_sensitivity = Column(Integer, nullable=False)  # Q14: 1-5
    price_comparison = Column(String(50), nullable=False)  # Q15
    local_shops_impact = Column(String(50), nullable=False)  # Q16

    # SECTION F: FACTORS INFLUENCING PREFERENCE (Table)
    # Storing each factor as a separate column for easier SQL analysis
    importance_delivery = Column(String(50), nullable=False)
    importance_convenience = Column(String(50), nullable=False)
    importance_pricing = Column(String(50), nullable=False)
    importance_availability = Column(String(50), nullable=False)

    # SECTION G: OVERALL PERCEPTION
    overall_satisfaction = Column(String(50), nullable=False)  # Q18
    future_usage_intent = Column(String(50), nullable=False)  # Q19

    # SECTION H: OPEN-ENDED
    qualitative_response = Column(Text, nullable=True)  # Q20
