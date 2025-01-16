class PhotoblocksError(Exception):
    """Base exception class for Photoblocks"""
    pass

class NetworkError(PhotoblocksError):
    """Raised when network operations fail"""
    pass

class ConsensusError(PhotoblocksError):
    """Raised when consensus cannot be reached"""
    pass

class StorageError(PhotoblocksError):
    """Raised when Redis operations fail"""
    pass

class ValidationError(PhotoblocksError):
    """Raised when blockchain validation fails"""
    pass

class AuthenticationError(PhotoblocksError):
    """Raised when authentication fails"""
    pass

class MiningError(PhotoblocksError):
    """Raised when mining operations fail"""
    pass 

class ConfigurationError(PhotoblocksError):
    """Raised when configuration is invalid"""
    pass

class NodeError(PhotoblocksError):
    """Raised when a node operation fails"""
    pass

class TransactionError(PhotoblocksError):
    """Raised when a transaction operation fails"""
    pass

class BlockError(PhotoblocksError):
    """Raised when a block operation fails"""
    pass

class WalletError(PhotoblocksError):
    """Raised when a wallet operation fails"""
    pass

class ResourceError(PhotoblocksError):
    """Raised when a resource is not available"""
    pass

class PortInUseError(NetworkError):
    """Raised when attempting to use an occupied port"""
    pass

class PeerConnectionError(NetworkError):
    """Raised when connection to a peer fails"""
    pass

class DataValidationError(ValidationError):
    """Raised when received data fails validation"""
    pass

class NodeTypeError(ValidationError):
    """Raised when an invalid node type is specified"""
    pass


