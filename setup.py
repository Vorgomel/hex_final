from itertools import product
from tqdm import tqdm
import secp256k1 as ice

# Захардкоженные значения
addr = '1E4t1MyEer1FKLWZdpkjoPMaXF6ybw9uC9'
HEX_key_FIND = '9FC82E36FA2E7C1B59694A1B3CC5FF3200592CC2F99A160740E************B'
# первая позиция - 0, последняя - 63
# Словарь с возможными значениями для каждой неизвестной позиции
# Словарь с возможными значениями для каждой неизвестной позиции
position_values = {
    51: ['4', '3', 'a', 'e'],
    52: ['4', '3', 'a', 'e'],
    53: ['4', 'f', 'a', 'e'],
    54: ['4', 'd', 'a', 'e'],
    55: ['4', '0', 'a', 'e'],
    56: ['4', '0', 'a', 'e'],
    57: ['8', '0', 'a', 'e'],
    58: ['4', 'f', 'a', 'e'],
    59: ['4', '0', 'a', 'e'],  # '4' это валидное значение
    60: ['0', '3', 'b', 'f'],  # '0' это валидное значение
    61: ['7', '0', '4', 'c'],  # '7' это валидное значение
    62: ['4', '2', '0', '3'],  # '4' это валидное значение

}


def generate_combinations(hex_key, pos_values):
    positions = sorted(pos_values.keys())
    values = [pos_values[pos] for pos in positions]
    combos = product(*values)
    for combo in combos:
        new_key = list(hex_key)
        for i, pos in enumerate(positions):
            new_key[pos] = combo[i]
        yield ''.join(new_key)


if __name__ == '__main__':
    print(f"Исходный HEX с неизвестными позициями: {HEX_key_FIND}")
    combinations = list(generate_combinations(HEX_key_FIND, position_values))
    print(f"Всего комбинаций для проверки: {len(combinations)}")

    for test_key in tqdm(combinations):
        try:
            dec = int(test_key[0:64], 16)
            uaddr = ice.privatekey_to_address(0, False, dec)
            caddr = ice.privatekey_to_address(0, True, dec)
            if uaddr == addr or caddr == addr:
                wifc = ice.btc_pvk_to_wif(test_key)
                wifu = ice.btc_pvk_to_wif(test_key, False)
                print('ПОБЕДИТЕЛЬ! Проверьте файл WINNER.txt')
                with open('WINNER.txt', 'a') as f:
                    f.write('===========================================================================\n')
                    f.write(
                        f"DEC Key: {dec} \n HEX Key: {test_key} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc}\nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu}\n")
                    f.write('===========================================================================\n')
                break
        except ValueError:
            continue  # Пропускаем невалидные значения HEX
