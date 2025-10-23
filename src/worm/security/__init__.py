"""
Security features for Worm Python
"""

from .restricted_builtins import (
    enable_restricted_builtins,
    disable_restricted_builtins,
    get_restriction_status,
    RestrictedBuiltinsError,
)

from .resource_limits import (
    set_cpu_limit,
    set_memory_limit,
    set_file_size_limit,
    set_open_files_limit,
    set_standard_limits,
    get_current_usage,
    ResourceLimitError,
)

from .audit_log import (
    AuditLogger,
    get_audit_logger,
    enable_audit_logging,
    disable_audit_logging,
    read_audit_log,
    search_audit_log,
)

from .filesystem_sandbox import (
    FilesystemSandbox,
    enable_filesystem_sandbox,
    disable_filesystem_sandbox,
    get_sandbox_status,
    FilesystemAccessError,
)

__all__ = [
    # Restricted builtins
    'enable_restricted_builtins',
    'disable_restricted_builtins',
    'get_restriction_status',
    'RestrictedBuiltinsError',
    # Resource limits
    'set_cpu_limit',
    'set_memory_limit',
    'set_file_size_limit',
    'set_open_files_limit',
    'set_standard_limits',
    'get_current_usage',
    'ResourceLimitError',
    # Audit logging
    'AuditLogger',
    'get_audit_logger',
    'enable_audit_logging',
    'disable_audit_logging',
    'read_audit_log',
    'search_audit_log',
    # Filesystem sandbox
    'FilesystemSandbox',
    'enable_filesystem_sandbox',
    'disable_filesystem_sandbox',
    'get_sandbox_status',
    'FilesystemAccessError',
]
