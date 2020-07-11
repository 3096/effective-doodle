import dq11s.save
import sys
import struct

DRACONIAN_FLAG_IDENTIFIER = "DLC_00".encode()
DRACONIAN_FLAG_OFFSET_FROM_IDENTIFIER = -0x30
DRACONIAN_FLAG_STRUCT = struct.Struct('<IIIIIIII')
DRACONIAN_FLAGS_TO_ADD = [
    1,  # flag 0
    1,  # flag 1
    1,  # flag 2
    1,  # flag 3
    1,  # flag 4
    1,  # flag 5
    1,  # flag 6
    1,  # flag 7
]

if __name__ == "__main__":
    save_path = sys.argv[1]

    with open(save_path, 'rb') as save_file:
        save_buffer = save_file.read()

    save_is_encrypted, save_version = dq11s.save.get_save_is_encrypted_and_version(save_buffer)

    if save_is_encrypted is None:
        print("file not recognized")
        exit(-1)

    if save_is_encrypted:
        save_buffer, is_verified = dq11s.save.get_save_decrypt(save_buffer, save_version)
        if not is_verified:
            print("failed to verify save decryption")
            exit(-2)

    draconian_identifier_offset = save_buffer.find(DRACONIAN_FLAG_IDENTIFIER)
    if draconian_identifier_offset == -1:
        print("failed to find flag location")
        exit(-3)

    draconian_offset = draconian_identifier_offset + DRACONIAN_FLAG_OFFSET_FROM_IDENTIFIER

    save_buffer = save_buffer[:draconian_offset] + DRACONIAN_FLAG_STRUCT.pack(*DRACONIAN_FLAGS_TO_ADD) \
                  + save_buffer[draconian_offset + DRACONIAN_FLAG_STRUCT.size:]

    with open(save_path, 'wb') as out_file:
        out_file.write(dq11s.save.get_save_encrypt(save_buffer, save_version))

    print("pray to sothis that this has worked wait wrong franchise")
