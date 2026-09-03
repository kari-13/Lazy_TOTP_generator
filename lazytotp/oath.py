from ctypes import CDLL, byref, c_char_p, c_int, c_void_p, c_size_t, create_string_buffer, cast, POINTER,string_at
from pathlib import Path
from typing import Union


class OathError(Exception):
    """Custom exception raised when liboath functions return an error code."""

    def __init__(self, return_code: int):
        self.return_code = return_code
        super().__init__(f"liboath failed with error code: {return_code}")


class OathConverter:
    """A direct Python wrapper to convert byte arrays into standard Base32 strings
    using the liboath library bindings.
    """

    def __init__(self, lib_path: Union[str, Path] = "liboath.dylib"):
        self.lib = CDLL(str(lib_path))
        self.c_lib = CDLL(None)  # Load libc for free()
        self._setup_prototypes()

        # Initialize the underlying C context
        rc = self.lib.oath_init()
        if rc != 0:
            raise OathError(rc)

    def _setup_prototypes(self):
        """Map signatures directly to standard liboath API specifications."""
        self.lib.oath_init.restype = c_int
        self.lib.oath_done.restype = c_int

        # int oath_base32_encode (const char *in, size_t inlen, char **out, size_t *outlen)
        self.lib.oath_base32_encode.argtypes = [
            c_char_p,
            c_size_t,
            POINTER(c_char_p),  # char **out
            POINTER(c_size_t),  # size_t *outlen
        ]
        self.lib.oath_base32_encode.restype = c_int

        # Set up free() function
        self.c_lib.free.argtypes = [c_void_p]
        self.c_lib.free.restype = None

    def bytes_to_base32(self, data_bytes: bytes) -> str:
        """Converts raw binary data into a valid Base32 string.

        Args:
            data_bytes: The raw data or salted byte array to encode.

        Returns:
            An uppercase Base32 encoded text string.
        """
        if not isinstance(data_bytes, bytes):
            raise TypeError("Input data must be provided as bytes")

        # Create a buffer to hold the input data (handles embedded nulls correctly)
        buf = create_string_buffer(data_bytes)

        # Set up reference targets for C to write back memory addresses
        c_out_ptr = c_void_p()
        c_out_len = c_size_t()

        # Call liboath to parse and allocate memory internally
        rc = self.lib.oath_base32_encode(
            buf, len(data_bytes),
            byref(c_out_ptr), byref(c_out_len)
        )

        if rc != 0:
            raise OathError(rc)

        # Grab the string value before cleanup
        encoded_string = c_out_ptr.value.decode("utf-8")

        # Properly free the memory allocated by liboath
        if c_out_ptr.value:
            self.c_lib.free(cast(c_out_ptr, c_void_p))

        return encoded_string

    def __del__(self):
        """Deallocate library bindings on cleanup."""
        if hasattr(self, "lib"):
            rc = self.lib.oath_done()
            if rc != 0:
                # Use warning to avoid exceptions during cleanup
                import warnings
                warnings.warn(f"oath_done() failed with error code: {rc}")
