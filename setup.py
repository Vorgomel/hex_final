import trotter
from tqdm import tqdm
import secp256k1 as ice

addr = str(input('Enter Your Bitcoin Address Here : (Example = 12NdrFv3DLoNVAXin7AS9dtoaKQkCWxVo9)\n Enter Here =  '))

HEX_key_FIND = str(input('Enter HEX with Missing Characters  as * : ((Example = 8ea6007390bee9daa120ac8aa5840230ed16f77c8611**d*ae5254********02)\n Enter Here =  '))


def complete_key(hex_key_find_string, missing_letters):
    for letter in missing_letters:
        hex_key_find_string = hex_key_find_string.replace('*', letter, 1)
    return hex_key_find_string


if __name__ == '__main__':
    missing_length = HEX_key_FIND.count('*')
    print(f"Looking for {missing_length} characters in {HEX_key_FIND}")
    allowed_characters = 'cdef'
    master_list = trotter.Amalgams(missing_length, allowed_characters)
    print(master_list)
    print(len(master_list))
    for i in tqdm(range(len(master_list))):
        test_key = complete_key(HEX_key_FIND, master_list[i])
        try:
            dec = int(test_key[0:64], 16)
            uaddr = ice.privatekey_to_address(0, False, dec)
            caddr = ice.privatekey_to_address(0, True, dec)
            if uaddr in addr or caddr in addr:
                wifc = ice.btc_pvk_to_wif(test_key)
                wifu = ice.btc_pvk_to_wif(test_key, False)
                print('WINNER WINNER Check WINNER.txt')
                f = open('WINNER.txt', 'a')
                f.write('===========================================================================\n')
                f.write(
                    f"DEC Key: {dec} \n HEX Key: {test_key} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc}\nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu}\n")
                f.write('===========================================================================\n')
                f.close()
        except ValueError:
            pass
