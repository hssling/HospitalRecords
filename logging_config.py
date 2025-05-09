import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up file handler for general logs
    general_handler = logging.handlers.RotatingFileHandler(
        'logs/hospital_management.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    general_handler.setLevel(logging.INFO)
    general_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    general_handler.setFormatter(general_formatter)

    # Set up file handler for error logs
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/error.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
        'File: %(pathname)s\n'
        'Line: %(lineno)d\n'
        'Function: %(funcName)s\n'
        'Exception: %(exc_info)s'
    )
    error_handler.setFormatter(error_formatter)

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(general_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    # Configure Flask logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(general_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)

    # Log application startup
    app.logger.info('Application started')
    app.logger.info(f'Environment: {app.config["ENV"]}')
    app.logger.info(f'Debug mode: {app.config["DEBUG"]}')

def log_user_activity(user_id, action, details=None):
    """Log user activities"""
    logger = logging.getLogger('user_activity')
    log_message = f'User {user_id}: {action}'
    if details:
        log_message += f' - Details: {details}'
    logger.info(log_message)

def log_patient_activity(patient_id, action, details=None):
    """Log patient-related activities"""
    logger = logging.getLogger('patient_activity')
    log_message = f'Patient {patient_id}: {action}'
    if details:
        log_message += f' - Details: {details}'
    logger.info(log_message)

def log_system_error(error, context=None):
    """Log system errors"""
    logger = logging.getLogger('system_error')
    log_message = f'Error: {str(error)}'
    if context:
        log_message += f' - Context: {context}'
    logger.error(log_message, exc_info=True) 