import logging
from typing import Dict, Optional, List
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from acfe.core.domain.value_objects import SeverityLevel, Location
from acfe.core.domain.events import AlertGeneratedEvent
from acfe.core.ports.repositories import IAlertRepository
from acfe.core.ports.services import IEventPublisher

logger = logging.getLogger(__name__)

# Dummy class for typing
class FusionResult:
    def __init__(self, result_id: str, confidence: float, locations: List[Location] = None):
        self.result_id = result_id
        self.confidence = confidence
        self.locations = locations or []

class GenerateAlertUseCase:
    """Use case for generating alerts from fusion results."""
    
    def __init__(self, 
                 alert_repo: IAlertRepository, 
                 event_publisher: IEventPublisher,
                 dedup_window_minutes: int = 5):
        self.alert_repo = alert_repo
        self.event_publisher = event_publisher
        self.dedup_window_minutes = dedup_window_minutes
        
    def execute(self, 
                result: FusionResult, 
                alert_thresholds: Dict[SeverityLevel, float]) -> Optional[AlertGeneratedEvent]:
        """
        Evaluates a fusion result and generates an alert if necessary.
        
        Steps:
        1. Evaluate against thresholds
        2. Determine severity
        3. Create AlertEvent
        4. Deduplicate
        5. Save via repository
        6. Publish event
        """
        logger.info(f"Evaluating fusion result {result.result_id} for alerts")
        
        # 1 & 2. Determine severity level
        severity = None
        # Sort thresholds descending by severity string or custom logic
        # For simplicity, check from highest to lowest severity
        for level in [SeverityLevel.CRITICAL, SeverityLevel.HIGH, SeverityLevel.MEDIUM, SeverityLevel.LOW, SeverityLevel.INFO]:
            if level in alert_thresholds and result.confidence >= alert_thresholds[level]:
                severity = level
                break
                
        if not severity:
            logger.debug(f"Fusion result confidence {result.confidence} below all thresholds.")
            return None
            
        logger.info(f"Threshold met for {severity.value}. Confidence: {result.confidence}")
        
        # 3. Create AlertEvent
        primary_location = None
        if result.locations:
            loc = result.locations[0]
            primary_location = {"lat": loc.lat, "lon": loc.lon, "alt": loc.alt}
            
        alert_event = AlertGeneratedEvent(
            alert_id=uuid4(),
            severity=severity.value,
            confidence=result.confidence,
            location=primary_location
        )
        
        # 4. Deduplicate
        # Look for similar unacknowledged alerts in the repository
        recent_alerts = self.alert_repo.get_unacknowledged()
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=self.dedup_window_minutes)
        
        for existing in recent_alerts:
            if existing.severity == severity.value and existing.timestamp > cutoff_time:
                # Basic dedup based on severity and time; could be enhanced with location
                logger.info("Similar alert generated recently. Deduplicating.")
                return None
                
        # 5. Save alert via repository
        try:
            self.alert_repo.create(alert_event)
        except Exception as e:
            logger.error(f"Failed to save alert to repository: {e}")
            raise
            
        # 6. Publish event
        try:
            self.event_publisher.publish(alert_event)
        except Exception as e:
            logger.error(f"Failed to publish AlertGeneratedEvent: {e}")
            # Continuing since the alert was saved
            
        logger.info(f"Alert {alert_event.alert_id} generated successfully")
        return alert_event
