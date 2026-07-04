class AgentError(Exception):
    """Base exception for AI-Recruit-Agent"""
    pass

class ProfileParseError(AgentError):
    """Raised when there is an error parsing the candidate profile"""
    pass

class OfferParseError(AgentError):
    """Raised when there is an error parsing the job offer"""
    pass

class OllamaConnectionError(AgentError):
    """Raised when the connection to Ollama fails"""
    pass

class AnalysisError(AgentError):
    """Raised when the analysis process fails"""
    pass
