import struct
import zlib
from Crypto.Cipher import AES

SAVE_KEY_DICT = {
    0x001: b'C5VbD9SJxe4FhK7wnWxy_LVSuHfbQjAU',  # C5VbD9SJxe4FhK7wnWxy_LVSuHfbQjAUHBLxstRi3JBRc5eZVK6jQm9YGXDugs6J
    0x100: b'D4FDrH92HO8ztZ1Bs492F4a3o9c3gixt',  # D4FDrH92HO8ztZ1Bs492F4a3o9c3gixtR8KclkwfYCRjGm634ueG9bINaB2IizQO
}
DEFAULT_SAVE_VERSION = 1

SAVE_MAGIC = 'SQEX'.encode()

SAVE_VERSION_SIZE_STRUCT = struct.Struct('<II')
SAVE_SIZE_CRC32_STRUCT = struct.Struct('<IIQ')


def get_save_is_encrypted_and_version(buffer):
    save_version, size_encrypted_size = SAVE_VERSION_SIZE_STRUCT.unpack(buffer[:SAVE_VERSION_SIZE_STRUCT.size])

    if save_version in SAVE_KEY_DICT and size_encrypted_size == len(buffer) - 8:
        return True, save_version
    elif buffer[0:len(SAVE_MAGIC)] == SAVE_MAGIC:
        return False, DEFAULT_SAVE_VERSION

    # unrecognized
    return None, None


def get_save_encrypt(buffer, save_version):
    save_size = len(buffer)
    save_crc32_sum = zlib.crc32(buffer)

    working_buffer = buffer + (bytes([0]) * (0x10 - (save_size % 0x10)))  # align for AES block
    working_buffer += SAVE_SIZE_CRC32_STRUCT.pack(save_size, save_crc32_sum, 0)

    result_buffer = bytes()
    result_buffer += struct.pack('<I', save_version)
    result_buffer += struct.pack('<I', len(working_buffer))
    result_buffer += AES.new(SAVE_KEY_DICT[save_version], AES.MODE_ECB).encrypt(working_buffer)
    return result_buffer


def get_save_decrypt(buffer, save_version):
    result_buffer = AES.new(SAVE_KEY_DICT[save_version], AES.MODE_ECB).decrypt(buffer[8:])
    save_size, save_crc32_sum, padding = SAVE_SIZE_CRC32_STRUCT.unpack(result_buffer[-SAVE_SIZE_CRC32_STRUCT.size:])
    return result_buffer[:save_size], save_crc32_sum == zlib.crc32(result_buffer[:save_size])
