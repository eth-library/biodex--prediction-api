from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import AnonRateThrottle

class AnonBurstRateThrottle(AnonRateThrottle):
    scope = 'anon_burst'

class AnonSustainedRateThrottle(AnonRateThrottle):
    scope = 'anon_sustained'

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
