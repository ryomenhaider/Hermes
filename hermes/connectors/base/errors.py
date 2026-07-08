class BaseError(Exception): raise

class ValidationError(BaseError): raise

class TransformationError(BaseError): raise

class HTTPSError(BaseError): raise