import dq11s.save
import sys

if __name__ == "__main__":
    save_path = sys.argv[1]

    with open(save_path, 'rb') as save_file:
        save_buffer = save_file.read()

    save_is_encrypted, save_version = dq11s.save.get_save_is_encrypted_and_version(save_buffer)

    if save_is_encrypted is None:
        print("file not recognized")
        exit(-1)

    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    elif save_is_encrypted:
        out_path = save_path + ".dec"
    else:
        out_path = save_path + ".enc"

    with open(out_path, 'wb') as out_file:
        if save_is_encrypted:
            save_buffer, is_verified = dq11s.save.get_save_decrypt(save_buffer, save_version)
            out_file.write(save_buffer)
            if is_verified:
                print(f"successfully decrypted to {out_path}")
            else:
                print("failed to verify, decryption maybe have produced garbage")

        else:
            out_file.write(dq11s.save.get_save_encrypt(save_buffer, save_version))
            print(f"successfully encrypted to {out_path}")
