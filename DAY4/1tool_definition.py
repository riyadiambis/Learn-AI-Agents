from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# 1. nama fungsi --> yang mau dipanggil
# 2. Desc --> memanggil ini kalau kamu mau menggunakan kalkulator untuk operasi matematika
# 3. Parameters --> parameter apa yang harus di isi

# contoh
# def penjumlahan(a, b):
#   return(a+b)

'''
1. Penjumlahan
2. Ambil jika mau menjumlahkan
3. a, b

'''


basic_template = {
    'type' : 'function', # membuat tipenya fungsi
    'function' : {
        'name' : 'fungtion_name', 
        'description' : 'apa yang funsi lakukan', # ini harus dideskripsikan karena llm hanya mengerti bahasa, harus di deskripsikan
        'parameters' : {
            'type' : 'object', # artinya ini bisa campur-campur
            'properties' : {
                'param1' : {
                    'type' : 'string',
                    'description' : 'penjelasan paramter'
                },
                'param2' : {
                    'type' : 'number',
                    'description' : 'penjelasan paramter'
                },
            },
            'requared' : ['param1'] # parameter mana yang bisa diguankana untuk memanggil fungsi ini 
        }
    }
}


'''

5 PARAMETER UTAMA
1. string
2. number
3. bolean
4 array
5. object

'''


basic_template = {
    'type' : 'function', # membuat tipenya fungsi
    'function' : {
        'name' : 'fungtion_name', 
        'description' : 'apa yang funsi lakukan', # ini harus dideskripsikan karena llm hanya mengerti bahasa, harus di deskripsikan
        'parameters' : {
            'type' : 'object', # artinya ini bisa campur-campur
            'properties' : {
                'param1' : {
                    'type' : 'string',
                    'description' : 'penjelasan paramter'
                },
                'param2' : {
                    'type' : 'number',
                    'description' : 'penjelasan paramter'
                },
                'param3' : {
                    'type' : 'boolean',
                    'description' : 'penjelasan paramter'
                },
                'param4' : { 
                    'type' : 'array', # bukan definisi list tapi array dalam bahasa pemrograman lain
                    'item' : {'type' : 'string'},
                    'description' : 'penjelasan paramter'
                },
                'param5' : {
                    'type' : 'object', # nah ini banyak tipe data yang bisa dimasukkan
                    'properties' : {
                        'city' : {'type' : 'string'},
                        'code_zip' : {'type' : 'number'}
                    },
                    'description' : 'penjelasan paramter'
                },
            },
            'requared' : ['param1'] # parameter mana yang bisa diguankana untuk memanggil fungsi ini 
        }
    }
}


